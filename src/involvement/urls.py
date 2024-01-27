from django.conf.urls import re_path
from rest_framework import routers
from involvement import views

#API URLs
router = routers.SimpleRouter()
router.register(r'^position', views.position_api.PositionViewSet, basename="PositionView")
router.register(r'^position2', views.position_api.Position2ViewSet, basename="Position2View")
router.register(r'^teams', views.team_read_api.TeamViewSet, basename="TeamsView")
router.register(r'^roles', views.role_read_api.RoleViewSet, basename="RolesView")
router.register(r'^application', views.application_api.ApplicationViewSet, basename="ApplicationView")

urlpatterns = [
    re_path(
        r'^admin/involvement/position/elect/(\d+)/$',
        views.admin_approve_applicants,
        name='involvement_position_modeladmin_approve'
    ),
    re_path(
        r'^admin/involvement/position/appoint/(\d+)/$',
        views.admin_appoint,
        name='involvement_position_modeladmin_appoint'
    ),
    re_path(
        r'^admin/involvement/position/extend/(\d+)/$',
        views.admin_extend_deadline,
        name='involvement_position_extend'
    ),
]

urlpatterns += router.urls
