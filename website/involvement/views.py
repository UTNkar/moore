from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from rules.contrib.views import permission_required

from involvement import forms
from involvement.models import Position, Team, Application


def open_positions(request, context):
    """View redirect for the currently open positions"""
    context['positions'] = context['positions'].filter(
        recruitment_start__lte=date.today()
    ).filter(
        recruitment_end__gte=date.today()
    )
    context['teams'] = Team.objects.all()
    return render(request, 'involvement/open_positions.html', context)


@login_required
def my_applications(request, context):
    """View redirect for the applications by user"""
    if request.method == 'POST':
        # TODO: Use form?
        try:
            action = request.POST.get('action')
            appl_id = request.POST.get('application')
            appl = Application.objects.get(id=appl_id)
            if appl.applicant != request.user:
                messages.add_message(request, messages.ERROR,
                                     _('You cannot delete an application that '
                                       'is not yours!'))
            elif appl.position.recruitment_end < date.today():
                messages.add_message(request, messages.ERROR,
                                     _('You cannot delete an application '
                                       'after its deadline has passed!'))
            else:
                if action == 'delete':
                    appl.delete()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        _('Your application has been removed!')
                    )
                else:
                    messages.add_message(request, messages.ERROR,
                                         _('No action has been supplied!'))
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('This application does not exist!'))

    applications = Application.objects.filter(applicant=request.user).order_by(
        'position__recruitment_end'
    )

    context['drafts'] = applications.filter(
        position__in=context['positions'],
        position__recruitment_end__gte=date.today(),
        status='draft',
    )
    context['submitted'] = applications.filter(
        position__in=context['positions'],
        position__recruitment_end__gte=date.today(),
        status='submitted',
    )
    context['waiting'] = applications.filter(
        Q(position__in=context['positions'],
          position__recruitment_end__lt=date.today(),
          status='submitted')
        | Q(position__in=context['positions'],
            status='approved')
    )
    context['old'] = applications.filter(
        position__in=context['positions'],
        status__in=['disapproved', 'appointed', 'turned_down'],
    )

    return render(request, 'involvement/my_applications.html', context)


def view_position(request, context, page, position=None):
    """
    View function for specific positions.
    """
    context['position'] = get_object_or_404(context['positions'], id=position)

    # Load application form if user is logged in
    if request.user.is_authenticated:
        # Did the user already have an application?
        try:
            appl = Application.objects.get(applicant=request.user,
                                           position=context['position'])
            context['status'] = appl.status
        except ObjectDoesNotExist:
            appl = Application()
            context['status'] = 'draft'
        # Did the user already fill in the form?
        if request.method == 'POST' and not context['position'].is_past_due:
            context['form'] = forms.ApplicationForm(request.POST,
                                                    instance=appl)
            context['reference_forms'] = forms.ReferenceFormSet(request.POST,
                                                                request.FILES,
                                                                instance=appl)
            if context['form'].is_valid() \
                    and context['reference_forms'].is_valid():
                appl = context['form'].save(commit=False)
                appl.applicant = request.user
                appl.position = context['position']
                appl.save()
                context['reference_forms'].save()
                if not appl.status == 'draft':
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        _('Your application has been submitted!'),
                    )
                    return HttpResponseRedirect(
                        page.get_url(request=request)
                        + page.reverse_subpage('my_applications')
                    )
            else:
                return render(request, 'involvement/position.html', context)

        # Render fresh: empty or after saving draft.
        context['form'] = forms.ApplicationForm(instance=appl)
        context['reference_forms'] = forms.ReferenceFormSet(instance=appl)

    return render(request, 'involvement/position.html', context)


def get_position_by_pk(request, position_id):
    return get_object_or_404(Position, pk=position_id)


@permission_required('involvement.appoint_position', fn=get_position_by_pk)
def admin_appoint(request, pos_id=None):
    """
    Admin view to appoint members to the position
    """
    position = get_object_or_404(Position, pk=pos_id)

    if request.method == 'POST':
        form = forms.AppointmentForm(position, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _('Your decisions have successfully been saved.'),
            )
            return HttpResponseRedirect(
                reverse('involvement_position_modeladmin_index')
            )
    else:
        form = forms.AppointmentForm(position)

    view = {
        'get_meta_title': 'Appoint applicants',
        'get_page_title': 'Appoint applicants for',
        'get_page_subtitle': position.__str__(),
        'header_icon': 'pick',
    }
    context = {
        'view': view,
        'request': request,
        'position': position,
        'form': form,
    }
    return render(request, 'involvement/admin/position_appointment.html',
                  context)


@permission_required('involvement.approve_position', fn=get_position_by_pk)
def admin_approve_applicants(request, key):
    """
    Admin view to approve members for a position
    """
    position = get_object_or_404(Position, pk=key)
    applications = position.applications.filter(
        status__in=['submitted', 'approved', 'disapproved']
    )

    formset_class = modelformset_factory(
        Application,
        form=forms.ApprovalForm,
        can_delete=False,
        extra=0,
    )
    if request.method == 'POST':
        formset = formset_class(request.POST, request.FILES,
                                queryset=applications)
        if formset.is_valid():
            formset.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _('Your decisions have successfully been saved.'),
            )
            return HttpResponseRedirect(
                reverse('involvement_position_modeladmin_index')
            )
    else:
        formset = formset_class(queryset=applications)

    view = {
        'get_meta_title': 'Approve applicants',
        'get_page_title': 'Approve applicants for',
        'get_page_subtitle': position.__str__(),
        'header_icon': 'tick',
    }
    context = {
        'view': view,
        'request': request,
        'position': position,
        'formset': formset,
    }
    return render(request, 'involvement/admin/position_approval.html', context)


@permission_required('involvement.change_position', fn=get_position_by_pk)
def admin_extend_deadline(request, key):
    """
    An admin view to automatically extend the deadline of vacant positions.
    """
    position = get_object_or_404(Position, pk=key)
    if position.recruitment_end >= date.today():
        messages.add_message(
            request, messages.ERROR,
            _('This position is not due for an extension yet.')
        )
    elif position.applications.exclude(status='draft').exists():
        messages.add_message(
            request, messages.ERROR,
            _('A position with submitted applications cannot be automatically'
              'extended.')
        )
    else:
        position.recruitment_end = date.today() + timedelta(days=7)
        position.save()
        messages.add_message(
            request, messages.SUCCESS,
            _('The recruitment deadline for %(position)s has been extended '
              'until %(date)s') % {
                'position': position,
                'date': position.recruitment_end,
            }
        )

    return HttpResponseRedirect(
        reverse('involvement_position_modeladmin_index')
    )
