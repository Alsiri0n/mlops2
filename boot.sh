#!/bin/bash
source venv/bin/activate
exec gunicorn -b :$FLASK_RUN_PORT --access-logfile - --error-logfile - run:app
