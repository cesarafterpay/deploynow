def get_aws_account_details(env):
    # return env attributes
    env_details = {}

    # Find account
    if env in ['dev', 'us-dev', 'eu-dev', 'gl-dev', 'migdev', 'tech']:
        env_details['id'] = '568431661506'
        env_details['name'] = 'alpha'
    elif env in ['qa', 'us-qa', 'eu-qa', 'gl-qa', 'stg', 'stg2', 'us-stg', 'eu-stg', 'pentest', 'gl-stg', 'qaload', 'pentest', 'tpi', 'us-tpi', 'gl-tpi']:
        env_details['id'] = '723236915308'
        env_details['name'] = 'beta'
    elif env in ['sbox', 'us-sbox', 'eu-sbox', 'gl-sbox']:
        env_details['id'] = '687512651472'
        env_details['name'] = 'psi'
    elif env in ['prod', 'prod2', 'us-prod', 'us-prod2', 'eu-prod', 'eu-prod2', 'gl-prod']:
        env_details['id'] = '830726149330'
        env_details['name'] = 'omega'
    else:
        print(env + ' environment AWS account_id and name not found')
        return False

    # Find region
    if env in ['dev', 'migdev', 'tech', 'qa', 'stg', 'qaload', 'tpi', 'sbox', 'prod']:
        env_details['region'] = 'ap-southeast-2'
    elif env in ['stg2', 'prod2']:
        env_details['region'] = 'ap-southeast-1'
    elif env in ['us-dev', 'us-qa', 'us-stg', 'us-tpi', 'us-sbox', 'us-prod']:
        env_details['region'] = 'us-east-1'
    elif env in ['us-prod2', 'gl-dev', 'gl-qa', 'gl-stg', 'gl-tpi', 'gl-sbox', 'gl-prod']:
        env_details['region'] = 'us-west-2'
    elif env in ['eu-dev', 'eu-qa', 'pentest', 'eu-stg', 'eu-sbox', 'eu-prod']:
        env_details['region'] = 'eu-west-1'
    elif env in ['eu-prod2']:
        env_details['region'] = 'eu-central-1'
    else:
        print(env + ' environment region not found')
        return False

    return env_details
