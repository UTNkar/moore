from django.urls import path, re_path
from events import views

urlpatterns = [
    path('event/<int:pk>',
         views.EventView.as_view(),
         name="single-event-page"
         ),
    path('ticket/<int:event_pk>',
         views.my_ticket,
         name="my-ticket"
         ),
    re_path(
        r'^admin/events/event/assign/(\d+)/$',
        views.admin_assign,
        name='events_event_modeladmin_assign_tickets'
    ),
    re_path(
        r'^admin/events/event/unassign_unpaid/(\d+)/$',
        views.admin_unassign_unpaid,
        name='events_event_modeladmin_unassign_unpaid_tickets'
    ),
    re_path(
        r'^admin/events/event/remove_applications/(\d+)/$',
        views.admin_remove_applications,
        name='events_event_modeladmin_remove_applications'
    ),
]
