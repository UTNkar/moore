from django.conf.urls import url

from involvement import views

urlpatterns = [
    url(r'^admin/involvement/position/elect/(\d+)/$', views.admin_approve_applicants,
        name='involvement_position_modeladmin_elect'),
    url(r'^admin/involvement/position/appoint/(\d+)/$', views.admin_appoint,
        name='involvement_position_modeladmin_appoint'),
]
