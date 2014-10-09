from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import TemplateView
from mezzanine.core.views import direct_to_template
from crm.views import *

admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = i18n_patterns("",
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),
    url("^admin/backup/$", "admin_backup.views.admin_backup", name="admin_backup"),
    # url(r'^calendar/', include('calendarium.urls')),
    url(r'^login/$', TemplateView.as_view(template_name='login.html')),
    url(r'^logout/$', TemplateView.as_view(template_name='login.html')),
    # (r'^todo/', include('todo.urls')),

    url(r"^customers/$", ListCustomers.as_view(), name='list_customers'),
    url(r'^customers/create/$', CreateCustomer.as_view(), name='create_customer'),
    url(r'^customers/edit/(?P<pk>\d+)/$', EditCustomer.as_view(), name='edit_customer'),
    url(r'^customers/delete/(?P<pk>\d+)/$', DeleteCustomer.as_view(), name='delete_customer'),
    url(r"^suppliers/$", ListSuppliers.as_view(), name='list_suppliers'),
    url(r'^suppliers/create/$', CreateSupplier.as_view(), name='create_supplier'),
    url(r'^suppliers/edit/(?P<pk>\d+)/$', EditSupplier.as_view(), name='edit_supplier'),
    url(r'^suppliers/delete/(?P<pk>\d+)/$', DeleteSupplier.as_view(), name='delete_supplier'),
    url(r"^currencies/$", ListCurrencies.as_view(), name='list_currencies'),
    url(r'^currencies/create/$', CreateCurrency.as_view(), name='create_currency'),
    url(r'^currencies/edit/(?P<pk>\d+)/$', EditCurrency.as_view(), name='edit_currency'),
    url(r'^currencies/delete/(?P<pk>\d+)/$', DeleteCurrency.as_view(), name='delete_currency'),
    url(r"^taxes/$", ListTaxes.as_view(), name='list_taxes'),
    url(r'^taxes/create/$', CreateTax.as_view(), name='create_tax'),
    url(r'^taxes/edit/(?P<pk>\d+)/$', EditTax.as_view(), name='edit_tax'),
    url(r'^taxes/delete/(?P<pk>\d+)/$', DeleteTax.as_view(), name='delete_tax'),
    url(r"^units/$", ListUnits.as_view(), name='list_units'),
    url(r'^units/create/$', CreateUnit.as_view(), name='create_unit'),
    url(r'^units/edit/(?P<pk>\d+)/$', EditUnit.as_view(), name='edit_unit'),
    url(r'^units/delete/(?P<pk>\d+)/$', DeleteUnit.as_view(), name='delete_unit'),
)

urlpatterns += patterns('',

    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # HOMEPAGE AS STATIC TEMPLATE
    # ---------------------------
    # This pattern simply loads the index.html template. It isn't
    # commented out like the others, so it's the default. You only need
    # one homepage pattern, so if you use a different one, comment this
    # one out.

    url("^$", direct_to_template, {"template": "index.html"}, name="home"),

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "/", which
    # is the value used below in the ``{"slug": "/"}`` part.
    # Also note that the normal rule of adding a custom
    # template per page with the template name using the page's slug
    # doesn't apply here, since we can't have a template called
    # "/.html" - so for this case, the template "pages/index.html"
    # should be used if you want to customize the homepage's template.

    # url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.
    ("^", include("mezzanine.urls")),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
