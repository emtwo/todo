#!/bin/sh

set -e

flask db upgrade

gunicorn -b 0.0.0.0:5000 app.app:app