from pyramid_layout.panel import panel_config

@panel_config(name='language_selector', renderer='templates/panels/language_selector.jinja2')
def language_selector(context, request):
    # TODO: get available languages
    langs = ['fa', 'en']
    return {'langs': langs}
