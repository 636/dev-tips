#!/usr/bin -e
# -*- coding: utf-8 -*-

USER_ID=$(id -u)
GROUP_ID=$(id -g)

if [ x"$GROUP_ID" != x"0" ]; then
  groupadd -f -g $GROUP_ID $USER_NAME
fi

if [ x"$USER_ID" != x"0" ] && [ "$(getent passwd $USER_NAME)" = "" ]; then
  useradd -d /home/$USER_NAME -m -s /bin/bash -u $USER_ID -g $GROUP_ID $USER_NAME
  sudo chown -R $USER_NAME:$USER_NAME /home/$USER_NAME
fi

sudo chmod u-s /usr/sbin/useradd
sudo chmod u-s /usr/sbin/groupadd

cd /home/$USER_NAME

exec $@