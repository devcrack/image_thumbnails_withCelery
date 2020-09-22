from .celery import celery_app

"""
At this way we ensure that the previous created and configured celery application gets injected into Django application when it's Ran.
Impot the celery application within the django projects main __init__ (this file) script and explicitly registering it as a namespaced 
symbol within the "image_parroter" django package 
"""

__all__ = ('celery_app')

