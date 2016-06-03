#!/bin/sh

### BEGIN INIT INFO
# Provides:          pigpio as a service starting automatically at boot time.
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Provides access to the Raspberry Pi GPIOs without a need to be root
# Description:       TBA
# Other instructions: This script should be made executable and placed at /etc/init.d, like this:
# sudo cp pigpiod.sh /etc/init.d
# Then, run "sudo update-rc.d pigpiod.sh defaults"
# To start/stop the service manually, use:
# sudo /etc/init.d/pigpiod.sh start
# sudo /etc/init.d/pigpiod.sh stop
# sudo /etc/init.d/pigpiod.sh status
#
# Install like this:
# Copy this file to the Raspberry Pi
# sudo cp pigpiod.sh /etc/init.d/
# sudo chmod +x /etc/init.d/pigpiod.sh
# sudo update-rc.d pigpiod.sh defaults
# sudo systemctl enable pigpiod
#
# More info on system services on Debian Jessie at 
# https://blog.sleeplessbeastie.eu/2015/04/27/how-to-manage-system-services-on-debian-jessie/
#
# To remove the service:
# sudo update-rc.d -f pigpiod remove
#
### END INIT INFO

DIR=/usr/bin/pigpiod
DAEMON=$DIR/pigpiod
DAEMON_NAME=pigpiod

# Add any command line options for your daemon here
DAEMON_OPTS=""

# This next line determines what user the script runs as.
# Root generally not recommended but necessary if you are using the Raspberry Pi GPIO from Python.
DAEMON_USER=root

# The process ID of the script when it runs is stored here:
PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --startas $DAEMON -- $DAEMON_OPTS
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0