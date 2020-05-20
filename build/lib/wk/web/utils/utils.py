from wk.io import db
from wk.basic import join_path,IterObject,SecureDirPath,PointDict,Path,DirPath,PowerDirPath,Status,StatusSuccess,StatusError
from flask import request,render_template,redirect,make_response,jsonify
import functools,inspect
from jinja2 import Environment,PackageLoader
env=Environment(loader=PackageLoader('wpkit.data','templates'))
import inspect

def log_func(msg="*** running %s ...."):
    # def decorator(func):
    #     @functools.wraps(func)
    #     def wrapper(*args,**kwargs)
    #         print(msg%(func.__name__) if "%s" in msg else msg)
    #         func(*args,**kwargs)
    #     return wrapper
    def before(func):
        print(msg % (func.__name__) if "%s" in msg else msg)
    decorator=config_run(before=before)
    return decorator

def config_run(before=None,after=None):
    def decorator(func):
        def do_before():
            dosome=before
            if not dosome:return
            if hasattr(dosome,'__call__'):
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
            if hasattr(dosome,'__call__'):
                dosome_args = inspect.getfullargspec(dosome).args
                if 'func' in dosome_args:
                    dosome(func=func)
                else:
                    dosome()
            else:
                print(dosome)
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            do_before()
            res=func(*args,**kwargs)
            do_after()
            return res
        # print("wrapper args:",inspect.getfullargspec(wrapper).args)
        # print("func args:",inspect.getfullargspec(func).args)
        return wrapper
    return decorator

def rename_func(name):
    def decorator(func):
        func.__name__=name
        @functools.wraps(func)
        def new_func(*args,**kwargs):
            return func(*args,**kwargs)
        return new_func
    return decorator

def parse_from(*refers):
    def decorator(f):
        fargs = inspect.getfullargspec(f).args
        @functools.wraps(f)
        def wrapper(*args,**kwargs):
            dic={}
            for ref in refers:
                d = ref() if callable(ref) else dict(ref)
                d = d or {}
                if d:dic.update(d)
            params = {}
            for ag in fargs:
                params[ag] = dic.get(ag, None)
            # print("args:",fargs)
            # print("params:",params)
            params.update(kwargs)
            return f(*args,**params)
        return wrapper
    return decorator
def get_form():return request.form
def get_json():return request.json
def get_cookies():return request.cookies
# parse_json is a decorator
parse_json_and_form=parse_from(get_json,get_form)
parse_json=parse_from(get_json)
parse_form=parse_from(get_form)
parse_cookies=parse_from(get_cookies)
parse_all=parse_from(get_cookies,get_form,get_json)


def log(*msgs):
    print("log".center(10, '*') + ":" + ' '.join([str(msg) for msg in msgs]))
class UserManager:
    __status_succeeded__='succeeded'
    __status_failed__='failed'
    def __init__(self,dbpath='./data/user_db',home_url='/'):
        self.db=db.Piu(dbpath)
        self.home_url=home_url
    def exists_user(self,email):
        if not self.get_user(email):return False
        return True
    def users(self):
        return self.db.keys()
    def add_user(self,email,info={}):
        self.db.add(email,info)
    def get_user(self,email):
        return self.db.get(email,None)
    def update_user(self,email,info={}):
        if not self.get_user(email):
            self.add_user(email)
        self.db.get(email).update(info)
    def status(self,status,**kwargs):
        return jsonify(dict(status=status,**kwargs))
    def home_page(self,**kwargs):
        return env.get_template('pan.html').render(signup=True, **kwargs)
    def signup_page(self,**kwargs):
        return env.get_template('sign3.html').render(signup=True, **kwargs)
    def login_page(self,**kwargs):
        return env.get_template('sign3.html').render(login=True,**kwargs)
    def error_page(self,**kwargs):
        return env.get_template('error.html').render(**kwargs)
    def login_required(self,f):
        @functools.wraps(f)
        @parse_cookies
        def wrapper(user_email,user_password,*args,**kwargs):
            if not (user_email and user_password):
                return self.login_page()
            user=self.get_user(user_email)
            user=PointDict.from_dict(user) if user else user
            if not user:
                return self.signup_page()
            if user and (user.user_email == user_email ) and (user.user_password==user_password):
                return f(*args,**kwargs)
            else:
                # return self.login_page()
                return self.error_page()
        return wrapper

    def signup(self):
        @parse_form
        def do_signup(user_email,user_password):
            log("sign up:",user_email,user_password)
            # if self.db.get(user_email,None):return self.signup_page(msg='Email has been taken.')
            if self.db.get(user_email,None):
                msg="Email has been taken"
                log(msg)
                return jsonify(StatusError(msg=msg))
            self.add_user(user_email,{'user_email':user_email,'user_password':user_password})
            log(self.db.get(user_email))
            resp=make_response(self.status(status=self.__status_succeeded__,redirect=self.home_url))
            resp.set_cookie('user_email',user_email)
            resp.set_cookie('user_password',user_password)
            return resp
        return do_signup()

    def login(self,redirect_to=None):
        def decorator():
            @log_func()
            @parse_form
            def do_login(user_email, user_password):
                log("log***:", user_email, user_password)
                if not self.db.get(user_email, None):
                    msg = "Email doesn't exists."
                    print(msg)
                    return self.status(self.__status_failed__, msg=msg)
                resp = make_response(self.home_page()) if not redirect_to else redirect_to
                resp.set_cookie('user_email', user_email)
                resp.set_cookie('user_password', user_password)
                log("resp:",resp)
                return resp
            return do_login()
        return decorator






