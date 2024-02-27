from django.conf.urls import re_path

from involvement import views

urlpatterns = [
    re_path(
        r'^involvement/position/elect/(\d+)/$',
        views.admin_approve_applicants,
        name='involvement_position_modeladmin_approve'
    ),
    re_path(
        r'^involvement/position/appoint/(\d+)/$',
        views.admin_appoint,
        name='involvement_position_modeladmin_appoint'
    ),
    re_path(
        r'^involvement/position/extend/(\d+)/$',
        views.admin_extend_deadline,
        name='involvement_position_extend'
    ),
]
