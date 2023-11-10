#!/bin/bash
nohup python -u ../main_monitor.py > "crash_monitor.log" 2>&1 < /dev/null &
echo "main_monitor.py was started"