#!/usr/bin/env bash

SCRIPT_BASE="$(cd "$( dirname "$0")" && pwd )"
ROOT=${SCRIPT_BASE}/..

# Exit immediatly if any command exits with a non-zero status
set -e

# Usage
print_usage() {
    echo "Set the app/add-on version"
    echo ""
    echo "Usage:"
    echo "  set-version.sh <new-version>"
    echo ""
}

# if less than one arguments supplied, display usage
if [  $# -lt 1 ]
then
    print_usage
    exit 1
fi

# check whether user had supplied -h or --help . If yes display usage
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    print_usage
    exit 0
fi

# NEW_VERSION=$(echo "$1" | sed -e 's/-beta\./.b/' | sed -e 's/-alpha\./.a/')

# Set version in galaxy.yml
grep -E '^version: (.+)$' "$ROOT/galaxy.yml" >/dev/null
sed -i.bak -E "s/^version: (.+)$/version: $1/" "$ROOT/galaxy.yml" && rm "$ROOT/galaxy.yml.bak"

# Set version in docs/source/index.rst
grep -E '^Version: (.+)$' "$ROOT/docs/source/index.rst" > /dev/null
sed -i.bak -E "s/^Version: (.+)$/Version: $1/" "$ROOT/docs/source/index.rst" && rm "$ROOT/docs/source/index.rst.bak"