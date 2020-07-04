from wk import web
from wk.web import request, session, generate_password_hash, check_password_hash
import wk
from wk import generate_hash, gen_sms_code, ArgumentSpace, gen_random_key, generate_random_id
from wk.web.modules.apis.qq import get_user_info, get_openid
from . import utils
import json, random, uuid, functools, inspect
import requests

module_env = web.get_module_environment('login')


class TIME:
    MINUTE = 60
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    WEEK = 7 * DAY
    MONTH = 30 * DAY
    YEAR = 365 * DAY
    EMIAL_CODE_TIMEDELTA = 30 * MINUTE
    SMS_CODE_TIMEDELTA = 5 * MINUTE
    NORMAL_PAGE_KEY=30*MINUTE


def retrieve_from_session(arg, strict=False):
    return ArgumentSpace(**dict(session)).retrieve_arguments(arg, strict=strict)


class LoginManager:
    def __init__(self, User, UserAuth, db, app, state_manager, home_url='/', register_url='/register',
                 login_url='/login',
                 logout_url='/logout',
                 pkg_resource_url='/pkg-resource',
                 auth_qq_callback_url='auth/qq/callback',
                 qq_auth_config=None,
                 getter_user_home=lambda x: 'users/' + x,
                 auth_url='/auth', send_sms_url='', send_email_url='',
                 send_sms_code_to=None, send_email_code=None, ):
        self.User = User
        self.UserAuth = UserAuth
        self.db = db
        assert isinstance(app, (web.Flask, web.Blueprint))
        self.app = app
        self.state_manager = state_manager
        self.home_url = home_url
        self.register_url = register_url
        self.login_url = login_url
        self.logout_url = logout_url
        self.auth_url = auth_url
        self.send_sms_url = send_sms_url
        self.send_email_url = send_email_url
        self.send_sms_code_to = send_sms_code_to
        self.auth_qq_callback_url = auth_qq_callback_url
        self.getter_user_home = getter_user_home

        self.send_email_code = send_email_code
        self.qq_auth_config = qq_auth_config
        assert qq_auth_config

        class Context(dict):
            def __init__(self, **kwargs):
                dic = dict(
                    pkg_resource_url=pkg_resource_url,
                    home_url=home_url,
                    register_url=register_url,
                    logout_url=logout_url,
                    login_url=login_url,
                    auth_url=auth_url,
                    send_sms_url=send_sms_url,
                    send_email_url=send_email_url,
                    qq_auth_config=qq_auth_config,
                )
                dic.update(**kwargs)
                super().__init__(**dic)

        self.Context = Context

    def init(self):
        @self.app.route(self.auth_qq_callback_url + '/token', methods=['get'])
        def do_auth_callback_qq_token():
            data = web.request.args.to_dict()
            access_token = data.get('access_token')
            open_id = get_openid(data)
            user_info = get_user_info(data, open_id,self.qq_auth_config.appid)
            with self.db.get_session() as sess:
                users = sess.query(self.UserAuth).filter_by(
                    self.UserAuth.identity_type == 'qq',
                    self.UserAuth.identifier == open_id,
                ).all()

                if len(users):
                    user = users[0]
                    return web.redirect(self.getter_user_home(user.id))
                else:
                    user_id = generate_random_id()
                    user = self.User(id=user_id, username=user_info.get('nickname'),
                                     avatar=user_info.get('figureurl_1'), gender=user_info.get('gender'))
                    sess.add(user)
                    user_auth = self.UserAuth(user_id=user_id, identity_type='qq', identifier=open_id,
                                              credential=access_token, )
                    sess.add(user)
                    sess.add(user_auth)
                    return web.redirect(self.getter_user_home(user_id))

        @self.app.route(self.auth_qq_callback_url, methods=['get'])
        @web.parse_args
        def do_auth_callback_qq(code, state):
            if not self.state_manager.check_key(state):
                return web.StatusErrorResponse(message='该请求可能已过期')
            url = 'https://graph.qq.com/oauth2.0/token'
            body = {'grant_type': 'authorization_code', 'client_id': self.qq_auth_config.appid,
                    'client_secret': self.qq_auth_config.appkey, 'code': code,
                    'redirect_uri': self.qq_auth_config.redirect_uri}
            response = requests.get(url, params=body)  # 发送GET请求
            token = response.text
            requests.session().close()  # 关闭请求
            return web.redirect(self.auth_qq_callback_url + '/token?' + token)

        @self.app.route(web.join_path(self.login_url), methods=['get'])
        def do_login_get():
            return self.login_page()

        @self.app.route(web.join_path(self.login_url), methods=['post'])
        @self.decorator_adaptive_convert_response()
        @web.parse_from(web.get_url_args, web.get_json, web.get_form)
        def do_login_post(type, phone, validation_code, password, email, redirect_url=self.home_url):
            if type == 'phone':
                if not (phone and password):
                    return web.StatusErrorResponse(message='缺失手机号码或密码')
                with self.db.get_session() as sess:
                    exist = sess.query(self.UserAuth).filter(self.UserAuth.identity_type == 'phone',
                                                             self.UserAuth.identifier == phone,
                                                             self.UserAuth.credential == password).all()
                    if not exist:
                        return web.StatusErrorResponse(message='手机号码或密码错误')
                    user_auth = exist[0]
                    login_key = gen_random_key()
                    self.state_manager.push('login_key', login_key, user_auth.user_id, timedelta=TIME.MONTH)
                    session['login_key'] = login_key
                    return web.ActionRedirect(redirect_url)
            elif type == 'phone-code':
                if not (phone and validation_code):
                    return web.StatusErrorResponse(message='缺失手机号码或验证码')
                target, code = retrieve_from_session(' phone_number,sms_code')
                if not (target == phone and validation_code == code):
                    return web.StatusErrorResponse(message='手机号码错误或验证码错误')
                if not self.state_manager.get(target, code):
                    return web.StatusErrorResponse(message='验证码超时')
                with self.db.get_session() as sess:
                    exist = sess.query(self.UserAuth).filter(self.UserAuth.identity_type == 'phone',
                                                             self.UserAuth.identifier == phone, ).all()
                    if not exist:
                        return web.StatusErrorResponse(message='该手机号码尚未注册')
                    user_auth = exist[0]
                    login_key = gen_random_key()
                    self.state_manager.push('login_key', login_key, user_auth.user_id, timedelta=TIME.MONTH)
                    session['login_key'] = login_key
                    return web.ActionRedirect(redirect_url)
            elif type == 'email':
                if not (email and password):
                    return web.StatusErrorResponse(message='缺失邮箱地址或密码')
                with self.db.get_session() as sess:
                    exist = sess.query(self.UserAuth).filter(self.UserAuth.identity_type == 'email',
                                                             self.UserAuth.identifier == email).all()
                    if not exist:
                        return web.StatusErrorResponse(message='邮箱地址错误,您是否还未注册？')
                    user_auth = exist[0]
                    if not user_auth.credential == password:
                        return web.StatusErrorResponse(message='邮箱地址或密码错误')
                    login_key = gen_random_key()
                    self.state_manager.push('login_key', login_key, user_auth.user_id, timedelta=TIME.MONTH)
                    session['login_key'] = login_key
                    return web.ActionRedirect(redirect_url)

        @self.app.route(web.join_path(self.register_url, ''), methods=['get', 'post'])
        @self.decorator_adaptive_convert_response()
        @web.parse_from(web.get_url_args, web.get_json, web.get_form)
        def do_register(type, phone, validation_code, password, password_confirm, email):
            method = request.method
            if method == 'GET':
                return self.register_page()
            elif method == 'POST':
                if type == 'phone':
                    if not (phone and validation_code and password and password_confirm):
                        return web.StatusErrorResponse(message="表单不完整")
                    target, code = retrieve_from_session(' phone_number,sms_code')
                    if not (target == phone and validation_code == code):
                        return web.StatusErrorResponse(message='手机号码错误或验证码错误')
                    if not self.state_manager.get(phone, validation_code):
                        return web.StatusErrorResponse(message="发生错误，可能验证码已超时")
                    user = self.User()
                    user_auth = self.UserAuth(user_id=user.id, identity_type='phone', identifier=phone,
                                              credential=password)
                    with self.db.get_session() as sess:
                        exist = sess.query(self.UserAuth).filter(self.UserAuth.identity_type == 'phone',
                                                                 self.UserAuth.identifier == phone).count()
                        if exist:
                            return web.StatusErrorResponse(message='该手机号码已被注册')
                        sess.add(user)
                        sess.add(user_auth)
                        sess.commit()
                        return web.ActionRedirect(location=self.login_url)


                elif type == 'email':
                    target, code = retrieve_from_session('email,email_code')
                    if not (target == email and code == validation_code):
                        return web.StatusErrorResponse(message='验证码错误或邮箱错误')
                    if not self.state_manager.get(target, code):
                        return web.StatusErrorResponse(message='验证码超时')
                    user = self.User()
                    user_auth = self.UserAuth(user_id=user.id, identity_type='email', identifier=email,
                                              credential=password)
                    with self.db.get_session() as sess:
                        exist = sess.query(self.UserAuth).filter(self.UserAuth.identity_type == 'email',
                                                                 self.UserAuth.identifier == email).count()
                        if exist:
                            return web.StatusErrorResponse(message='该邮箱已被注册')
                        sess.add(user)
                        sess.add(user_auth)
                        sess.commit()
                        return web.ActionRedirect(location=self.login_url)

        @self.app.route(self.send_sms_url, methods=['get', 'post'])
        @web.parse_json
        def do_send_sms(target):
            if not utils.checkPhone(target):
                print('电话号码错误:%s' % target)
                if self.app.debug:
                    raise
                return web.StatusErrorResponse(message='不是正确的电话号码')
            try:
                code = self.send_sms_code_to(target)
            except:
                print('发送号码时出现错误')
                if self.app.debug:
                    raise
                return web.StatusErrorResponse(message='发送号码时出现错误')
            session['sms_code'] = code
            session['phone_number'] = target
            self.state_manager.push(target, code, timedelta=TIME.SMS_CODE_TIMEDELTA)
            return web.StatusSuccessResponce(message='短信验证码已发送')

        @self.app.route(self.send_email_url, methods=['get', 'post'])
        @web.parse_json
        def do_send_email_code(target):
            if not utils.checkEmail(target):
                print('邮箱地址错误:%s' % (target))
                if self.app.debug:
                    raise
                return web.StatusErrorResponse(message='不是正确的邮箱地址')
            try:
                code = self.send_email_code(target)
                if code is None:
                    print("邮件发送失败")
                elif self.app.debug:
                    print('成功发送验证码%s至%s' % (code, target))
            except:
                print('发送邮件验证码时出现错误')
                if self.app.debug:
                    raise
                return web.StatusErrorResponse(message='发送邮件验证码时出现错误')
            session['email_code'] = code
            session['email'] = target
            self.state_manager.push(target, code, timedelta=TIME.EMIAL_CODE_TIMEDELTA)
            return web.StatusSuccessResponce(message='邮箱验证码已发送')

        return self

    def parse_user_from_request(self):
        # if web.session.get('')
        pass

    def generate_hash(self, s):
        return wk.generate_hash(self.app.secret_key + s)

    def login_required(self, get_user=False, name='user'):
        if inspect.isfunction(get_user):
            func = get_user

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.is_login():
                    return self.message_page('您尚未登录，是否前往登陆？', redirect={
                        '返回首页': self.home_url,
                        '点击前往': self.login_url,
                    })
                return func(*args, **kwargs)

            return wrapper

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                user = self.get_login_user()
                if not user:
                    return self.message_page('您尚未登录，是否前往登陆？', redirect={
                        '返回首页': self.home_url,
                        '点击前往': self.login_url,
                    })
                if get_user:
                    res = func(*args, **{name: user}, **kwargs)
                else:
                    res = func(*args, **kwargs)
                return res

            return wrapper

        return decorator

    def get_login_user(self):
        login_key = retrieve_from_session('login_key')
        if not login_key:
            return False
        user = self.state_manager.get('login_key', login_key)
        if not user:
            return False
        user_id = user['c3']
        with self.db.get_session() as sess:
            exist = sess.query(self.User).filter(self.User.id == user_id).all()
            if not exist:
                print('user_id %s exists in state_store but not found in users' % (user_id))
                return False
            return exist[0]

    def is_login(self):
        login_key = retrieve_from_session('login_key')
        if not login_key:
            return False
        user = self.state_manager.get('login_key', login_key)
        if not user:
            return False
        return True

    def register_error_page(self, message="注册失败", redirect=None):
        return self.message_page(message=message, redirect=redirect)

    def login_error_page(self, message="登录失败", redirect=None):
        return self.message_page(message=message, redirect=redirect)

    def message_page(self, message, redirect=None, links=None):
        _links = {
            "首页": self.home_url,
            "前往登录": self.login_url,
            "前往注册": self.register_url,
        }
        _links.update(**(links or {}))
        if request.referrer:
            _back = {"返回": request.referrer}
        else:
            _back = None
        context = self.Context(
            message=message,
            redirect=redirect,
            links=_links,
            back=_back,
            title='info-page'
        )
        return module_env.get_template('MessagePage.tem').render(context=context)

    def register_page(self):
        context = self.Context(
            title='注册',
            key=self.state_manager.produce_key(timedelta=TIME.NORMAL_PAGE_KEY)
        )
        return module_env.get_template('RegisterPage.tem').render(context=context)

    def login_page(self):
        context = self.Context(
            title='登录',
            key=self.state_manager.produce_key(timedelta=TIME.NORMAL_PAGE_KEY)
        )
        return module_env.get_template('LoginPage.tem').render(context=context)

    def json_to_page(self, res, page='message'):
        pages = {
            'message': self.message_page,
            'login_error': self.login_error_page,
            'register_error': self.register_error_page,
        }
        if isinstance(page, str):
            page = pages[page]
        res = page(message=res['message'])
        return res

    def decorator_adaptive_convert_response(self):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                if isinstance(res, (web.StatusResponse, dict)):
                    if not res['success']:
                        print('*** Failed:', res)
                    if request.form:
                        if res['action'] == 'redirect':
                            res = web.redirect(res['params']['location'])
                        else:
                            res = self.json_to_page(res)
                return res

            return wrapper

        return decorator

    def decorator_json_to_page(self, page='message'):
        pages = {
            'message': self.message_page,
            'login_error': self.login_error_page,
            'register_error': self.register_error_page,
        }
        if isinstance(page, str):
            page = pages[page]

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                if isinstance(res, (web.StatusResponse, dict)):
                    res = page(message=res['message'])
                else:
                    try:
                        r = json.loads(res)
                        res = page(message=r['message'])
                    except:
                        pass
                return res

            return wrapper

        return decorator
