from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from mezzanine.core.views import direct_to_template
from crm_core import views
from ajax_select import urls as ajax_select_urls


admin.autodiscover()


# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = \
    i18n_patterns(
        "",
        # Change the admin prefix here to use an alternate URL for the
        # admin interface, which would be marginally more secure.
        ('^admin/', include('smuggler.urls')),
        ("^admin/", include(admin.site.urls)),
        url(r'^dashboard/$', views.show_dashboard, name='dashboard'),
        url(r'^login/$', views.login_user, name='login'),
        url(r'^logout/$', views.login_user, name='logout'),
        url(r'^profileupdate/(?P<pk>\d+)/$', views.UpdateUserProfile.as_view(), name='profile_update'),
        url(r'^settings/$', views.show_settings, name='settings'),

        # #############
        # Customer urls
        # #############

        url(r'^customers/$', views.ListCustomers.as_view(), name='customer_list'),
        url(r'^customers/detail/(?P<pk>\d+)/$', views.ViewCustomer.as_view(), name='customer_detail'),
        url(r'^customers/create/$', views.CreateCustomer.as_view(), name='customer_create'),
        url(r'^customers/createcontract/(?P<customer_pk>\d+)/$', views.create_contract_from_customer,
            name='customer_create_contract'),
        url(r'^customers/edit/(?P<pk>\d+)/$', views.EditCustomer.as_view(), name='customer_edit'),
        url(r'^customers/delete/(?P<pk>\d+)/$', views.DeleteCustomer.as_view(), name='customer_delete'),

        # #############
        # Supplier urls
        # #############

        url(r'^suppliers/$', views.ListSuppliers.as_view(), name='supplier_list'),
        url(r'^suppliers/detail/(?P<pk>\d+)/$', views.ViewSupplier.as_view(), name='supplier_detail'),
        url(r'^suppliers/create/$', views.CreateSupplier.as_view(), name='supplier_create'),
        url(r'^suppliers/edit/(?P<pk>\d+)/$', views.EditSupplier.as_view(), name='supplier_edit'),
        url(r'^suppliers/delete/(?P<pk>\d+)/$', views.DeleteSupplier.as_view(), name='supplier_delete'),

        # ########
        # Tax urls
        # ########

        url(r'^taxes/create/$', views.CreateTax.as_view(), name='tax_create'),
        url(r'^taxes/edit/(?P<pk>\d+)/$', views.EditTax.as_view(), name='tax_edit'),
        url(r'^taxes/delete/(?P<pk>\d+)/$', views.DeleteTax.as_view(), name='tax_delete'),

        # #########
        # Unit urls
        # #########

        url(r'^units/create/$', views.CreateUnit.as_view(), name='unit_create'),
        url(r'^units/edit/(?P<pk>\d+)/$', views.EditUnit.as_view(), name='unit_edit'),
        url(r'^units/delete/(?P<pk>\d+)/$', views.DeleteUnit.as_view(), name='unit_delete'),

        # #####################
        # Product category urls
        # #####################

        url(r'^productcategory/create/$', views.CreateProductCategory.as_view(), name='productcategory_create'),
        url(r'^productcategory/edit/(?P<pk>\d+)/$', views.EditProductCategory.as_view(), name='productcategory_edit'),
        url(r'^productcategory/delete/(?P<pk>\d+)/$',
            views.DeleteProductCategory.as_view(), name='productcategory_delete'),

        # ############
        # Product urls
        # ############

        url(r'^products/$', views.ListProducts.as_view(), name='product_list'),
        url(r'^products/create/$', views.CreateProduct.as_view(), name='product_create'),
        url(r'^products/edit/(?P<pk>\d+)/$', views.EditProduct.as_view(), name='product_edit'),
        url(r'^products/delete/(?P<pk>\d+)/$', views.DeleteProduct.as_view(), name='product_delete'),

        # #################
        # BillingCycle urls
        # #################

        url(r'^billingcycles/create/$', views.CreateBillingCycle.as_view(), name='customerbillingcycle_create'),
        url(r'^billingcycles/edit/(?P<pk>\d+)/$', views.EditBillingCycle.as_view(), name='customerbillingcycle_edit'),
        url(r'^billingcycles/delete/(?P<pk>\d+)/$',
            views.DeleteBillingCycle.as_view(), name='customerbillingcycle_delete'),

        # ##################
        # Purchaseorder urls
        # ##################

        url(r'^purchaseorders/edit/(?P<pk>\d+)/$', views.EditPurchaseOrder.as_view(), name='purchaseorder_edit'),
        url(r'^purchaseorders/delete/(?P<pk>\d+)/$', views.DeletePurchaseOrder.as_view(), name='purchaseorder_delete'),
        url(r'^purchaseorders/detail/(?P<pk>\d+)/$', views.view_purchaseorder_details, name='purchaseorder_detail'),

        # ##################
        # CustomerGroup urls
        # ##################

        url(r'^customergroups/create/$', views.CreateCustomerGroup.as_view(), name='customergroup_create'),
        url(r'^customergroups/edit/(?P<pk>\d+)/$', views.EditCustomerGroup.as_view(), name='customergroup_edit'),
        url(r'^customergroups/delete/(?P<pk>\d+)/$', views.DeleteCustomerGroup.as_view(), name='customergroup_delete'),

        # #############
        # Contract urls
        # #############

        url(r'^contracts/$', views.ListContracts.as_view(), name='contract_list'),
        url(r'^contracts/detail/(?P<pk>\d+)/$', views.ViewContract.as_view(), name='contract_detail'),
        url(r'^contracts/create/$', views.CreateContract.as_view(), name='contract_create'),
        url(r'^contracts/createinvoice/(?P<contract_pk>\d+)/$', views.create_invoice_from_contract,
            name='contract_create_invoice'),
        url(r'^contracts/createquote/(?P<contract_pk>\d+)/$',
            views.create_quote_from_contract, name='contract_create_quote'),
        url(r'^contracts/createpurchaseorder/(?P<contract_pk>\d+)/$', views.create_purchaseorder_from_contract,
            name='contract_create_purchaseorder'),
        url(r'^contracts/edit/(?P<pk>\d+)/$', views.EditContract.as_view(), name='contract_edit'),
        url(r'^contracts/delete/(?P<pk>\d+)/$', views.DeleteContract.as_view(), name='contract_delete'),

        # ############
        # Invoice urls
        # ############

        url(r'^invoices/edit/(?P<pk>\d+)/$', views.EditInvoice.as_view(), name='invoice_edit'),
        url(r'^invoices/delete/(?P<pk>\d+)/$', views.DeleteInvoice.as_view(), name='invoice_delete'),
        url(r'^invoices/detail/(?P<pk>\d+)/$', views.view_invoice_details, name='invoice_detail'),

        # ##########
        # Quote urls
        # ##########

        url(r'^quotes/edit/(?P<pk>\d+)/$', views.EditQuote.as_view(), name='quote_edit'),
        url(r'^quotes/delete/(?P<pk>\d+)/$', views.DeleteQuote.as_view(), name='quote_delete'),
        url(r'^quotes/detail/(?P<pk>\d+)/$', views.view_quote_details, name='quote_detail'),
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

                         # Cartridge URLs.
                        url("^shop/", include("cartridge.shop.urls")),
                        url(r"^account/orders/$", "cartridge.shop.views.order_history", name="shop_order_history"),

                        url("^", include("mezzanine.urls")),
)

try:
    import ajax_select
    # If django-ajax-selects is installed, include its URLs:
    urlpatterns += patterns('',
                            url(r'^admin/lookups/', include(ajax_select_urls)),
    )
except ImportError:
    pass

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
