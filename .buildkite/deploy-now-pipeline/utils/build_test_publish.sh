#!/bin/bash

PUBLISH_TASKS=""

if [[ "${BUILDKITE_BRANCH}" == "master" ]] ; then
    PUBLISH_TASKS="jib"
fi

./gradlew \
    --console=plain \
    --no-daemon \
    --stacktrace \
    -Dfile.encoding=UTF-8 \
    -Djib.console=plain \
    -Djib.httpTimeout=60000 \
    clean build ${PUBLISH_TASKS}

EXIT_CODE=$?

exit $EXIT_CODE
