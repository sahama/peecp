Peereesook Control Panel
========================
this is a framework to Centralized Management for distributed system. 
this framework use build via `pyramid <http://docs.pylonsproject.org/en/latest/docs/pyramid.html>`_ on top of `saltmaster <https://docs.saltstack.com/en/getstarted/>`_.

Getting Started
---------------
- create virtual env and activate it

- cd <directory containing this file>

- $VENV/bin/pip install -e .

- $VENV/bin/initialize_peecp_db development.ini 

- $VENV/bin/pserve development.ini

Configuration SaltStack Minions
---------------------
in minions create /etc/salt/minion.d/master.conf add this line
- master: <YOUR SALT MASTER IP>
for example
- master: 127.0.0.1

and restart minion service via
- service salt-minion restart

add minion key to master in master
- salt-key -A

and accept all keys

Configuration Saltstack Master
-----------------------
At now peereesook control panel use salt-api to connect saltstack and it may change to `pepper <https://github.com/saltstack/pepper>`_.
to use salt-api install it ang add the fallowing config to salt.
.. code:: yaml
    rest_cherrypy:
        port: 8080
        disable_ssl: True
        host: 0.0.0.0

and add user with username admin in os and add the following config to add access for this user.
.. code:: yaml
    external_auth:
        pam:
            admin:
                - .*


Adding user
-----------
in your OS (tested on debian GNU/Linux 8) add admin user
- adduser admin
and set password for this user.

now you can login to peecp via this user and password.