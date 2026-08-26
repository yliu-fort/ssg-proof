#!/usr/bin/env bash
# Rebuild frontier.pdf and mirror it to Google Drive (gdrive:ssg-proof/).
#
# The rclone remote "gdrive:" is already configured in ~/.config/rclone/rclone.conf.
# Uploading through rclone rather than the Drive MCP tool keeps the whole PDF out
# of the model's context, which matters: the file base64-encodes to ~550 KB.
set -euo pipefail

cd "$(dirname "$0")/.."

TEX="${TEX:-frontier}"
REMOTE="${REMOTE:-gdrive:ssg-proof/}"

make pdf "TEX=$TEX" >/dev/null
rclone copy "$TEX.pdf" "$REMOTE"
echo "synced $TEX.pdf -> $REMOTE"
