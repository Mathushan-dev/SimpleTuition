from main import app as asgi_app

# Backwards-compatible entrypoint for hosting platforms that expect
# a top-level `app` module. We expose both an ASGI `asgi_app` and a
# WSGI `app` (wrapped via AsgiToWsgi) so either a sync Gunicorn worker
# or an ASGI-capable worker can run the service.

try:
	from asgiref.wsgi import AsgiToWsgi
	app = AsgiToWsgi(asgi_app)
except Exception:
	# If asgiref isn't available for any reason, fall back to exposing
	# the ASGI app directly. ASGI workers will still work.
	app = asgi_app

# Also expose the ASGI app explicitly for ASGI workers/configs
asgi_app = asgi_app

