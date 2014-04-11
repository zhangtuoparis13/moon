#!/bin/bash

unset http_proxy

bash .doc/set_sshtunnel.sh

python manage.py runserver 0.0.0.0:8080