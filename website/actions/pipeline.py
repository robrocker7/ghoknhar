import pytz
from datetime import datetime, timedelta

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
    session_redirect = backend.strategy.session_get('redirect_uri')
    session_state = backend.strategy.session_get('state')
    
    if backend.name == 'google-plus-action' and social:
        auth_code = data.get('code')
        # create a Grant from the oauth toolkit lib
        ten_day_exp = datetime.now(pytz.utc) + timedelta(days=10)
        app = Application.objects.get(name='GoogleActionsAPI')  #hardcoded to googleplus
        grant = Grant.objects.create(code=auth_code,
                                     application=app,
                                     user=social.user,
                                     expires=ten_day_exp,
                                     redirect_uri=session_redirect)

        # delete older associations so we do not get confused
        UserSocialAuth.objects.filter(user=user, provider='google-plus-action').delete()
        
        social.uid = auth_code
        social.extra_data['state'] = session_state
        social.save()
        
        google_home_redirect = '{0}?code={1}&state={2}'.format(session_redirect, auth_code, session_state)
        return redirect(google_home_redirect)