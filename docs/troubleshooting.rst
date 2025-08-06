Issues & Troubleshooting
========================

Mac OS Installation
===================

Docker/Database Issues
----------------------

Make sure Docker is installed:

Download the dmg installer from:
https://docs.docker.com/desktop/setup/install/mac-install/

### Database: `mariadb_config` error

Sometimes the plugin isn't properly set up or can't be found.

Check:

.. code-block:: bash

   which mariadb

If no path is displayed:

1. Install the connector:

   .. code-block:: bash

      brew install mariadb-connector-c

2. Add missing paths:

**For Intel:**

.. code-block:: bash

   export PATH="/usr/local/opt/mariadb-connector-c/bin:$PATH"
   export CPPFLAGS="-I/usr/local/opt/mariadb-connector-c/include"
   export LDFLAGS="-L/usr/local/opt/mariadb-connector-c/lib"
   export MARIADB_CONFIG=/usr/local/opt/mariadb-connector-c/bin/mariadb_config

**For Apple Silicon:**

.. code-block:: bash

   export PATH="/opt/homebrew/opt/mariadb-connector-c/bin:$PATH"
   export CPPFLAGS="-I/opt/homebrew/opt/mariadb-connector-c/include"
   export LDFLAGS="-L/opt/homebrew/opt/mariadb-connector-c/lib"
   export MARIADB_CONFIG=/opt/homebrew/opt/mariadb-connector-c/bin/mariadb_config

3. Manually install MariaDB Python bindings:

   .. code-block:: bash

      pip install mariadb

4. Update your shell environment:

   .. code-block:: bash

      source ~/.zshrc

Linux Installation
==================

Prerequisite Libraries/Plugins
------------------------------

These are not installed by default, so it is helpful to ensure all Python tools are available:

.. code-block:: bash

   sudo apt update
   sudo apt install software-properties-common -y
   sudo add-apt-repository ppa:deadsnakes/ppa -y
   sudo apt update
   sudo apt install -y python3-dev python3-pip python3-venv build-essential
   sudo apt install python3.11 python3.11-venv python3.11-dev -y

Install GCC:

.. code-block:: bash

   sudo apt install build-essential -y

### Database: `mariadb_config` error

.. code-block:: bash

   sudo apt install libmariadb-dev -y

Check:

.. code-block:: bash

   mariadb_config --cflags
   mariadb_config --libs

Docker Issues
-------------

After installing Docker, if you get a permissions error when running `dt-db up`:

1.

.. code-block:: bash

   sudo groupadd docker

2.

.. code-block:: bash

   sudo usermod -aG docker $USER

3.

.. code-block:: bash

   newgrp docker

4. Verify Docker is working:

.. code-block:: bash

   docker ps

---

Thank you for helping us improve the project!
