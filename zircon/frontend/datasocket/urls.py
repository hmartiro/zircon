from django.conf.urls import patterns, include, url

from socketio import sdjango
sdjango.autodiscover()

urlpatterns = patterns('zircon.frontend.datasocket.views',

    url('', include(sdjango.urls)),
)
