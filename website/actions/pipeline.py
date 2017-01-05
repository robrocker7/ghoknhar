from django.shortcuts import redirect


def redirect_if_no_refresh_token(backend, response, social, *args, **kwargs):
    data = backend.strategy.request_data()
    print data
    if backend.name == 'google-oauth2' and social and \
        response.get('refresh_token') is None and \
        social.extra_data.get('refresh_token') is None:
        return redirect('/login/google-oauth2?approval_prompt=force')