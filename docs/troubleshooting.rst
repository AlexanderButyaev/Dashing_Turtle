Issues & Troubleshooting
========================

====================
##### MAC OS INSTALLATION ######
====================

Docker/Database Issues
==============

Make sure Docker is installed:

Download the dmg installer from:
docker: https://docs.docker.com/desktop/setup/install/mac-install/

Database: mariadb_config error
----------------------
Sometimes the plug in isnt properly set up or can't be found.

check:
which mariadb

If no path is displayed:

1) brew install mariadb-connector-c

2) Add missing paths

Add these to path (Intel)
export PATH="/usr/local/opt/mariadb-connector-c/bin:$PATH"
export CPPFLAGS="-I/usr/local/opt/mariadb-connector-c/include"
export LDFLAGS="-L/usr/local/opt/mariadb-connector-c/lib"
MARIADB_CONFIG=/usr/local/opt/mariadb-connector-c/bin/mariadb_config

Add these to path (Silicon)
export PATH="/opt/homebrew/opt/mariadb-connector-c/bin:$PATH"
export CPPFLAGS="-I/opt/homebrew/opt/mariadb-connector-c/include"
export LDFLAGS="-L/opt/homebrew/opt/mariadb-connector-c/lib"
MARIADB_CONFIG=/opt/homebrew/opt/mariadb-connector-c/bin/mariadb_config

3) Manually install mariadb

pip install mariadb

4) Update shell

source ~/.zshrc


====================
##### LINUX INSTALLATION ######
====================

Prerequisite Libraries/Plugins
==============

These are not installed by default so it is helpful to ensure all the python tools are installed:

sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt update
sudo apt install -y python3-dev python3-pip python3-venv build-essential
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y

GCC
sudo apt install build-essential -y


Database: mariadb_config error
==============

sudo apt install libmariadb-dev -y

#check
mariadb_config --cflags
mariadb_config --libs

Docker Issues
==============

After installing Docker if there is a permissions error when running dt-db up:

1) sudo groupadd docker
2) sudo usermod -aG docker $USER
3) newgrp docker
4) Verify: docker ps

---

Thank you for helping us improve the project!
