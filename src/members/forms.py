from datetime import datetime

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from wagtail.users import forms as wagtail
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (password_validators_help_text_html, validate_password)
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from members.models import StudyProgram, Member, Section

from utils.melos_client import MelosClient

User = get_user_model()


class PersonNumberField(forms.Field):
    def __init__(self, *args, **kwargs):
        super(PersonNumberField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None, ''
        value = force_text(value)
        validators.RegexValidator(
            regex=r'^\d{8}\-?(T|\d)\d{3}$',
            message=_('Use the format YYYYMMDD-XXXX for your person number.')
        )(value)
        try:
            date = datetime.strptime(value[:8], '%Y%m%d').date()
        except ValueError:
            date = value[:4] + '-' + value[4:6] \
                + '-' + value[6:8]
            raise ValidationError(
                _('%(date)s is an invalid date'),
                params={'date': date}
            )
        number = value[-4:]
        return date, number

    def widget_attrs(self, widget):
        attrs = super(PersonNumberField, self).widget_attrs(widget)
        attrs['class'] = attrs.get('class', '') + ' person_number'
        attrs['placeholder'] = 'YYYYMMDD-XXXX'
        return attrs


class MemberForm(forms.ModelForm):
    person_number = PersonNumberField(
        label=_('Person number'),
        help_text=_('Person number using the YYYYMMDD-XXXX format.'),
    )

    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone_number',
                  'registration_year', 'study', 'section', 'email']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        initial = kwargs.pop('initial', {})

        if instance is not None:
            melos_user_id = instance.melos_id
            melos_data = MelosClient.get_user_data(melos_user_id)
            initial['person_number'] = instance.person_number()
            initial['first_name'] = melos_data['first_name']
            initial['last_name'] = melos_data['last_name']
            initial['person_number'] = melos_data['person_number']
            initial['phone_number'] = melos_data['phone_number']
            initial['email'] = melos_data['email']

        super(MemberForm, self).__init__(initial=initial, *args, **kwargs)
        if instance is not None:
            self.fields['first_name'].disabled = True
            self.fields['last_name'].disabled = True
            self.fields['phone_number'].disabled = True
            self.fields['person_number'].disabled = True
            self.fields['email'].disabled = True

    def clean_username(self):
        username = self.cleaned_data['username']
        if (Member.objects.exclude(pk=self.instance.pk)
                .filter(username=username).exists()):
            raise forms.ValidationError(_(
                "A user with that username already exists."))
        return username

    def clean(self):
        person_number = self.cleaned_data['person_number']
        melos_id = MelosClient.get_melos_id(person_number)
        if (Member.objects.exclude(pk=self.instance.pk)
                .filter(melos_id=melos_id).exists()) or melos_id is False:
            raise forms.ValidationError(_(
                "Something went wrong, please try again."))

        self.instance.melos_id = melos_id

    def save(self, commit=True):
        # Need to reset fields since we don't want to store this data in the database
        self.instance.phone_number = ''
        self.instance.email = ''
        self.instance.birthday = None
        self.instance.person_number_ext = ''
        self.instance.first_name = ''
        self.instance.last_name = ''
        self.instance.status = ''
        return super(MemberForm, self).save(commit=commit)


class RegistrationForm(MemberForm, auth.UserCreationForm):
    class Meta:
        model = Member
        fields = ['username']
        field_classes = {'username': auth.UsernameField}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'}
        )


class CustomPasswordResetForm(forms.Form):

    person_number = PersonNumberField(
        label=_('Person number'),
        help_text=_('Person number using the YYYYMMDD-XXXX format.'),
    )

    def get_email(self, melos_id):
        data = MelosClient.get_user_data(melos_id)
        if data:
            return data['email']
        return ''

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(
            subject,
            body,
            from_email,
            [to_email]
            )
        if html_email_template_name is not None:
            html_email = loader.render_to_string(
                html_email_template_name,
                context
                )
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = User._default_manager.filter(**{
            '%s__iexact' % User.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """

        person_number = self.cleaned_data['person_number']
        melos_id = MelosClient.get_melos_id(person_number)
        if melos_id:
            member = Member.objects.filter(melos_id=int(melos_id)).exists()
            if (member):
                email = self.get_email(melos_id)
            else:
                email = ''
        else:
            email = ''

        user = Member.objects.filter(melos_id=int(melos_id)).get()

        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        context = {
            'email': email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
            **(extra_email_context or {}),
        }
        self.send_mail(
            subject_template_name, email_template_name, context,
            from_email, email,
            html_email_template_name=html_email_template_name,
        )


class UserForm(wagtail.UsernameForm):

    required_css_class = "required"

    @property
    def password_required(self):
        return getattr(settings, 'WAGTAILUSERS_PASSWORD_REQUIRED', True)

    @property
    def password_enabled(self):
        return getattr(settings, 'WAGTAILUSERS_PASSWORD_ENABLED', True)

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    first_name = forms.CharField(required=False, label=_('First Name'))
    last_name = forms.CharField(required=False, label=_('Last Name'))

    password1 = forms.CharField(
        label=_('Password'), required=False,
        widget=forms.PasswordInput,
        help_text=_("Leave blank if not changing."))
    password2 = forms.CharField(
        label=_("Password confirmation"), required=False,
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    is_superuser = forms.BooleanField(
        label=_("Administrator"), required=False,
        help_text=_('Administrators have full access to manage any object '
                    'or setting.'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name']
        if self.password_enabled:
            if self.password_required:
                self.fields['password1'].help_text = mark_safe(
                    password_validators_help_text_html())
                self.fields['password1'].required = True
                self.fields['password2'].required = True
        else:
            del self.fields['password1']
            del self.fields['password2']

    # We cannot call this method clean_username since this the name of the
    # username field may be different, so clean_username would not be reliably
    # called. We therefore call _clean_username explicitly in _clean_fields.
    def _clean_username(self):
        username_field = User.USERNAME_FIELD
        # This method is called even if username if empty, contrary to clean_*
        # methods, so we have to check again here that data is defined.
        if username_field not in self.cleaned_data:
            return
        username = self.cleaned_data[username_field]

        users = User._default_manager.all()
        if self.instance.pk is not None:
            users = users.exclude(pk=self.instance.pk)
        if users.filter(**{username_field: username}).exists():
            self.add_error(User.USERNAME_FIELD, forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            ))
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password2 != password1:
            self.add_error('password2', forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            ))

        return password2

    def validate_password(self):
        """
        Run the Django password validators against the new password. This must
        be called after the user instance in self.instance is populated with
        the new data from the form, as some validators rely on attributes on
        the user model.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 == password2:
            validate_password(password1, user=self.instance)

    def _post_clean(self):
        super()._post_clean()
        try:
            self.validate_password()
        except forms.ValidationError as e:
            self.add_error('password2', e)

    def _clean_fields(self):
        super()._clean_fields()
        self._clean_username()

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.password_enabled:
            password = self.cleaned_data['password1']
            if password:
                user.set_password(password)

        if commit:
            user.save()
            self.save_m2m()
        return user


class UserEditForm(UserForm):
    password_required = False

    def __init__(self, *args, **kwargs):
        kwargs.pop('editing_self', False)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Member
        fields = [
            'username', 'is_superuser', 'groups',
            'email', 'first_name', 'last_name',
            'phone_number'
        ]
        widgets = {
            'groups': forms.CheckboxSelectMultiple
        }


class CustomUserEditForm(UserEditForm):
    """
    Custom form to edit users from within the wagtail admin interface.
    """
    person_number = PersonNumberField(
        label=_('Person number'),
        help_text=_('Person number using the YYYYMMDD-XXXX format.'),
        required=False
    )

    registration_year = forms.CharField(
        required=False,
        label=_('Registration year'),
    )
    study = forms.ModelChoiceField(
        required=False,
        queryset=StudyProgram.objects,
        label=_("Study Program"),
    )
    section = forms.ModelChoiceField(
        required=False,
        queryset=Section.objects,
        label=_("Section"),
    )
    status = forms.ChoiceField(
        choices=Member.MEMBERSHIP_CHOICES,
        label=_("Membership status"),
        required=False
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        initial = kwargs.pop('initial', {})
        if instance is not None:
            melos_user_id = instance.melos_id
            melos_data = MelosClient.get_user_data(melos_user_id)
            person_number = melos_data['person_number']

            initial['first_name'] = melos_data['first_name']
            initial['last_name'] = melos_data['last_name']
            initial['person_number'] = person_number
            initial['email'] = melos_data['email']
            initial['phone_number'] = melos_data['phone_number']

            status = melos_is_member(person_number)
            initial['status'] = "member" if status else "nonmember"

        super(CustomUserEditForm, self).__init__(
            initial=initial, *args, **kwargs
        )

        self.fields['first_name'].disabled = True
        self.fields['last_name'].disabled = True
        self.fields['person_number'].disabled = True
        self.fields['phone_number'].disabled = True
        self.fields['email'].disabled = True
        self.fields['status'].disabled = True

    def save(self, commit=True):
        self.instance.email = ''
        self.instance.birthday = None
        self.instance.person_number_ext = ''
        self.instance.first_name = ''
        self.instance.last_name = ''
        self.instance.phone_number = ''
        self.instance.status = ''

        return super(CustomUserEditForm, self).save(commit=commit)


class UserCreationForm(UserForm):
    class Meta:
        model = Member
        fields = ['username', 'is_superuser',
                  'groups']
        widgets = {
            'groups': forms.CheckboxSelectMultiple
        }


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form to create user from within the Wagtail admin user interface.
    """ 
    person_number = PersonNumberField(
        label=_('Person number'),
        help_text=_('Person number using the YYYYMMDD-XXXX format.'),
    )
    registration_year = forms.CharField(
        required=False,
        label=_('Registration year'),
    )
    study = forms.ModelChoiceField(
        required=False,
        queryset=StudyProgram.objects,
        label=_("Study program"),
    )
    section = forms.ModelChoiceField(
        required=False,
        queryset=Section.objects,
        label=_("Section"),
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        initial = kwargs.pop('initial', {})
        if instance is not None:
            initial['person_number'] = instance.person_number()

        super(CustomUserCreationForm, self).__init__(
            initial=initial, *args, **kwargs
        )

    def clean_person_number(self):
        person_number = self.cleaned_data['person_number']

        melos_id = MelosClient.get_melos_id(person_number)
        if melos_id:
            if (Member.objects.exclude(pk=self.instance.pk)
                    .filter(melos_id=melos_id).exists()):
                raise forms.ValidationError(_('Incorrect SSN'))
            self.instance.melos_id = melos_id
            return person_number

        else:
            raise forms.ValidationError(_('Incorrect SSN'))

    def save(self, commit=True):
        person_number = self.cleaned_data['person_number']
        self.instance.birthday = person_number[0]
        self.instance.person_number_ext = person_number[1]

        return super(CustomUserCreationForm, self).save(commit=commit)
