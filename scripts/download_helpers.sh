#!/usr/bin/env bash
#
# Downloads latest release assets for BACAP-Addon-Helper and WB-Addon-Helper.
# Selects framework-dependent binaries if .NET 10 runtime is detected,
# otherwise falls back to self-contained binaries. Target directory is configured via HELPERS_DIR.
#
set -euo pipefail

# Configure output directory via environment variable with a default fallback
HELPERS_DIR="${HELPERS_DIR:-scripts/helpers}"
mkdir -p "${HELPERS_DIR}"

# Detect operating system
OS_NAME="$(uname -s)"
case "${OS_NAME}" in
    Linux*)  OS="linux" ;;
    Darwin*) OS="osx" ;;
    *)
        echo "[ERROR] Unsupported operating system: ${OS_NAME}" >&2
        exit 1
        ;;
esac

# Detect CPU architecture
ARCH_NAME="$(uname -m)"
case "${ARCH_NAME}" in
    x86_64|amd64)  ARCH="x64" ;;
    arm64|aarch64) ARCH="arm64" ;;
    *)
        echo "[ERROR] Unsupported CPU architecture: ${ARCH_NAME}" >&2
        exit 1
        ;;
esac

# Check for .NET 10 runtime availability
HAS_DOTNET10=0
if command -v dotnet >/dev/null 2>&1; then
    if dotnet --list-runtimes 2>/dev/null | grep -q "^Microsoft\.NETCore\.App 10\."; then
        HAS_DOTNET10=1
    fi
fi

if [ "${HAS_DOTNET10}" -eq 1 ]; then
    echo "[.NET 10 Found] Target: framework-dependent binaries"
else
    echo "[.NET 10 Not Found] Target: self-contained binaries"
fi

echo "Destination directory: ${HELPERS_DIR}"

##
# Downloads an asset from GitHub Releases into the target directory and marks it executable.
#
# @param $1 repo_slug       GitHub repository path (e.g. "owner/repo").
# @param $2 asset_prefix    Asset file prefix (e.g. "BACAP_Addon_Helper").
# @param $3 output_name     Target file name on disk (e.g. "bacap_addon_helper").
#
# @return 0 on success, 1 on failure.
#
# @example
#   download_asset "ItzSkyReed/BACAP-Addon-Helper" "BACAP_Addon_Helper" "bacap_addon_helper"
##
download_asset() {
    local repo_slug="$1"
    local asset_prefix="$2"
    local output_name="$3"
    local target_path="${HELPERS_DIR}/${output_name}"

    local asset_name
    if [ "${HAS_DOTNET10}" -eq 1 ]; then
        asset_name="${asset_prefix}-framework-dependent-${OS}-${ARCH}"
    else
        asset_name="${asset_prefix}-${OS}-${ARCH}"
    fi

    local download_url="https://github.com/${repo_slug}/releases/latest/download/${asset_name}"
    echo "Fetching ${asset_name} -> ${target_path}..."

    if command -v curl >/dev/null 2>&1; then
        curl -fL "${download_url}" -o "${target_path}"
    elif command -v wget >/dev/null 2>&1; then
        wget -q --show-progress "${download_url}" -O "${target_path}"
    else
        echo "[ERROR] Neither curl nor wget is available in PATH." >&2
        return 1
    fi

    chmod +x "${target_path}"
    echo "[OK] Saved: ${target_path}"
}

# Download BACAP Addon Helper
download_asset "ItzSkyReed/BACAP-Addon-Helper" "BACAP_Addon_Helper" "bacap_addon_helper"

# Download WB Addon Helper
download_asset "ItzSkyReed/WB-Addon-Helper" "WB_Addon_Helper" "wb_addon_helper"

echo "[SUCCESS] All helpers downloaded and ready in ${HELPERS_DIR}."