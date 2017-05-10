#!/bin/bash

while true;
do
  # mysql
  count=`ps -ef | grep "mysqld" | grep -v "grep"`
  if [ "$?" != "0" ]; then
    echo '[mysqld] shutdown'
    systemctl restart mysqld
  fi
  # fetch
  count=`ps -ef | grep "python" | grep "service\.py fetch" | grep -v "grep"`
  if [ "$?" != "0" ]; then
    echo '[fetch] shutdown'
    nohup python service.py fetch >/dev/null 2>&1 &
  fi
  # check
  count=`ps -ef | grep "python" | grep "service\.py check" | grep -v "grep"`
  if [ "$?" != "0" ]; then
    echo '[check] shutdown'
    nohup python service.py check >/dev/null 2>&1 &
  fi
  sleep 2
done

