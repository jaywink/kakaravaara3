import datetime

from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.utils.translation import ugettext

from shoop.core.models import OrderLineType
from shoop.front.signals import order_creator_finished
from shoop.notify import Event, Variable
from shoop.notify.typology import Email, Language, Model, Phone, Text, Decimal, Integer, URL
from shoop.utils.dates import parse_date


class ReservationsOrderReceived(Event):
    identifier = "reservations_order_received"

    order = Variable("Order", type=Model("shoop.Order"))
    order_id = Variable("Order ID", type=Integer)
    order_details = Variable("Order Details", type=Text)
    order_url = Variable("Order URL", type=URL)
    customer_email = Variable("Customer Email", type=Email)
    customer_phone = Variable("Customer Phone", type=Phone)
    customer_name = Variable("Customer Name", type=Text)
    language = Variable("Language", type=Language)
    additional_notes = Variable("Additional Notes", type=Text)
    total_sum = Variable("Total Sum", type=Decimal)


def get_order_details(order):
    details = []
    for line in order.lines.filter(type=OrderLineType.PRODUCT):
        details.append("%s" % line.text)
        if line.product.type.identifier == "reservable":
            start = parse_date(line.extra_data["reservation_start"])
            end = start + datetime.timedelta(days=int(line.quantity))
            details.append(ugettext("    %s nights, %s persons, %s - %s" % (
                int(line.quantity), line.extra_data["persons"], start, end
            )))
    return "\n".join(details)


@receiver(order_creator_finished)
def send_order_received_notification(order, **kwargs):
    ReservationsOrderReceived(
        order=order,
        order_id=order.id,
        order_details=get_order_details(order),
        order_url=reverse("shoop:show-order", kwargs={"pk": order.pk}),
        customer_email=order.email,
        customer_phone=order.phone,
        customer_name=order.billing_address.name if order.billing_address else "",
        language=order.language,
        additional_notes=order.customer_comment,
        total_sum=order.taxful_total_price_value,
    ).run()
