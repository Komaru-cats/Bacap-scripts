#!/usr/bin/env bash
set -e

# Load .env.bacap_addon from working directory if it exists
if [ -f ".env.wb_addon" ]; then
    set -a
    # Filter comments and empty lines
    # shellcheck disable=SC1090
    source <(grep -v '^#' .env.bacap_addon | grep -v '^[[:space:]]*$')
    set +a
fi

# Execute the helper binary with all passed arguments
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${SCRIPT_DIR}/helpers/wb_addon_helper" "$@"