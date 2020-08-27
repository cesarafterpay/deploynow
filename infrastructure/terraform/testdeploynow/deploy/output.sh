#!/bin/bash -e

for arg in "$@"; do
    case $arg in
        --env=*)
            env="${arg#*=}"
            shift # past argument=value
        ;;
        *)
                # unknown option
        ;;
    esac
done

cd "$(dirname "$0")"

source ./environment-${env}.sh
source ./secrets-${env}.sh

mkdir -p out

cd ..
rm -rf .terraform
terraform init -input=false -backend-config "role_arn=arn:aws:iam::${TF_VAR_account_id}:role/terraform-state-manager" -backend-config "bucket=${TF_VAR_state_bucket}"
terraform workspace select ${env} || terraform workspace new ${env}
terraform output
