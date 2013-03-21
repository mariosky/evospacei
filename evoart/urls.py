from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


from shapes.views import  logout_view,\
    home, evospace, facebook_get_login,facebook_login, individual_view,\
    add_collection, get_user_collections, add_ind_to_col, get_collection,\
    dashboard


urlpatterns = patterns('',

	#url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	#url(r'^admin/', include(admin.site.urls)),
	#url(r'^twitter/login/?$', twitter_login),
	url(r'^twitter/logout/?$', logout_view),
    #url(r'^twitter/login/authenticated/?$', twitter_authenticated),

    url(r'^facebook/get_login/?$', facebook_get_login),
    url(r'^facebook/login/?$', facebook_login),
    url(r'^logout/?$', logout_view),


    url(r'^$', home),
    #url(r'^individual/(.+:.+:\d+)/$', individual_view),
    url(r'^individual/(\d+)/$', individual_view),
    url(r'^EvoSpace/?$', evospace),
    url(r'^add_collection/(\d+)/$', add_collection),
    url(r'^get_user_collections/(\d+)/$', get_user_collections),
    url(r'^add_ind_to_col/(\d+)/$', add_ind_to_col),
    url(r'^get_collection/(\d+)/(\d+)$', get_collection),
    url(r'^get_collection/(\d+)/$', get_collection),

    url(r'^dashboard/$', dashboard),
	

    # Examples:
    # url(r'^$', 'evoart.views.home', name='home'),
    # url(r'^evoart/', include('evoart.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
