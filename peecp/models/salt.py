import requests
import json

class SaltApi():
    def __init__(self, token=None):

        # TODO: get salt api url from config file
        self.base_url = 'http://127.0.0.1:8080'
        self.token = token
        self.headers = {'Accept': 'application/json',
                        # 'Content-Type':'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-Auth-Token': token}
        self.eauth = 'pam'


    def run(self, function, arg=[], kwarg={}, target='*'):

        self.headers['Content-Type'] = 'application/json'
        json_arg = [{"client": "local", "tgt": target, "fun": function}]
        json_arg[0].setdefault('arg', arg) if arg else None
        json_arg[0].setdefault('kwarg', kwarg) if kwarg else None

        req = requests.post(
            url=self.base_url,
            headers=self.headers,
            data=json.dumps(json_arg)
        )


        return req.json()

    # TODO: uncomplete function
    def chack_password(self, username, password):
        return False
        data = {'fun'   : 'shadow',
                'client': 'local',
                'tgt'   : '*'}
        req = requests.post(
            url=self.base_url,
            headers=self.headers,
            data=data
        )

        return req.json()

    # TODO: change target to cammand only master
    # This is a Bug in multi minion systems
    def change_password(self, username, password):
        pass_in_json = self.json_run('shadow.gen_password', arg=password)

        j = pass_in_json['return'][0]
        hashed_pass = j[next(iter(j))]

        # print(hashed_pass)

        data = {'fun'   : 'shadow.set_password',
                'arg'   : [username, hashed_pass],
                'client': 'local',
                'tgt'   : '*'}
        req = requests.post(
            url=self.base_url,
            headers=self.headers,
            data=data
        )

        return req.json()

    def login(self, username, password):

        req = requests.post(
            url='/'.join([self.base_url, 'login']),
            headers=self.headers,
            data={'username': username,
                  'password': password,
                  'eauth'   : self.eauth}
        )

        print(req.content)

        if req.ok:
            try:
                d = req.json()
                return d
            except:
                return None
        else:
            return None

    def logout(self, token):
        headers = {'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest', 'X-Auth-Token': token}
        req = requests.post(
            url='/'.join([self.base_url, 'logout']),
            headers=headers,
        )
        return True
