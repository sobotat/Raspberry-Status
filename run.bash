#!/bin/bash
nohup sudo python -u main.py > "crash.log" 2>&1 < /dev/null &
echo "main.py was started"