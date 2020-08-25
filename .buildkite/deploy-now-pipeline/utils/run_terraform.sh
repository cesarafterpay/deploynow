#!/bin/bash
set -euo pipefail

echo "+++ :terraform: Updating terraform version"
export account=`buildkite-agent meta-data get "account"`
export env=`buildkite-agent meta-data get "env"`
export TF_VAR_application_version=`buildkite-agent meta-data get "new_version"`
export terraform_config=`buildkite-agent meta-data get "terraform_config"`
export auto_deploy=`buildkite-agent meta-data get "auto_deploy"`

buildkite-agent annotate "<h3>Deploy Version $TF_VAR_application_version</h3>" --style "info" --context "ctx-info"

source .buildkite/scripts/environment-$account.sh
tfpath=${terraformpath:-"infrastructure/terraform/${terraform_config}"}

# Add no knownhost checking for git
if [ ! -f /root/.ssh/config ]; then
cat << EOF | tee /root/.ssh/config
Host *
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
EOF

chmod 600 /root/.ssh/config
fi

# Try to figure out the required version from the source
set +e
tfversion=$(grep -h -R required_version --include '*tf' ${tfpath}/* | sed 's/.*\([0-9]\+\.[0-9]\+\.[0-9]\+\).*/\1/')
set -e

if [[ -z "$tfversion" ]]; then
    echo "+++ :terraform: required version not found, continuing"
else
    # Download the required version
    echo "+++ :terraform: required version ${tfversion} found, downloading"
    cd /tmp
    wget "https://releases.hashicorp.com/terraform/${tfversion}/terraform_${tfversion}_linux_amd64.zip"
    unzip "terraform_${tfversion}_linux_amd64.zip"
    mv terraform /usr/bin
fi

cd /home

# Use time for cancelling jobs that maybe approved after extended period time to fail the job
plan_time="false"

# FIXME: Attempted to do a artifact upload in the preview and a subsequent download in the apply. Didnt work.
# Run preview plan only
if [[ "$auto_deploy" == "plan" ]]; then
  echo "+++ :terraform: plan app version $TF_VAR_application_version for environment $env"
  sh infrastructure/terraform/$terraform_config/deploy/plan.sh --env=$env --version=$TF_VAR_application_version
  plan_time=`date +%s`
fi

buildkite-agent meta-data set "plan_time" "${plan_time}"

# Run plan and apply
if [[ "$auto_deploy" == "true" || "$auto_deploy" == "apply" ]]; then

  # Check plan time is not greater than 5 mins
  plan_time=`buildkite-agent meta-data get "plan_time"`
  if [[ $plan_time != "false" ]]; then
    time_now=`date +%s`
    lapse_time=`expr $time_now - $plan_time`
    timeout=$((60 * 5)) # 5 mins
    if [[ $lapse_time -gt $timeout ]]; then
      echo "+++ :alarm_clock: Plan is greater than 5 minutes. Cancelling job"
      exit 1
    fi
  fi

  echo "+++ :terraform: plan and apply app version $TF_VAR_application_version for environment $env"
  sh infrastructure/terraform/$terraform_config/deploy/plan.sh --env=$env --version=$TF_VAR_application_version
  sh infrastructure/terraform/$terraform_config/deploy/apply.sh --env=$env
fi