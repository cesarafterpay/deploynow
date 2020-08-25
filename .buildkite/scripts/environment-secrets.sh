#!/bin/bash
set -euo pipefail

echo "+++ :zipper_mouth_face: Getting secrets from secrets manager and saving to environment"
secret_var_list=(${config_secrets:-})

for i in "${secret_var_list[@]}"
do
    env_var=$(echo ${i} | cut -f1 -d:)
    secret_name=$(echo ${i} | cut -f2 -d:)
    secret_value=`python .buildkite/scripts/python/paylater/secrets.py --secret_name ${secret_name} --env ${env} --account_id ${account_id} --role_name terraform-secrets`
    echo "exporting secret ${secret_name} to ${env_var}"
    export ${env_var}="${secret_value}"
done
