import boto3
import botocore
import logging
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ecr_client = boto3.client('ecr', region_name='ap-southeast-2')

def get_ecr_image_tags(repo_name):
    # Return list of repository tags/versions
    paginator = ecr_client.get_paginator('list_images')
    response_iterator = paginator.paginate(
        repositoryName=repo_name,
        filter={
            'tagStatus': 'TAGGED'
        },
        PaginationConfig={
            'MaxItems': 100000,
            'PageSize': 1000
        }
    )

    images = []

    for page in response_iterator:
        for image in page['imageIds']:
            images.append(image['imageTag'])

    images.sort(reverse=True)

    return images

def main():
    # For testing only
    repo_name = 'paylater/card/marqeta-gateway'
    print(get_ecr_image_tags(repo_name))

if __name__ == '__main__':
    main()
