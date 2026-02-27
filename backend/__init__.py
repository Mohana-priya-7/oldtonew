from .celery import app as celery_app 
__all__ = ['celery_app']

#Ensures Celery starts whenever Django starts.Without this:Celery may not load tasks.Django + Celery won’t sync properly