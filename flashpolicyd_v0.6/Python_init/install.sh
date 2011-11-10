#!/bin/sh

install -m644 ../flashpolicy.xml /usr/local/etc/

install -m755 flashpolicyd.py /usr/local/sbin/
install -m755 flashpolicyd.init /etc/init.d/flashpolicyd
chkconfig --add flashpolicyd
