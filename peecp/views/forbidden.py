from pyramid.view import forbidden_view_config


@forbidden_view_config(renderer='../templates/forbidden.jinja2')
def notfound_view(request):
    return {}

