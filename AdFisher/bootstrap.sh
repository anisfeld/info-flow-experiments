#!/bin/bash

# NOTE: this is written for Ubuntu 14.04. Will not work as written on later versions

### Install os dependencies
apt-get update

# Install gui
apt-get install -y ubuntu-desktop gnome-session-flashback

# Required for browsing
apt-get install -y firefox

# Required for headless testing
apt-get install -y xvfb


# Required for data analysis
apt-get install -y python-numpy python-scipy python-matplotlib

# Requiured for python dependencies
apt-get install -y python-pip python-dev

# Required for pyre2 dependencies
apt-get install -y git build-essential
cd ~
git clone https://code.googlesource.com/re2
cd re2
make test
sudo make install


### Install python dependencies
sudo pip install -r /vagrant/requirements.txt

# Fetch nltk stopwords corpus
python -m nltk.downloader -d /usr/share/nltk_data stopwords

# need to drive firefox with selenium
apt-get install -y firefox-geckodriver



# on Ubuntu 20. pip is not available through apt-get
# apt-get install -y python2
# https://stackoverflow.com/questions/61981156/unable-to-locate-package-python-pip-ubuntu-20-04
# apt-get install -y curl
# curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
# sudo python ./get-pip.py
