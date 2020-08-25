from __future__ import print_function

import os
import sys

import yaml
from aws_account_details import get_aws_account_details
from ecr_image_tags import get_ecr_image_tags

try:
    from generate_app_testing_pipeline import generate_test_environment_step
except ImportError:
    generate_test_environment_step = None


def generate_version_list_step(repo_name):
    # Get list of versions/docker tags available in the service's ECR repo
    versions = get_ecr_image_tags(repo_name)
    versions_list = []
    for version in versions:
        versions_list.append({'label': str(version), 'value': str(version)})

    step = [
        {
            'block': 'SelectVersion',
            'label': ':radio_button: Select Deploy Version',
            'prompt': 'Select version to deploy',
            'fields': [
                {   'select': 'Version',
                    'key': 'new_version',
                    'options': versions_list
                }
            ]
        }
    ]

    return step


def generate_docker_step(label, commands, concurrency_group, agent_queue, env_vars=None):
    # Build docker step template
    docker_step = {
        'label': label,
        'commands': commands if isinstance(commands, list) else [commands],
        'agents': {'queue': agent_queue},
        'concurrency': 1,
        'concurrency_group': concurrency_group,
        'plugins': {
            'docker#v3.0.1': {
                'image': 'afterpaytouch/p-toolkit:1.0.3',
                'workdir': '/home',
                'propagate-environment': True,
                'mount-ssh-agent': True,
                # For whatever reason things in the environment hook are not propagated so doing so here.
                'environment': [
                    'BUILDKITE_ARTIFACT_UPLOAD_DESTINATION',
                    'BUILDKITE_S3_DEFAULT_REGION',
                    'BUILDKITE_S3_ACL'
                ]
            }
        }
    }

    if env_vars is not None:
        docker_step['env'] = env_vars

    return docker_step


def generate_env_deploys(auto_deploy_list, envs, terraform_config, run_flyway):
    # Generate the environment specific terraform plan and apply steps
    steps = []

    for env in envs:
        env_details = get_aws_account_details(env)
        account_id = env_details.get('id')
        account_name = env_details.get('name')
        concurrency_group = '/terraform/%s/%s/%s' % (account_name, env, terraform_config)
        steps.append('wait')

        # Check if flyway step
        if run_flyway is not None:
            region = env_details.get('region')
            steps.append(run_flyway_task(account_id, env, region, terraform_config))
            steps.append('wait')

        if env in auto_deploy_list:
            steps.append(generate_docker_step(
                ':terraform: :hammer_and_wrench: Running plan and apply %s in env %s' % (terraform_config, env),
                ['buildkite-agent meta-data set "account" "'+account_name+'" ',
                 'buildkite-agent meta-data set "env" "'+env+'" ',
                 'buildkite-agent meta-data set "terraform_config" "'+terraform_config+'" ',
                 'buildkite-agent meta-data set "auto_deploy" "true" ',
                 '.buildkite/deploy-now-pipeline/utils/run_terraform.sh'],
                concurrency_group,
                'paylater-'+account_name+'-deploy-ci'
            ))
            steps.append('wait')
        else:
            steps.append(generate_docker_step(
                ':terraform: :hammer_and_wrench: Running plan %s in env %s' % (terraform_config, env),
                ['buildkite-agent meta-data set "account" "'+account_name+'" ',
                 'buildkite-agent meta-data set "env" "'+env+'" ',
                 'buildkite-agent meta-data set "terraform_config" "'+terraform_config+'" ',
                 'buildkite-agent meta-data set "auto_deploy" "plan" ',
                 '.buildkite/deploy-now-pipeline/utils/run_terraform.sh'],
                concurrency_group,
                'paylater-'+account_name+'-deploy-ci'
            ))
            steps.append('wait')
            steps.append(
                {
                    'block': 'ConfirmPlanAndDeploy',
                    'label': ':rocket: Confirm Plan and Deploy'
                }
            )
            steps.append('wait')
            steps.append(generate_docker_step(
                ':terraform: :hammer_and_wrench: Running apply %s in env %s' % (terraform_config, env),
                ['buildkite-agent meta-data set "account" "'+account_name+'" ',
                 'buildkite-agent meta-data set "env" "'+env+'" ',
                 'buildkite-agent meta-data set "terraform_config" "'+terraform_config+'" ',
                 'buildkite-agent meta-data set "auto_deploy" "apply" ',
                 '.buildkite/deploy-now-pipeline/utils/run_terraform.sh'],
                concurrency_group,
                'paylater-'+account_name+'-deploy-ci'
            ))
            steps.append('wait')

        if generate_test_environment_step:
            steps.append(generate_test_environment_step(
                ':terraform: :hammer_and_wrench: Testing deployment %s in env %s' % (terraform_config, env),
                concurrency_group,
                'paylater-' + account_name + '-deploy-ci'
            ))
            steps.append('wait')

    # Remove last Confirm
    steps.pop()

    return steps


def run_flyway_task(account, env, region, terraform_config):
    # Run the flyway task
    agent_queue = os.environ['BUILDKITE_AGENT_META_DATA_QUEUE']

    step = {
            'command': 'buildkite-agent meta-data set "terraform_config" "'+terraform_config+'" && buildkite-agent meta-data set "env" "'+region+'_'+env+'" && sh .buildkite/deploy-now-pipeline/run-flyway-task/run-flyway-task.sh',
            'label': ':airplane: Run flyway',
            'env': {'account_id': account},
            'agents': {'queue': agent_queue}
            }

    return step


def main():
    environmnet_list = os.environ.get("environmnet_list").split(",")
    auto_deploy_list = os.environ.get("auto_deploy_list", "").split(",")

    repo = os.environ['repo']
    terraform_config = os.environ['terraform_config']
    run_flyway = os.getenv("flyway_repo")

    steps = []

    if os.getenv("new_version") is not None:
        new_version = os.environ['new_version']
        cmd = 'buildkite-agent meta-data set "new_version" "'+new_version+'" '
        os.system(cmd)
    else:
        versions_step = generate_version_list_step(repo)
        steps = versions_step

    env_steps = generate_env_deploys(auto_deploy_list, environmnet_list, terraform_config, run_flyway)
    steps += env_steps

    pipeline = {'steps': steps}
    return yaml.safe_dump(pipeline, default_flow_style=False, width=10000)


if __name__ == '__main__':
    print(main(), file=sys.stdout)
