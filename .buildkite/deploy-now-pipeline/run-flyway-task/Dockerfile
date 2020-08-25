# This docker image is currently built and pushed to the following repository and tag. This image is refernced in the
# run-flyway-task.sh script to run the flyway migrate
# 361053881171.dkr.ecr.ap-southeast-2.amazonaws.com/paylater/deploynow/utils:ecs-run-task01

FROM alpine:3.9

RUN apk update && apk upgrade
RUN apk add make curl jq bash openssl python py-pip git
RUN pip install awscli

ENV VERSION v1.3.0
RUN curl -LO https://github.com/buildkite/ecs-run-task/releases/download/${VERSION}/ecs-run-task-linux-amd64 \
  && chmod +x ecs-run-task-linux-amd64 \
  && mv ecs-run-task-linux-amd64 /usr/local/bin/ecs-run-task

ENTRYPOINT [ "ecs-run-task" ]
