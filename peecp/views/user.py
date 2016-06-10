from pyramid.security import (
    remember,
    forget
)

from pyramid.httpexceptions import (
    HTTPFound
)
from pyramid.view import view_config
from pyramid.view import view_defaults

from ..models.salt import SaltApi
from ..models.message import Message

from ..bower import components
@view_defaults()
class UserVeiw():
    def __init__(self, context, request):
        self.request = request
        self.context = context
        self.message = Message(request=request, source='userView')
        token = None
        if 'salt' in self.request.session:
            token = self.request.session['salt'].get('token', None)
        self.salt = SaltApi(token=token)
        request.include(components, 'bootstrap-rtl')

    @view_config(route_name='login', renderer='templates/login.jinja2')
    def login_view(self):
        # print(self.request.path)
        referer = self.request.path if not self.request.path == self.request.route_path('login') else self.request.POST.get('referer', '/')

        print(referer)
        # lang = self.request.POST.get('lang', '').strip()
        # lang = 'fa' if lang not in ['fa', 'en'] else lang
        # self.request.response.set_cookie('_LOCALE_', lang)

        # print(lang)

        auth_username = self.request.authenticated_userid
        print(auth_username)
        # print(self.request.session)
        if not auth_username:
            if 'submit' in self.request.POST:
                username =  self.request.POST.get('username', '')
                password = self.request.POST.get('password', '')
                user = self.salt.login(username, password)
                if user:
                    self.request.session['salt'] = user['return'][0]
                    headers = remember(self.request, username)

                    # headers.append(('Set-Cookie', '_LOCALE_={0}; Path=/'.format(lang)))

                    self.message.add('user fount', user=username)
                    return HTTPFound(location=referer, headers=headers)
                else:
                    self.message.add('user not fount', user=username)
                    # return HTTPFound(location=referer)
        else:
            return HTTPFound(location='/')
            # self.message.add('you are already loged in', user=auth_username)
            # return HTTPFound(location=referer)
        return {'referer': referer}

    @view_config(route_name='logout')
    def logout_view(self):
        salt = self.request.session.get('salt',None)
        if salt:
            token = salt['token']
            self.request.session.invalidate()
        else:
            token = None
        self.salt.logout(token)
        headers = forget(self.request)

        self.message.add('you are logged out', message_type=Message.info)
        return HTTPFound(location=self.request.route_url('home'), headers=headers)


    @view_config(route_name='change_password', renderer='templates/change_password.jinja2',permission='admin')
    def change_password_view(self):
        if 'submit' in self.request.POST:
            new_password = self.request.POST.get('new_password', '')
            re_new_password = self.request.POST.get('re_new_password', '')

            msg = 'password NOT changed.'
            if new_password and new_password==re_new_password:
                r = self.salt.change_password(self.request.authenticated_userid, new_password)
                if list(r['return'][0].values())[0]:
                    msg = 'password changed.'

            self.message.add(msg)
        return {}