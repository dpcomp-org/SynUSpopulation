#!/usr/bin/bash
#
# Create a 32GB swap file
# https://www.centos.org/docs/5/html/5.1/Deployment_Guide/s2-swap-creating-file.html
dd if=/dev/zero of=/home/centos/gits/swapfile bs=1048576 count=32
chmod 600 /home/centos/gits/swapfile
mkswap /home/centos/gits/swapfile
swapon /home/centos/gits/swapfile
