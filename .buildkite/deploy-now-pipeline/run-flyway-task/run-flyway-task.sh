#!/bin/bash
#------------------------------------------------------------------------------
# run-flyway-task
#------------------------------------------------------------------------------

set -euo pipefail

# global vars
security_group_id=""
subnet_id=""
log_group_name=""
env_name_temp=$(buildkite-agent meta-data get env)
env_region=${env_name_temp%_*}
env_name=${env_name_temp#*_}
cluster_name=""
flyway_image_version=$(buildkite-agent meta-data get new_version)
terraform_config=$(buildkite-agent meta-data get terraform_config)


function installEcsRunTasksDockerImage() {
  echo
  echo "--- installing ecs run tasks docker image---"

  unset AWS_ACCESS_KEY_ID
  unset AWS_SECRET_ACCESS_KEY
  unset AWS_SESSION_TOKEN

  $(aws ecr get-login --no-include-email --region ap-southeast-2)
  docker pull 361053881171.dkr.ecr.ap-southeast-2.amazonaws.com/paylater/deploynow/utils:ecs-run-task01

}


function generateTaskDefinition() {
  echo "DEBUG2"
  if [ -f "/tmp/task_definition.json" ] ; then
      rm -rf /tmp/task_definition.json
  fi

  echo "ENV REGION $env_region"
  echo "FLYWAY_VERSION $flyway_image_version"
  task_arn=$(aws resourcegroupstaggingapi get-resources --region $env_region --resource-type-filters ecs:task-definition --tag-filters Key=Tag,Values=FLYWAY Key=Flyway,Values=true Key=Name,Values=$env_name-$terraform_config --max-items 1 | jq --raw-output '.ResourceTagMappingList[].ResourceARN')
  echo "TASK ARN $task_arn"
  aws ecs describe-task-definition --task-definition $task_arn --region $env_region >> /tmp/task_definition.json

  # replace FLYWAY_IMAGE_VERSION with actual passed version
  sed -i "s/FLYWAY_IMAGE_VERSION/$flyway_image_version/g" /tmp/task_definition.json
}


function getStsToken() {
  echo "DEBUG1"
  echo "ENV REGION $env_region"
  echo "ENV NAME $env_name"
  temp_role=$(aws sts assume-role --role-arn arn:aws:iam::$account_id:role/terraform-paylater-deploynow-ecs --role-session-name buildkite-flyway-deploy --region $env_region)

  export AWS_ACCESS_KEY_ID=$(echo $temp_role | jq .Credentials.AccessKeyId | xargs)
  export AWS_SECRET_ACCESS_KEY=$(echo $temp_role | jq .Credentials.SecretAccessKey | xargs)
  export AWS_SESSION_TOKEN=$(echo $temp_role | jq .Credentials.SessionToken | xargs)
}


function getTaskDetails() {
    echo "DEBUG3"
    # To get variables required for running the ecs-run-task job
    export security_group_id=$(cat /tmp/task_definition.json | jq -r --arg container_def "$env_name-$terraform_config-flyway" '.taskDefinition.containerDefinitions[] | select(.name==$container_def) | .environment[] | select(.name == "SECURITY_GROUP") | .value' | xargs)
    export subnet_id=$(cat /tmp/task_definition.json | jq -r --arg container_def "$env_name-$terraform_config-flyway" '.taskDefinition.containerDefinitions[] | select(.name=$container_def) | .environment[] | select(.name == "SUBNET") | .value' | xargs)
    export cluster_name=$(cat /tmp/task_definition.json | jq -r --arg container_def "$env_name-$terraform_config-flyway" '.taskDefinition.containerDefinitions[] | select(.name=$container_def) | .environment[] | select(.name == "CLUSTER_NAME") | .value' | xargs)
    export log_group_name=$(cat /tmp/task_definition.json | jq -r --arg container_def "$env_name-$terraform_config-flyway" '.taskDefinition.containerDefinitions[] | select(.name=$container_def) | .environment[] | select(.name == "LOG_GROUP") | .value' | xargs)
}

#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
installEcsRunTasksDockerImage
getStsToken
generateTaskDefinition
getTaskDetails

echo "-------"
cat /tmp/task_definition.json | jq '.taskDefinition' > /tmp/task_definition_final.json
echo "----"
cat /tmp/task_definition_final.json
echo "-------"

echo

echo "--"
echo $env_region
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
echo $AWS_SESSION_TOKEN
echo $env_name
echo $security_group_id
echo $subnet_id
echo $log_group_name
echo "--"

echo "--- :berserk: running flyway for database $env_name-card-flyway-task Version: $flyway_image_version ---"
export AWS_DEFAULT_REGION=$env_region
docker run -v /tmp:/tmp -e AWS_REGION=$env_region \
                        -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
                        -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
                        -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
                        361053881171.dkr.ecr.ap-southeast-2.amazonaws.com/paylater/deploynow/utils:ecs-run-task01 \
                        --debug \
                        --file /tmp/task_definition_final.json \
                        --name $env_name-flyway-task \
                        --cluster $cluster_name \
                        --fargate \
                        --security-group $security_group_id \
                        --subnet $subnet_id \
                        --log-group $log_group_name

echo
echo "end"
