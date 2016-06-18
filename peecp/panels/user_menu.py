from pyramid_layout.panel import panel_config

@panel_config(name='user_menu', renderer='templates/panels/user_menu.jinja2')
def user_menu(context, request, user):
    return {'user':user}
