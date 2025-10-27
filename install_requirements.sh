#!/usr/bin/env bash
set -euo pipefail
# Install requirements from the ecom app
if [ -f "requirements.txt" ]; then
  echo "Using root requirements.txt"
  pip install -r requirements.txt
elif [ -f "ecom/requirements.txt" ]; then
  echo "Using ecom/requirements.txt"
  pip install -r ecom/requirements.txt
else
  echo "No requirements.txt found" >&2
  exit 1
fi