from django.conf.urls import url, patterns
from django.views.decorators.csrf import csrf_exempt

from reservations.views import ReservableProductDetailView, ReservableProductEditView, ReservableReservationsListView, \
    ReservationEditView

urlpatterns = patterns(
    '',
    # override Shoop ProductDetailView with our own
    url(r'^p/(?P<pk>\d+)-(?P<slug>.*)/$', csrf_exempt(ReservableProductDetailView.as_view())),

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
