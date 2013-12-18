# -*- coding: utf-8 -*-

__about__ = """
In addition to what is provided by the "zero" project, this project
provides thorough integration with django-user-accounts, adding
comprehensive account management functionality. It is a foundation
suitable for most sites that have user accounts.
"""

from south.signals import post_migrate


def update_permissions_after_migration(app, **kwargs):
    """
    Update app permission just after every migration.
    This is based on app django_extensions update_permissions management
    command.
    """
    from django.conf import settings
    from django.db.models import get_app, get_models
    from django.contrib.auth.management import create_permissions

    create_permissions(get_app(app), get_models(), 2 if settings.DEBUG else 0)


post_migrate.connect(update_permissions_after_migration)
