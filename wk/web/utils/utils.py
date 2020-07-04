from wk.io import db
import wk
from wk.basic import join_path, IterObject, SecureDirPath, PointDict, Path, DirPath, PowerDirPath, Status, \
    StatusSuccess, StatusError
from flask import request, render_template, redirect, make_response, jsonify
import functools, inspect
from jinja2 import Environment, PackageLoader

usman_env = Environment(loader=PackageLoader('wk.data', 'templates/modules/UserManager'))
import inspect, uuid, copy


def log_func(msg="*** running %s ...."):
    # def decorator(func):
    #     @functools.wraps(func)
    #     def wrapper(*args,**kwargs)
    #         print(msg%(func.__name__) if "%s" in msg else msg)
    #         func(*args,**kwargs)
    #     return wrapper
    def before(func):
        print(msg % (func.__name__) if "%s" in msg else msg)

    decorator = config_run(before=before)
    return decorator


def config_run(before=None, after=None):
    def decorator(func):
        def do_before():
            dosome = before
            if not dosome: return
            if hasattr(dosome, '__call__'):
                dosome_args = inspect.getfullargspec(dosome).args
                if 'func' in dosome_args:
                    dosome(func=func)
                else:
                    dosome()
            else:
                print(dosome)

        def do_after():
            dosome = after
            if not dosome: return
            if hasattr(dosome, '__call__'):
                dosome_args = inspect.getfullargspec(dosome).args
                if 'func' in dosome_args:
                    dosome(func=func)
                else:
                    dosome()
            else:
                print(dosome)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            do_before()
            res = func(*args, **kwargs)
            do_after()
            return res

        # print("wrapper args:",inspect.getfullargspec(wrapper).args)
        # print("func args:",inspect.getfullargspec(func).args)
        return wrapper

    return decorator


def rename_func(name):
    def decorator(func):
        func.__name__ = name

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            return func(*args, **kwargs)

        return new_func

    return decorator


def get_arg_dict(func):
    sign = inspect.signature(func)
    keys = list(sign.parameters.keys())
    dic = dict()
    for key in keys:
        value = sign.parameters.get(key).default
        dic[key] = value
    return dic


def parse_from(*refers):
    def decorator(f):
        # fargs = inspect.getfullargspec(f).args
        arg_dict=get_arg_dict(f)
        fargs=list(arg_dict.keys())
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            dic = {}
            for ref in refers:
                d = ref() if callable(ref) else dict(ref)
                d = d or {}
                if d: dic.update(d)
            params = {}
            for ag in fargs:
                val = dic.get(ag, None)
                if val is None:
                    for k, v in dic.items():
                        if k.replace('-', '_') == ag:
                            val = v
                if val is None:
                    val=arg_dict.get(ag,None)
                params[ag]=val
            params.update(kwargs)
            return f(*args, **params)

        return wrapper

    return decorator


def get_files(): return dict(request.files)


def get_form(): return request.form


def get_json(): return request.json


def get_cookies(): return request.cookies


def get_url_args(): return request.args


# parse_json is a decorator
parse_json_and_form = parse_from(get_json, get_form)
parse_json = parse_from(get_json)
parse_form = parse_from(get_form)
parse_files = parse_from(get_files)
parse_cookies = parse_from(get_cookies)
parse_args = parse_from(get_url_args)
parse_all = parse_from(get_cookies, get_form, get_json, get_url_args)


class Context(PointDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.utils = PointDict(
            wk=wk
        )


def log(*msgs):
    print("log".center(10, '*') + ":" + ' '.join([str(msg) for msg in msgs]))


class UserManager:
    '''
    user:
        id
        username
        email
        password
        articles
        zans
        cais
        views
        picture
        signature
        introduction

    '''
    __status_succeeded__ = 'succeeded'
    __status_failed__ = 'failed'

    def __init__(self, dbpath, User, home_url='/', url_prefix='/', signup_url=None, login_url=None, logout_url=None):
        self.db = db.Piu(dbpath)
        self.User = User
        self.home_url = home_url
        self.url_prefix = url_prefix
        self.signup_url = signup_url or join_path(url_prefix, 'join')
        self.login_url = login_url or join_path(url_prefix, 'login')
        self.logout_url = logout_url or join_path(url_prefix, 'logout')
        self.update_all_user_fields()

    def register(self, app):
        app.route(self.signup_url, methods=['get', 'post'])(self.signup())
        app.route(self.login_url, methods=['get', 'post'])(self.login())
        app.route(self.logout_url, methods=['get', 'post'])(self.logout())

    def exists_user(self, email):
        if not self.get_user(email): return False
        return True

    def users(self):
        return self.db.keys()

    def update_all_user_fields(self):
        self.db.pause_save()
        for k, v in self.db.dic.items():
            v = self.User(**v)
            self.db.set(k, v)
        self.db.resume_save(save_now=True)

    def add_user(self, user={}):
        user = self.User(**user)
        id = user['id']
        self.db.add(id, user)
        return id

    def get_user(self, id):
        return copy.deepcopy(self.db.get(id, None))

    def set_user(self, id, user):
        self.db.set(id, user)

    def update_user(self, id, info={}):
        if not self.get_user(id):
            self.add_user(id)
        user = self.db.get(id)
        user.update(**info)
        self.db.set(id, user)

    def status(self, status, **kwargs):
        return jsonify(dict(status=status, **kwargs))

    def home_page(self, **kwargs):
        return redirect('/')

    def redirect_page(self, target, target_text=None, message=None, source=None):
        return usman_env.get_template('Redirect.tem').render(target=target, target_text=target_text, message=message,
                                                             source=source)

    def signup_page(self, target, method='post', **kwargs):
        return usman_env.get_template('SignUp.tem').render(action=target, method=method, **kwargs)

    def login_page(self, target, method='post', **kwargs):
        return usman_env.get_template('Login.tem').render(action=target, method=method, **kwargs)

    def error_page(self, **kwargs):
        return usman_env.get_template('Error.tem').render(**kwargs)

    def get_user_context(self, arg_name='user'):
        '''从cookies中获取用户信息'''

        def decorator(f):
            @functools.wraps(f)
            @parse_cookies
            def wrapper(email, username, password, *args, **kwargs):
                # log(email,username,password)
                user = self.check_user(email, username, password)
                if not isinstance(user, self.User):
                    user = None
                kwargs.update(**{arg_name: user})
                return f(*args, **kwargs)

            return wrapper

        return decorator

    def check_user(self, email, username, password):
        if not (email and password) and not (username and password):
            return None
        if email:
            user = self.db.search(email=email)
            if not user:
                return self.redirect_page(target=self.signup_url, target_text='登录页面', message='请注册')
                # return self.signup_page(target=self.home_url, method='post')
            user = user[0]
            if user and (user['email'] == email) and (user['password'] == password):
                return user
            else:
                return None
        if username:
            user = self.db.search(username=username)
            user = PointDict.from_dict(user) if user else user
            if not user:
                return None
            if user and (user.username == username) and (user.password == password):
                return user
            else:
                return self.error_page()

    def login_required(self, f):
        @functools.wraps(f)
        @parse_cookies
        def wrapper(email, username, password, *args, **kwargs):
            # print(email,username,password)
            if not (email and password) and not (username and password):
                return self.redirect_page(target=self.signup_url, target_text='登录页面', message='请先登录')
                # return self.login_page(target=self.login_url,method='post')
            if email:
                user = self.db.search(email=email)
                if not user:
                    return self.redirect_page(target=self.signup_url, target_text='注册页面', message='请注册')
                    # return self.signup_page(target=self.signup_url, method='post')
                user = user[0]
                if user and (user['email'] == email) and (user['password'] == password):
                    return f(*args, **kwargs)
                else:
                    return self.error_page()
            elif username:
                user = self.db.search(username=username)
                if not user:
                    return self.redirect_page(target=self.signup_url, target_text='注册页面', message='请注册')
                    # return self.signup_page(target=self.signup_url, method='post')
                if user:
                    user = user[0]
                if user and (user['username'] == username) and (user['password'] == password):
                    return f(*args, **kwargs)
                else:
                    return self.error_page()

        return wrapper

    def signup(self):
        @parse_form
        def do_signup(email, password, username):
            if not email:
                return self.signup_page(target=self.signup_url, method='post')
            log("sign up:", email, password, username)
            if self.db.search(email=email):
                msg = "Email has been taken"
                log(msg)
                return jsonify(StatusError(message=msg))
            if self.db.search(username=username):
                msg = "Username has been taken"
                log(msg)
                return jsonify(StatusError(message=msg))

            id = self.add_user({'email': email, 'password': password, "username": username})
            log(self.db.get(id))
            resp = redirect(self.home_url)
            resp.set_cookie('email', email)
            resp.set_cookie('username', email)
            resp.set_cookie('password', password)
            return resp

        return do_signup

    def logout(self):
        @log_func()
        @parse_form
        def do_logout(email, username, password):
            resp = redirect(self.home_url)
            resp.set_cookie('email', '', expires=0)
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
            log("resp:", resp)
            return resp

        return do_logout

    def login(self):
        @log_func()
        @parse_form
        def do_login(email, username, password):
            log(email, username, password)
            if not email and not username:
                return self.login_page(target=self.login_url, method='post')
            if email:
                if not self.db.search(email=email):
                    msg = "Email doesn't exists."
                    print(msg)
                    return self.status(self.__status_failed__, msg=msg)
                # resp = make_response(self.home_page()) if not redirect_to else redirect_to
                resp = redirect(self.home_url)
            else:
                assert username
                if not self.db.search(username=username):
                    msg = "Username doesn't exists."
                    print(msg)
                    return self.status(self.__status_failed__, msg=msg)
                # resp = make_response(self.home_page()) if not redirect_to else redirect_to
                resp = redirect(self.home_url)
            resp.set_cookie('email', email)
            resp.set_cookie('password', password)
            log("resp:", resp)
            return resp

        return do_login
