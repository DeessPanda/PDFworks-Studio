#!/bin/bash
cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)"
./venv/bin/python -m pdfworks_studio.main
