import pytest
from django.test import TestCase

from shoop.testing.factories import get_default_shop


@pytest.mark.django_db
class KakaravaaraTestsBase(TestCase):
    def setUp(self):
        super(KakaravaaraTestsBase, self).setUp()
        # Ensure a shop exists
        self.shop = get_default_shop()
