#!/bin/bash

# init_deploy.sh — Bootstrap a fresh EC2 instance for aPersona Identity deployment
#
# This script:
# 1. Installs prerequisites (nvm, Node.js 22, npm, git, jq, aws-cdk)
# 2. Clones the release repo
# 3. Prompts user to configure tenants-config.json
# 4. Launches the installer
#
# Usage: curl -sL <url>/init_deploy.sh | bash
#   or:  ./init_deploy.sh

set -euo pipefail

# ============================================================
# Configuration
# ============================================================
REPO_BASE=https://github.com/kcsapersona/
export APERSONAIDP_REPO_NAME=aPersona-Identity_Multi-Tenant_Install

NVM_VER=v0.39.7
NODE_VER=22
NPM_VER=11.0.0

echo ""
echo "=============================================="
echo "aPersona Identity Manager — Initial Setup"
echo "=============================================="
echo ""

# ============================================================
# 1. Install system dependencies
# ============================================================
echo "--- Installing system dependencies ---"

# Install git and jq (required for tenants-config.json parsing)
if command -v yum &>/dev/null; then
    sudo yum update -y >/dev/null 2>&1
    sudo yum install -y git jq >/dev/null 2>&1
elif command -v apt-get &>/dev/null; then
    sudo apt-get update -y >/dev/null 2>&1
    sudo apt-get install -y git jq >/dev/null 2>&1
else
    echo "WARNING: Could not detect package manager. Ensure git and jq are installed."
fi
echo "  ✓ git and jq installed"

# ============================================================
# 2. Install Node.js via nvm
# ============================================================
echo ""
echo "--- Installing Node.js $NODE_VER via nvm $NVM_VER ---"

rm -rf "$HOME/.nvm"
curl -o- "https://raw.githubusercontent.com/nvm-sh/nvm/$NVM_VER/install.sh" | bash

# Source nvm into current shell
export NVM_DIR="$HOME/.nvm"
# shellcheck source=/dev/null
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

nvm install "$NODE_VER" >/dev/null
nvm use "$NODE_VER"
echo "  ✓ Node.js $(node --version) installed"

# ============================================================
# 3. Install npm and aws-cdk
# ============================================================
echo ""
echo "--- Installing npm v$NPM_VER and aws-cdk ---"

npm install -g "npm@$NPM_VER" >/dev/null 2>&1
npm install -g aws-cdk >/dev/null 2>&1
echo "  ✓ npm $(npm --version) installed"
echo "  ✓ aws-cdk $(cdk --version 2>/dev/null || echo 'installed') installed"

# ============================================================
# 4. Clone the release repo
# ============================================================
echo ""
echo "--- Cloning release repo ---"

if [[ -d "$APERSONAIDP_REPO_NAME" ]]; then
    echo "  Directory $APERSONAIDP_REPO_NAME already exists, pulling latest..."
    cd "$APERSONAIDP_REPO_NAME"
    git pull
else
    echo "  Cloning $REPO_BASE$APERSONAIDP_REPO_NAME ..."
    git clone "$REPO_BASE$APERSONAIDP_REPO_NAME"
    cd "$APERSONAIDP_REPO_NAME"
fi
echo "  ✓ Repository ready"

# ============================================================
# 5. Prompt user to configure tenants-config.json
# ============================================================
echo ""
echo "=============================================="
echo "  IMPORTANT: Configure tenants-config.json"
echo "=============================================="
echo ""
echo "Before running the installer, you MUST edit tenants-config.json with your settings:"
echo ""
echo "  Required fields:"
echo "    • aws.region          — Target AWS region (e.g., us-east-1)"
echo "    • aws.account         — Your AWS account ID"
echo "    • dns.rootDomain      — Your Route 53 domain"
echo "    • asm.installKey      — ASM install key (provided by aPersona)"
echo "    • asm.adminEmail      — Super admin email address"
echo "    • asm.salt            — ASM salt (provided by aPersona)"
echo "    • smtp.*              — SMTP server configuration"
echo "    • samlgw2.adminToken  — SAML Gateway v2 admin token (for X-Admin-Token header)"
echo ""
echo "  Edit now with:  vi tenants-config.json"
echo ""
echo "  Then run the installer with:  ./install-multi-tenants.sh"
echo ""
