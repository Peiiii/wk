#!/bin/bash
# chkconfig: 2345 85 15
# description: start service at boot time
#. /etc/init.d/functions
SERVICE_NAME="{{service_name}}"
RETVAL=0
PID=-1
PIDFILE=/var/run/${SERVICE_NAME}.PID
PROJECT_PATH="{{project_dir}}"
SCRIPT_FILE_NAME='{{script_file_name}}'
LOG_PATH=${PROJECT_PATH}/service.log
start() {
  # 首先检查PID文件是否已存在
  if [ -f ${PIDFILE} ]; then
    echo "PID file ${PIDFILE} already exists, please stop the service !"
  else
    echo "Starting service ${SERVICE_NAME} ..."
    # >/dev/null 2>&1 表示不输出stdout和stderr
    # 最后一个 & 表示整个命令在后台执行
    cd ${PROJECT_PATH}
    python3 ${SCRIPT_FILE_NAME}  > ${LOG_PATH}  2>&1  &
    PID=$!  # 获取本shell启动的最后一个后台程序的进程号（PID）
    if [ -z ${PID} ]; then # 检查有没有获取到pid
      echo "Failed to get the process id, exit!"
    else
      echo "Starting successfully, whose pid is ${PID}"
    fi
    touch $PIDFILE
    echo ${PID} > ${PIDFILE}
  fi
}
stop() {
  if [ -f $PIDFILE ]; then # 检查PIDFILE是否存在
    PID=`cat ${PIDFILE}`
    if [ -z $PID ]; then # 检查PID是否存在于PIDFILE中
      echo "PIDFILE $PIDFILE is empty !"
    fi
    # 检查该进程是否存在
    if [ -z "`ps axf | grep $PID | grep -v grep`" ]; then
      echo "Process dead but pidfile exists! removing pidfile"
      rm -f ${PIDFILE}
    else
      kill -9 $PID
      rm -f ${PIDFILE}
      echo "Stopping service successfully , whose pid is $PID"
    fi
  else
    echo "File $PIDFILE does NOT exist!"
  fi
}
restart() {
  stop
  start
}
status() {
  # 检查pid file是否存在
  if [ -f $PIDFILE ]; then
    PID=`cat $PIDFILE`
    # 检查pid file是否存在pid
    if [ -z $PID ] ; then
      echo "No effective pid but pidfile exists!"
    else
      # 检查pid对应的进程是否还存在
      if [ -z "`ps axf | grep $PID | grep -v grep`" ]; then
        echo "Process dead but pidfile exist"
      else
        echo "Running"
      fi
    fi
  else
    echo "Service not running"
  fi
}
case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    restart
    ;;
  status)
    status
    ;;
  *)
    echo "Usage: mysite {start|stop|restart|status}"
    ;;
esac