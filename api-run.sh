#! /usr/bin/env bash
source env/bin/activate
chmod +x setup.sh
./setup.sh
flask run --reload