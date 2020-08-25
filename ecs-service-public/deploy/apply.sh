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
if [ -f ./secrets-${env}.sh ];
 then source ./secrets-${env}.sh;
fi

cd ..
terraform apply "deploy/out/${tfplan}"
