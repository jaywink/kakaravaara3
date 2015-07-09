from django.conf.urls import url, patterns
from django.views.decorators.csrf import csrf_exempt

from reservations.views import ReservableProductDetailView, ReservableProductEditView

urlpatterns = patterns(
    '',
    # override Shoop ProductDetailView with our own
    url(r'^p/(?P<pk>\d+)-(?P<slug>.*)/$', csrf_exempt(ReservableProductDetailView.as_view())),

    url(
        r"^sa/products/(?P<pk>\d+)/$", ReservableProductEditView.as_view(),
        name="product.edit"
    ),
)
