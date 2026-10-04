#!/bin/sh
set -e
cd "$(dirname "$0")/.."

pnpm dlx @biomejs/biome@2.5.7 format --write web/index.html web/app.js web/app.css && pnpm dlx @biomejs/biome@2.5.7 check --write web/index.html web/app.js web/app.css
