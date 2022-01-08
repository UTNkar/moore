from django.shortcuts import render, get_object_or_404
from events.models import Event, EventApplication


def admin_remove_applications(request, pos_id=None):
    """
    Admin view to appoint members to the position
    """
    event = get_object_or_404(Event, pk=pos_id)
    applications = EventApplication.objects.filter(event=event)

    if request.method == 'POST':
        if 'confirm' in request.POST:
            applications.delete()

    view = {
        'get_meta_title': 'Remove applications',
        'get_page_title': 'Remove applications for',
        'get_page_subtitle': event.__str__(),
        'header_icon': 'pick',
    }
    context = {
        'view': view,
        'request': request,
        'event': event,
        'applications': applications
    }
    return render(request, 'events/admin/event_remove_applications.html',
                  context)
