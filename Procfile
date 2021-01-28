web: gunicorn config.wsgi
worker: REMAP_SIGTERM=SIGQUIT celery -A config worker -B --loglevel=info