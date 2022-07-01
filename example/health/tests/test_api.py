from unittest.mock import patch

import pytest
from django.db import DatabaseError
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from example.health.api.views import ServiceHealthCheckError


@pytest.mark.django_db
def test_healthz_success(client: APIClient, settings):
    """Test happy path."""
    response = client.get(reverse('api-health:health'))

    assert response.status_code == status.HTTP_200_OK
    assert response.data == 'ok'


@pytest.mark.django_db
def test_healthz_postgres_unavailable(client: APIClient, settings):
    """Test health endpoint when Postgres is unavailable."""
    exc = DatabaseError('test_error')
    with patch('django.db.connection.cursor', side_effect=exc):
        response = client.get(reverse('api-health:health'))

    assert response.status_code == ServiceHealthCheckError.status_code

    msg = response.json()
    assert msg == {'postgres': 'test_error'}
