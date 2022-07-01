#!/usr/bin/env bash

set -o errexit

# Change directory to the project root directory.
cd "$(dirname "$0")"

# Run on all files,
# ignoring the paths passed to this script,
# so as not to miss type errors.
mypy --package example --namespace-packages
