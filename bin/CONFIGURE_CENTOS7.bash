# Script to configure centos7 with necessary packages to create the Synthetic US Population
# usage: sudo bash CONFIGURE_CENTOS7.bash
#
# Load variables
. /etc/os-release

# these make centos easier for use. It's not necessary, and it increases bloat, but it's generally worth it.
yum -y install emacs screen git wget
# These are necessary
yum -y install yum-utils md5deep

# Bring the system up to date. Again, not necessary, but useful:
yum -y makecache fast
yum -y update



if test x$ID == x"amzn"; then
  sudo yum -y install python35 python35-devel python35-pip python35-setuptools python35-tools pythone5-virtualenv
  sudo pip-3.5 install numpy pandas ipython
else
  #
  # Install Python3.4 and necessary tools
  # See https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-centos-7
  sudo yum -y groupinstall development
  sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
  sudo yum -y install python36u
  sudo yum -y install python36u-pip
  sudo pip3.6 install numpy pandas ipython 
fi


# Note: We do not create a python36 virtual environment, but we probably should


# set up SSH access if not installed
if ! test -f $HOME/.ssh/id_rsa ; then
  ssh-keygen -t rsa -N "" -f $HOME/.ssh/id_rsa
  cp authorized_keys $HOME/.ssh/
  chmod 600 $HOME/.ssh/authorized_keys
fi

