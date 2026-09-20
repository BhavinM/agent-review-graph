#!/bin/bash
set -e

# Inputs mapped from action.yml
TARGET=$1
FAIL_ON_CONTRADICTION=$2
OUTPUT_DIR=$3

echo "🚀 Starting AgentReviewGraph Action..."

CMD="agent-review ${TARGET} --output-dir ${OUTPUT_DIR}"

if [ "${FAIL_ON_CONTRADICTION}" = "true" ]; then
    CMD="${CMD} --fail-on-contradiction"
fi

echo "Running: $CMD"
$CMD
