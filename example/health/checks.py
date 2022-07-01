from typing import Callable

from django.conf import settings
from django.db import connection
from django.utils.module_loading import import_string


def postgres():
    """Checks PostgreSQL connection state."""
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
        res = cursor.fetchone()[0]
        if res != 1:
            raise RuntimeError('Unable to communicate with Postgres')


class ChecksConf:
    """All avaialable health checks config."""

    _all_checks: set[Callable[[], None]] = set()

    def load_checks(self, dotted_checks):
        """Loads all specified health checks from the list `dotted_checks.

        :param dotted_checks: list of dotted paths.
        """
        for dotted_path in dotted_checks:
            callable_obj = import_string(dotted_path)
            assert callable(callable_obj)
            self._all_checks.add(callable_obj)

    @property
    def all_checks(self) -> set[Callable[[], None]]:
        """Returns all available health checks.

        :return: set of callable health checks.
        """
        return self._all_checks


checks_conf = ChecksConf()
checks_conf.load_checks(settings.HEALTH_CHECKS)
