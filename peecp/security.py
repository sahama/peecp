from pyramid.security import Allow, Everyone, Deny, authenticated_userid

def group_finder(userid, request):

    # TODO: add some code to add authz
    groups = []
    if userid:
        groups.append('users')
        if userid == 'admin':
            groups.append('admins')

    return groups



class RootFactory(object):

    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'users', 'user'),
               (Allow, 'admins', ('admin', 'user')),
               ]

    def __init__(self, request):
        self.request = request
