# Script to configure centos7 with necessary packages to create the Synthetic US Population
# usage: sudo bash CONFIGURE_CENTOS7.bash
#
# these make centos easier for use. It's not necessary, and it increases bloat, but it's generally worth it.
yum -y install emacs screen git 

# Bring the system up to date. Again, not necessary, but useful:
yum -y makecache fast
yum -y update


#
# Install Python3.4 and necessary tools
# See https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-centos-7
sudo yum -y install yum-utils md5deep
sudo yum -y groupinstall development
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
sudo yum -y install python36u-pip
sudo pip3.6 install numpy pandas ipython 


# Note: We do not create a python36 virtual environment, but we probably should

#
# this brings in the necessary tools:
sudo yum -y install wget


