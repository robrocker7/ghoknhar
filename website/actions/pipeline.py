from django.shortcuts import redirect


def redirect_if_no_refresh_token(backend, response, social, *args, **kwargs):
    data = backend.strategy.request_data()
    session_redirect = backend.strategy.session_get('redirect_uri')
    session_state = backend.strategy.session_get('state')
    
    if backend.name == 'google-plus-action' and social:
        auth_code = data.get('code')
        state = data.get('state')
        google_home_redirect = '{0}?code={1}&state={2}'.format(session_redirect, auth_code, session_state)
        print state
        print '-'
        print session_state
        print '-'
        print google_home_redirect
        return redirect(google_home_redirect)

    if backend.name == 'google-oauth2' and social and \
        response.get('refresh_token') is None and \
        social.extra_data.get('refresh_token') is None:
        return redirect('/login/google-oauth2?approval_prompt=force')