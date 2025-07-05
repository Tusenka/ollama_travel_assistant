#!/bin/bash
set +e
set -x
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ) >> j
[ ! -f "$SCRIPT_DIR"/.env ] && echo "***file .env doesn't exist***" && exit 1
set -a && source "$SCRIPT_DIR"/.env && set +a

if [ ! -d "$SCRIPT_DIR"/venv ]; then
        echo "***Creating venv***"
        python3 -m venv "$SCRIPT_DIR"/venv
fi

sudo lsof -iTCP:"${GPT_ASSIST_PORT:-8000}" | awk '{print $2}' | grep -v PID | xargs -I {} sudo kill {}
echo "***Getting source for python for venv***"
source "$SCRIPT_DIR"/venv/bin/activate
echo "***Installing python requirements***"
pip3 install -r "$SCRIPT_DIR"/requirements.txt
echo "***Running app***"
python3 "$SCRIPT_DIR"/main.py >> logs.log
echo "***done***"
set -e
set +x