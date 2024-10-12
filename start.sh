#!/bin/bash
source venv/bin/activate  # If you are using a virtual environment
gunicorn app:app --bind 0.0.0.0:10000  # Replace 'app' with your Flask app module name
