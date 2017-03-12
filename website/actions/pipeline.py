import pytz
from datetime import datetime, timedelta

from django.urls import reverse
from django.shortcuts import redirect

from social_django.models import UserSocialAuth

from oauth2_provider.models import Grant, Application

def redirect_if_no_refresh_token(backend, response, social, *args, **kwargs):

    if backend.name == 'google-oauth2' and social and \
        response.get('refresh_token') is None and \
        social.extra_data.get('refresh_token') is None:
        return redirect('/login/google-oauth2?approval_prompt=force')


def google_action_redirect(backend, response, social, *args, **kwargs):
    data = backend.strategy.request_data()

    if backend.name == 'google-plus-action' and social:
        session_redirect = backend.strategy.session_get('redirect_uri', '/')
        session_state = backend.strategy.session_get('state',
            data.get('session_state', data.get('state')))

        user_details = backend.get_user_details(
            backend.user_data(social.extra_data['access_token']))

        auth_code = data.get('code')
        # create a Grant from the oauth toolkit lib
        ten_day_exp = datetime.now(pytz.utc) + timedelta(days=10)
        app = Application.objects.get(name='GoogleActionsAPI')  #hardcoded to googleplus
        grant = Grant.objects.update_or_create(code=auth_code,
            defaults={
                'application':app,
                'user':social.user,
                'expires':ten_day_exp,
                'redirect_uri':session_redirect
            })

        # delete older associations so we do not get confused
        UserSocialAuth.objects.exclude(pk=social.pk).filter(
            user=social.user, provider='google-plus-action').delete()
        
        social.uid = user_details['email']
        social.extra_data['state'] = session_state
        social.save()

        # only redirect if google home is asking
        if session_redirect != '/':
            google_home_redirect = '{0}?code={1}&state={2}'.format(session_redirect, auth_code, session_state)
            return redirect(google_home_redirect)