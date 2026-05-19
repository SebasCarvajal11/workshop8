#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
pip install -e .
cd web
corepack enable
corepack prepare pnpm@11.1.1 --activate
pnpm install
pnpm build
