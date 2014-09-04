from django.conf.urls import patterns, include, url

urlpatterns = patterns('zircon.frontend.dashboard.views',

    url(r'^$', 'home', name='home'),
)
