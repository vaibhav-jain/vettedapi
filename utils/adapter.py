from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


__all__ = ['SignupAdapter']


class SignupAdapter(DefaultAccountAdapter):
    """

    """

    def __init__(self, request=None):
        super(SignupAdapter, self).__init__(request)
        self.password = None

    def get_email_confirmation_url(self, request, emailconfirmation):
        return settings.APP_SERVER + emailconfirmation.key

    # def save_user(self, request, user, form, commit=True):
    # #     user = super(SignupAdapter, self).save_user(request, user, form, commit=True)
    # #     data = form.cleaned_data
    # #     print(data)
    # #     self.password = data["password1"]
    # #     return user
    #
    # def send_confirmation_mail(self, request, emailconfirmation, signup):
    #     current_site = get_current_site(request)
    #     # print(request.body)
    #     print(self.request.POST)
    #     print(dir(self.request))
    #     activate_url = self.get_email_confirmation_url(
    #         request,
    #         emailconfirmation)
    #     ctx = {
    #         "user": emailconfirmation.email_address.user,
    #         "password": request.POST.get('password1'),
    #         "activate_url": activate_url,
    #         "current_site": current_site,
    #         "key": emailconfirmation.key,
    #     }
    #     if signup:
    #         email_template = 'account/email/email_confirmation_signup'
    #     else:
    #         email_template = 'account/email/email_confirmation'
    #     self.send_mail(
    #         email_template, emailconfirmation.email_address.email, ctx
    #     )
