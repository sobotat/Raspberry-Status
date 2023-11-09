#!/bin/bash
nohup sudo python -u main.py > "crash.log" 2>&1 < /dev/null &
nohup python -u main_monitor.py > "crash_monitor.log" 2>&1 < /dev/null &
echo "App was started"