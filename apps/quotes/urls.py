from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="dashboard"),
    url(r'^create$', views.create, name="create_quote"),
    url(r'^showuser/(?P<userid>[0-9]+)$', views.show_user, name="show"),
    url(r'^addfave/(?P<quote_id>[0-9]+)$', views.add_favorite, name="add_favorite"),
    url(r'^remfave/(?P<quote_id>[0-9]+)$', views.delete_favorite, name="delete_favorite"),
]
