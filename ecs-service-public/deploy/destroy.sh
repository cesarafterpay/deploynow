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

cd ..
terraform workspace select ${env}
terraform destroy -var-file=tfvars/${env}.tfvars
terraform workspace select default
terraform workspace delete ${env}
