#!/bin/bash

unset http_proxy

bash .doc/set_sshtunnel.sh

python moon.py --run runserver 0.0.0.0:8080