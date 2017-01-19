from django.shortcuts import redirect


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
        social.uid = auth_code
        social.extra_data['state'] = session_state
        social.save()
        
        google_home_redirect = '{0}?code={1}&state={2}'.format(session_redirect, auth_code, session_state)
        return redirect(google_home_redirect)