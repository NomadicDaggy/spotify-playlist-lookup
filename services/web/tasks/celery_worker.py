from app import create_app
from tasks import celery


app = create_app()
app.app_context().push()
