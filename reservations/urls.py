from django.conf.urls import url, patterns

from reservations.views import ReservableProductEditView, ReservableReservationsListView, \
    ReservationEditView, ReservableSearchView, DateRangeCheckView

urlpatterns = patterns(
    '',
    url(r"^reservable/check_period/$", DateRangeCheckView.as_view(), name="check_period"),

    url(r"^reservable/search/$", ReservableSearchView.as_view(), name="reservable.search"),

    url(
        r"^sa/products/(?P<pk>\d+)/$", ReservableProductEditView.as_view(),
        name="product.edit"
    ),

    url(
        r'^sa/reservable/(?P<reservable>\d+)/reservations/new/',
        ReservationEditView.as_view(), name="product.reservations.new"),

    url(
        r'^sa/reservable/(?P<reservable>\d+)/reservations/(?P<pk>\d+)/',
        ReservationEditView.as_view(), name="product.reservations.edit"),

    url(
        r'^sa/reservable/(?P<pk>\d+)/reservations/',
        ReservableReservationsListView.as_view(), name="product.reservations"),
)
