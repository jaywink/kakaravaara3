# Kakaravaara v3

[![Stories in Ready](https://badge.waffle.io/jaywink/kakaravaara3.png?label=ready&title=Ready)](https://waffle.io/jaywink/kakaravaara3) [![Build Status](https://travis-ci.org/jaywink/kakaravaara3.svg?branch=master)](https://travis-ci.org/jaywink/kakaravaara3) [![Code Health](https://landscape.io/github/jaywink/kakaravaara3/master/landscape.svg?style=flat)](https://landscape.io/github/jaywink/kakaravaara3/master) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/jaywink/kakaravaara3/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/jaywink/kakaravaara3/?branch=master) [![Requirements Status](https://requires.io/github/jaywink/kakaravaara3/requirements.svg?branch=master)](https://requires.io/github/jaywink/kakaravaara3/requirements/?branch=master) [![codecov.io](https://codecov.io/github/jaywink/kakaravaara3/coverage.svg?branch=master)](https://codecov.io/github/jaywink/kakaravaara3?branch=master)

Rewrite, again, this time with [Shoop](https://shoop.io).

## Initial data

After running `shoop_init` management command, the following needs done:

* Creation of a CMS page with the identifier `index`.
* Creation of a `ProductType` with identifier `reservable`. The identifier can only be set via the DB.
* Enable `Shoop Simple Theme`.
* Enable `Default Payment Method`.
* Enable `Default Shipping Method`.
* Set `Default Supplier` module to `Simple Supplier`.

## Products

Each product must have a supplier, for example `Default Supplier`. If the admin is broken:

    s = Supplier.objects.first()
    s.shop_products.add(ShopProduct.objects.get(product__sku=<sku>))

## License

AGPLv3 - https://www.tldrlegal.com/l/agpl3
