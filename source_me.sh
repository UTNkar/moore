#!/bin/bash

# This script should be sourced, `source source_me.sh`, to enter the python
# virtual environment used for Project Moore. If the environment is not yet
# present, then it will be created.

if [[ $SHLVL -gt 1 ]]; then
    echo "Remember: you need to run me as 'source ./source_me.sh', not execute
it!"
    exit
fi

if [ -d venv ]; then
    source venv/bin/activate
else
    python3 -m venv venv
    source venv/bin/activate
fi
