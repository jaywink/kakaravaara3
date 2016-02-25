import datetime

from dateutil import relativedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client
from django.utils.translation import activate
from freezegun import freeze_time
from shoop.xtheme import set_current_theme

from kakaravaara.tests import KakaravaaraTestsBase
from reservations.factories import ReservableProductFactory, ReservationFactory


class ReservableViewsBaseTestCase(KakaravaaraTestsBase):
    def setUp(self):
        super(ReservableViewsBaseTestCase, self).setUp()
        activate("en")
        set_current_theme("shoop_simple_theme")
        self.client = Client()


@freeze_time("2015-12-15")
class ReservableSearchViewTestCase(ReservableViewsBaseTestCase):
    def setUp(self):
        super(ReservableSearchViewTestCase, self).setUp()
        self.reservable = ReservableProductFactory()
        self.today = datetime.date.today()
        self.now = datetime.time(15)
        self.next = self.today + relativedelta.relativedelta(months=1)
        self.reservation = ReservationFactory(
            reservable=self.reservable,
            start_time=datetime.datetime.combine(self.today, self.now),
            end_time=datetime.datetime.combine(self.today + datetime.timedelta(days=3), self.now)
        )
        self.response = self.client.get(reverse('reservations:reservable.search'))

    def test_view_responds(self):
        self.assertContains(self.response, u"Select months to search from")

    def test_context_data(self):
        context = self.response.context_data
        self.assertEqual(list(context["reservables"]), [self.reservable])
        self.assertEqual(context["start_month"], self.today.strftime("%m/%Y"))
        self.assertEqual(context["end_month"], self.next.strftime("%m/%Y"))
        self.assertEqual(
            context["start_date"],
            (self.today + relativedelta.relativedelta(day=1)).strftime("%Y-%m-%d %H:%M")
        )
        self.assertEqual(
            context["end_date"],
            (self.today + relativedelta.relativedelta(day=1, months=+2, days=-1)).strftime("%Y-%m-%d %H:%M")
        )
        self.assertEqual(context["reserved_days"], {
            self.reservable.product.sku: [
                self.today.strftime("%Y-%m-%d"),
                (self.today + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                (self.today + datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            ]
        })
        self.assertEqual(context["visible_attributes"], settings.RESERVABLE_SEARCH_VISIBLE_ATTRIBUTES)
        self.assertEqual(
            context["months"],
            [
                self.today.strftime("%Y-%m"),
                (self.today + relativedelta.relativedelta(months=1)).strftime("%Y-%m"),
            ]
        )
