def generate_test_environment_step(label, concurrency_group, agent_queue, env_vars=None):
    test_step = {
        'label': label,
        'command': '.buildkite/deploy-now-pipeline/utils/test_deployment.sh',
        'agents': {'queue': agent_queue},
        'concurrency': 1,
        'concurrency_group': concurrency_group,
        'plugins': {
            'docker#v3.5.0': {
                'image': 'afterpaytouch/p-toolkit:1.0.3',
                'workdir': '/home',
                'propagate-environment': True
            }
        }
    }

    if env_vars is not None:
        test_step['env'] = env_vars

    return test_step
