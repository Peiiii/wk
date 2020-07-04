from wk import web
import wk
from wk.web import join_path
from wk.web.modules.login import LoginManager
from wk.web.modules.apis.aliyun import AliyunSmsService
from wk.web.modules.apis.qq import get_openid, get_user_info
from wk.web.modules.email import EmailSender
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from . import data_access_layer as DAL


class ZSPT(web.Application):
    url_prefix = '/'

    def __init__(self, import_name, config={}, *args, **kwargs):
        super().__init__(import_name, *args, **kwargs)

        class CONFIG:
            INIT_DB = True
            SECRET_KEY = 'nheb23gi23gr3^*()$#@=j.'
            class AUTH:
                class QQ:
                    appid='101884229'
                    appkey='835a3552175800a628681fe4632ae172'
                    redirect_uri='http://eiooie.com/auth/qq/callback'
            class QQEMAIL:
                sender = 'zshub@foxmail.com'
                auth_code = 'vladiwdamvprfffi'

            class ALIYUN:
                ACCESS_KEY_ID = 'LTAI4GABwJcNrdbPakJmaG8d'
                ACCESS_SECRET = 'akR4Fhef7pQiuDPvNR3vNt7w1mNTqC'

        class PATH:
            DB_URI = 'sqlite:///zspt_test.db'

        class CONST:
            SITE_NAME = 'zspt'

        class Services:
            email_sender = EmailSender(CONFIG.QQEMAIL.sender, CONFIG.QQEMAIL.auth_code)

        class Sitemap:
            class Getter:
                home = lambda x=None: join_path('/', x or '')
                users = lambda x=None: join_path('users', x or '')
                articles = lambda x=None: join_path('articles', x or '')
                files = lambda x=None: join_path('files', x or '')
                questions = lambda x=None: join_path('questions', x or '')
                collections = lambda x=None: join_path('collections', x or '')
                admin = lambda x=None: join_path('admin', x or '')

                # auth = lambda x=None: join_path('auth', x or '')
                class User:
                    home = lambda x: join_path('users', x)
                    login = lambda: 'login'
                    logout = lambda: 'logout'
                    register = lambda: 'register'

                    class Validation:
                        send_sms_url = lambda: join_path('api', 'validation', 'sms')
                        send_email_url = lambda: join_path('api', 'validation', 'email')

                class Auth:
                    class Callback:
                        qq = lambda: 'auth/qq/callback'

                class Assets:
                    pkg_resource = lambda x=None: join_path('pkg-resource', x or '')
                    site = lambda x=None: join_path('pkg-resource/sites', CONST.SITE_NAME, x or '')
                    img = lambda x=None: join_path('pkg-resource/sites', CONST.SITE_NAME, 'img', x or '')
                    css = lambda x=None: join_path('pkg-resource/sites', CONST.SITE_NAME, 'css', x or '')
                    js = lambda x=None: join_path('pkg-resource/sites', CONST.SITE_NAME, 'js', x or '')
                    pkgs = lambda x=None: join_path('pkg-resource/sites', CONST.SITE_NAME, 'pkgs', x or '')

        class URL:
            class Getter:
                home = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.home(x))
                users = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.users(x))
                articles = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.articles(x))
                files = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.files(x))
                questions = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.questions(x))
                collections = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.collections(x))
                admin = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.admin(x))

                # auth = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.auth(x))
                class User:
                    home = lambda x: join_path(self.url_prefix, Sitemap.Getter.User.home())
                    login = lambda: join_path(self.url_prefix, Sitemap.Getter.User.login())
                    logout = lambda: join_path(self.url_prefix, Sitemap.Getter.User.logout())
                    register = lambda: join_path(self.url_prefix, Sitemap.Getter.User.register())

                    class Validation:
                        send_sms_url = lambda: join_path(self.url_prefix, Sitemap.Getter.User.Validation.send_sms_url())
                        send_email_url = lambda: join_path(self.url_prefix,
                                                           Sitemap.Getter.User.Validation.send_email_url())

                class Auth:
                    class Callback:
                        qq = lambda: join_path(self.url_prefix, Sitemap.Getter.Auth.Callback.qq())

                class Assets:
                    pkg_resource = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.Assets.pkg_resource(x))
                    site = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.Assets.site(x))
                    img = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.Assets.img(x))
                    css = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.Assets.css(x))
                    js = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.Assets.js(x))
                    pkgs = lambda x=None: join_path(self.url_prefix, Sitemap.Getter.Assets.pkgs(x))

        self.secret_key = CONFIG.SECRET_KEY
        self.db = DAL.sql.Engine(PATH.DB_URI)
        self.db.create_all()
        self.state_manager = DAL.StateManger(self.db, DAL.StateStore)
        self.login_manager = LoginManager(DAL.User, DAL.UserAuth, self.db, self,
                                          state_manager=self.state_manager,
                                          home_url=URL.Getter.home(),
                                          pkg_resource_url=URL.Getter.Assets.pkg_resource(),
                                          register_url=URL.Getter.User.register(),
                                          login_url=URL.Getter.User.login(), logout_url=URL.Getter.User.logout(),
                                          send_sms_url=URL.Getter.User.Validation.send_sms_url(),
                                          send_email_url=URL.Getter.User.Validation.send_email_url(),
                                          send_email_code=Services.email_sender.send_email_code,
                                          auth_qq_callback_url=URL.Getter.Auth.Callback.qq(),
                                          qq_auth_config=CONFIG.AUTH.QQ,
                                          getter_user_home=URL.Getter.User.home,
                                          send_sms_code_to=AliyunSmsService(
                                              access_key_id=CONFIG.ALIYUN.ACCESS_KEY_ID,
                                              access_secret=CONFIG.ALIYUN.ACCESS_SECRET,
                                              debug=True
                                          ).send_to,
                                          ).init()

        @self.route(URL.Getter.home(), methods=['get'])
        def do_home():
            return 'Hello'
