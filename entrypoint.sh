#!/bin/bash
exec gunicorn --config /app/gunicorn_config.py src.app:app