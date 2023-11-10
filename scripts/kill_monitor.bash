#!/bin/bash
ps -ef | grep "main_monitor.py" | grep -v grep | awk '{print $2}' | sudo xargs kill
echo "process main_monitor.py killed"