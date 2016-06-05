Peereesook Control Panel
------------------------
this is a framework to Centralized Management for distributed system. 
this framework use build via [pyramid](docs.pylonsproject.org/en/latest/docs/pyramid.html) framework on top of [saltmaster](https://docs.saltstack.com/en/getstarted/).

Getting Started
---------------
- create virtual env and activate it

- cd <directory containing this file>

- $VENV/bin/pip install -e .

- $VENV/bin/initialize_peecp_db development.ini 

- $VENV/bin/pserve development.ini

Configuration Saltstack
-----------------------
At now peereesook control panel use salt-api to connect saltstack and it may change to [pepper](https://github.com/saltstack/pepper).
to use salt-api install it ang add the fallowing config to salt:
.. code-block:: bash
    rest_cherrypy:
        port: 8080
        disable_ssl: True
        host: 0.0.0.0

and add user with username admin in os and add the following config to add access for this user:
.. code-block:: bash
  external_auth:
    pam:
      admin:
        - .*