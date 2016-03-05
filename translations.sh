#!/usr/bin/env bash

if [[ $1 == "extract" ]]; then
    pybabel extract kakaravaara reservable_pricing reservations -o locale/django.pot -F babel.ini
    pybabel update -i locale/django.pot -D django -d locale -l fi
    python manage.py shoop_makemessages -l fi
elif [[ $1 == "compile" ]]; then
    pybabel compile -D django -d locale --statistics -l fi
else
    echo "Please give a command, either: extract, compile"
    exit 1
fi
