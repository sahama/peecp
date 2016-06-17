from pyramid_layout.panel import panel_config

@panel_config(name='footer', renderer='templates/panels/footer.jinja2')
def footer(context, request):
    return {}
