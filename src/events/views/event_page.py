from django.utils import timezone as tz
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from events.models import Event, Ticket, EventApplication
from events.forms.event_form import EventForm


class EventView(FormMixin, DetailView):
    """View for a single event"""
    model = Event
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)

        event = self.get_object()
        application = None
        ticket = None

        if self.request.user.is_authenticated:
            # There should never be more than one application and ticket
            # so this may be unnecessarily defensive, but helps during testing
            application = EventApplication.objects.filter(
                event_applicant=self.request.user, event=event)
            if application.count() > 0:
                application = application[0]

            ticket = Ticket.objects.filter(
                owner=self.request.user, event=event)
            if ticket.count() > 0:
                ticket = ticket[0]

        if ticket:
            context['has_ticket'] = True

        if application:
            context['already_applied'] = True

        context['can_still_apply'] = event.end_of_application > tz.now()
        return context

    def get_success_url(self):
        return reverse('single-event-page',
                       kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        user = request.user
        event = self.get_object()
        form = self.get_form()

        if 'cancel_application' in request.POST:
            EventApplication.objects.get(event_applicant=user).delete()
            return self.form_valid(form)

        if event.first_come_first_serve:
            try:
                # Lowest unassigned ticket
                ticket = Ticket.objects.filter(
                    event=event, owner=None).order_by('ticket_number')[0]
                # it is assumed that the user here is authenticated
                ticket.owner = user
                ticket.save()
            except IndexError as e:
                print(e)  # TODO
        else:
            applications = EventApplication.objects.filter(
                event_applicant=user, event=event)
            if applications.count() > 0:
                # Prevents tampering.
                pass
            else:
                EventApplication(event_applicant=user, event=event).save()

        return self.form_valid(form)
