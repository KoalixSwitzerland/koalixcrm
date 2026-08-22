# -*- coding: utf-8 -*-
"""Grant (or revoke) unrestricted service-account status for a Django user.

koalixcrm#432. ``core.ServiceAccountGrant`` is the sole signal
``koalixcrm.core.access.is_unrestricted_actor`` reads for non-superusers, and
it is written **only** administratively — through the superuser-only admin or
this command. It is deliberately NOT wired into the container entrypoint or
any authentication path: auto-granting the system's widest authority on every
startup is precisely the property this model exists to remove.

Typical bootstrap, once per environment, after the M2M client has
authenticated at least once (which is what auto-provisions its Django user)::

    python manage.py grant_service_account

With no argument the username defaults to ``settings.CELERY_WORKER_M2M_CLIENT_ID``,
which is the username ``koalixcrm/auth/m2m_authentication.py`` provisions the
service user under.
"""
from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from koalixcrm.core.models.service_account_grant import ServiceAccountGrant

UserModel = get_user_model()


class Command(BaseCommand):
    help = 'Grant or revoke unrestricted service-account status for a Django user.'

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument(
            'username',
            nargs='?',
            default=None,
            help=(
                'Username of the service user. Defaults to '
                'settings.CELERY_WORKER_M2M_CLIENT_ID.'
            ),
        )
        parser.add_argument(
            '--revoke',
            action='store_true',
            help='Remove the grant instead of creating it.',
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List the users that currently hold a grant, and exit.',
        )

    def handle(self, *args: Any, **options: Any) -> None:
        if options['list']:
            self._list()
            return

        username = options['username'] or getattr(settings, 'CELERY_WORKER_M2M_CLIENT_ID', None)
        if not username:
            raise CommandError(
                'No username given and settings.CELERY_WORKER_M2M_CLIENT_ID is unset.'
            )

        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # Deliberately not auto-created: this command grants authority, it
            # does not mint identities. The M2M user appears on the client's
            # first authenticated call.
            raise CommandError(
                f'No Django user named {username!r}. The M2M service user is '
                f'auto-provisioned on the first successful token exchange — '
                f'run the client once, then re-run this command.'
            ) from None

        if options['revoke']:
            deleted, _ = ServiceAccountGrant.objects.filter(user=user).delete()
            if deleted:
                self.stdout.write(self.style.SUCCESS(f'Revoked service-account grant for {username!r}.'))
            else:
                self.stdout.write(f'{username!r} held no service-account grant — nothing to do.')
            return

        _grant, created = ServiceAccountGrant.objects.get_or_create(user=user)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Granted service-account status to {username!r}.'))
        else:
            self.stdout.write(f'{username!r} already holds a service-account grant.')

    def _list(self) -> None:
        grants = ServiceAccountGrant.objects.select_related('user').order_by('user__username')
        if not grants:
            self.stdout.write('No service-account grants exist.')
            return
        self.stdout.write('Users holding an unrestricted service-account grant:')
        for grant in grants:
            self.stdout.write(f'  {grant.user.get_username()}  (granted {grant.created_at:%Y-%m-%d %H:%M})')
