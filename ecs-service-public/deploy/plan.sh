#!/bin/bash -e

for arg in "$@"; do
    case $arg in
        --env=*)
            env="${arg#*=}"
            shift # past argument=value
        ;;
        --version=*)
            version="${arg#*=}"
            shift # past argument=value
        ;;
        *)
                # unknown option
        ;;
    esac
done

export TF_VAR_application_version="${version}"

cd "$(dirname "$0")"

source ./environment-${env}.sh
if [ -f ./secrets-${env}.sh ];
 then source ./secrets-${env}.sh;
fi

mkdir -p out

cd ..
rm -rf .terraform
terraform init -input=false -backend-config "role_arn=arn:aws:iam::${TF_VAR_account_id}:role/terraform-state-manager" -backend-config "bucket=${TF_VAR_state_bucket}"
terraform workspace select ${env} || terraform workspace new ${env}
terraform plan -var-file=tfvars/${env}.tfvars -out=deploy/out/${tfplan}
