#!/bin/bash
ps -ef | grep "main.py" | grep -v grep | awk '{print $2}' | sudo xargs kill
echo "process "main.py" killed"