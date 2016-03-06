from django.conf.urls import url, patterns

from reservations.views import (
    ReservableProductEditView, ReservationEditView, ReservableSearchView, DateRangeCheckView,
    ReservationsAdminList)


urlpatterns = patterns(
    '',
    url(r"^reservations/check_period/$", DateRangeCheckView.as_view(), name="check_period"),

    url(r"^reservations/$", ReservableSearchView.as_view(), name="reservable.search"),

    url(
        r"^sa/products/(?P<pk>\d+)/$", ReservableProductEditView.as_view(),
        name="product.edit"
    ),
)
