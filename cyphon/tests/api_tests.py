# -*- coding: utf-8 -*-
# Copyright 2017-2018 Dunbar Security Solutions, Inc.
#
# This file is part of Cyphon Engine.
#
# Cyphon Engine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Cyphon Engine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cyphon Engine. If not, see <http://www.gnu.org/licenses/>.
"""
Provides a base class for testing views for REST API endpoints.
"""

# third party
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase

# local
from appusers.models import AppUser

API_URL = settings.API_URL


def settings_exist(settings):
    """
    Takse a dict of settings and returns a Boolean indicating whether
    all settings have value.
    """
    settings_exist = True
    for key, val in settings.items():
        if not val:
            settings_exist = False
    return settings_exist


class PassportMixin(object):
    """
    Supplies valid credentials to a Passport used in API tests.
    """

    @staticmethod
    def _update_passport(passport, settings):
        """
        Supplies valid credentials to a Passport used in tests.
        """
        passport.key = settings.get('KEY', '')
        passport.secret = settings.get('SECRET', '')
        passport.access_token = settings.get('ACCESS_TOKEN', '')
        passport.access_token_secret = settings.get('ACCESS_TOKEN_SECRET', '')
        passport.save()
        return passport


class APITestMixin(object):
    """

    """

    model_url = ''

    def authenticate(self, is_staff=True):
        """
        Forces authentication and returns a response in the specified format.
        """
        self.user.is_staff = is_staff
        self.user.save()
        return self.client.force_authenticate(user=self.user)

    def get_api_response(self, endpoint='', is_staff=True, authenticate=True):
        """

        """
        url = self.url + endpoint
        if authenticate:
            self.authenticate(is_staff=is_staff)
        return self.client.get(url, format='json')

    def post_to_api(self, endpoint, data, is_staff=True, authenticate=True):
        """

        """
        url = self.url
        if endpoint:
            url += endpoint
        if authenticate:
            self.authenticate(is_staff=is_staff)
        return self.client.post(url, data, format='json')

    def patch_to_api(self, endpoint, data, is_staff=True, authenticate=True):
        """

        """
        url = self.url
        if endpoint:
            url += endpoint
        if authenticate:
            self.authenticate(is_staff=is_staff)
        return self.client.patch(url, data, format='json')

    def test_unauthorized_access(self):
        """
        Ensures authentication for the REST API endpoint.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CyphonAPITestCase(APITestCase, APITestMixin):
    """
    Tests REST API endpoints.
    """

    def __init__(self, *args, **kwargs):
        super(CyphonAPITestCase, self).__init__(*args, **kwargs)
        self.url = API_URL + self.model_url

    def setUp(self, *args, **kwargs):
        # super(CyphonAPITestCase, self).setUp(*args, **kwargs)
        try:
            user = AppUser.objects.get(email='test@test.com')
            user.delete()
        except ObjectDoesNotExist:
            pass

        self.user = AppUser.objects.create_user(
            email='test@test.com',
            password='test'
        )


class CyphonAPITransactionTestCase(APITransactionTestCase, APITestMixin):
    """
    Tests REST API endpoints using transactions.
    """

    def __init__(self, *args, **kwargs):
        super(CyphonAPITransactionTestCase, self).__init__(*args, **kwargs)
        self.url = API_URL + self.model_url

    def setUp(self, *args, **kwargs):
        # super(CyphonAPITransactionTestCase, self).setUp(*args, **kwargs)
        try:
            user = AppUser.objects.get(email='test@test.com')
            user.delete()
        except ObjectDoesNotExist:
            pass

        self.user = AppUser.objects.create_user(
            email='test@test.com',
            password='test'
        )
