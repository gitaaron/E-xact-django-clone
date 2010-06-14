from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^exact_clone/', include('exact_clone.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Media files (only for development)
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', \
                    {'document_root': '%s/site_media' 
                     % settings.APPLICATION_ROOT}),

    # Shop assets uploaded via admin (only for development)
    (r'^assets/(?P<path>.*)$', 'django.views.static.serve', \
                    {'document_root': '%s/assets' 
                     % settings.APPLICATION_ROOT}),



    (r'^$', direct_to_template, {'template': 'index.html'}),
    (r'^category/(?P<primary_slug>[-\w]+)$', 'exact_clone.gallery.views.index'),
    (r'^category/(?P<primary_slug>[-\w]+)/(?P<secondary_slug>[-\w]+)$', 'exact_clone.gallery.views.index'),
    (r'^show/(?P<photo_slug>[-\w]+)$', 'exact_clone.gallery.views.detail'),
    (r'^shop/display_cart$', 'exact_clone.shop.views.display_cart'),
    (r'^shop/display_order/(?P<order_id>\d+)$', 'exact_clone.shop.views.display_order'),
    (r'^shop/add_item$', 'exact_clone.shop.views.add_item'),
    (r'^shop/checkout$', 'exact_clone.shop.views.checkout'),
    (r'^shop/empty_cart$', 'exact_clone.shop.views.empty_cart'),
)
