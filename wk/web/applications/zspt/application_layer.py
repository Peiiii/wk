from wk import web
import wk
from wk.web import join_path
from wk.web.modules.login import LoginManager
from wk.web.modules.apis.aliyun import AliyunSmsService
from wk.web.modules.apis.qq import get_openid, get_user_info
from wk.web.modules.email import EmailSender
from wk import PointDict, Pather
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from . import data_access_layer as DAL
from .presentation_layer import PageLoader
from . import business_logic_layer as BLL
from .config import create_sitemap

def log(*args,**kwargs):
    print('Log{sep}Log:\t'.format(sep='*'*20),*args,**kwargs)
class ZSPT(web.Application):
    url_prefix = '/'

    def __init__(self, import_name,CONFIG, config={}, *args, **kwargs):
        super().__init__(import_name, *args, **kwargs)
        Sitemap = create_sitemap(self.url_prefix,CONFIG.SITE_DATA_DIR_NAME)

        class Services:
            email_sender = EmailSender(CONFIG.QQEMAIL.sender, CONFIG.QQEMAIL.auth_code)
        Pages = PageLoader(CONFIG.SITE_DATA_DIR_NAME)
        self.add_static('/assets', web.pkg_static_path)
        self.secret_key = CONFIG.SECRET_KEY
        self.db = DAL.sql.Engine(CONFIG.PATH.DB_URI)
        self.db.create_all()
        self.state_manager = DAL.StateManger(self.db, DAL.StateStore)
        self.login_manager = LoginManager(DAL.User, DAL.UserAuth, self.db, self,
                                          state_manager=self.state_manager, home_url=Sitemap.Home(),
                                          pkg_resource_url=Sitemap.Assets(), register_url=Sitemap.User.register,
                                          login_url=Sitemap.User.login, logout_url=Sitemap.User.logout,
                                          send_sms_url=Sitemap.Api.Validation.send_sms_url,
                                          send_email_url=Sitemap.Api.Validation.send_email_url,
                                          send_email_code=Services.email_sender.send_email_code,
                                          auth_qq_callback_url=Sitemap.Auth.Qq.Callback(),
                                          qq_auth_config=CONFIG.AUTH.QQ,
                                          getter_user_home=Sitemap.User.Home,
                                          send_sms_code_to=AliyunSmsService(
                                              access_key_id=CONFIG.ALIYUN.ACCESS_KEY_ID,
                                              access_secret=CONFIG.ALIYUN.ACCESS_SECRET,
                                              debug=True
                                          ).send_to,
                                          ).init()
        app=self
        class Context(web.Context):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.update(
                    URL=Sitemap,
                    Sitemap=Sitemap,
                    title='知识树',
                    user=None,
                    article=None,
                )

            @classmethod
            def new(cls):
                context=cls()
                login_user=app.login_manager.get_login_user()
                log('user_login:',login_user)
                context.update(
                    login_user=login_user
                )
                return context
        @self.route(Sitemap.Home(), methods=['get'])
        def do_home():
            context = Context.new()
            return Pages.home_page(context)
        @self.route(Sitemap.User('<string:id>'),methods=['get'])
        @self.login_manager.login_required(get_user=True,name='user')
        @self.login_manager.same_user_required
        def do_user_home(id,user):
            context=Context.new()
            return Pages.user_home_page(context)
        @self.route(Sitemap.Contents.Articles.new)
        @self.login_manager.login_required(get_user=True, name='user')
        def do_article_new(user):
            context = Context.new()
            return Pages.article_write_page(context)

        # Apis

        def add_resource_user_assets(model,url):
            def update_attrs(obj,attrs):
                for k,v in attrs:
                    setattr(obj,k,v)
                return obj
            # assert isinstance(model,DAL.sql.Model)
            @app.route(url,methods=['post'])
            @app.login_manager.login_required(get_user=True, )
            @web.parse_json
            def post(user, data):
                instance = model(author_id=user.id, **data)
                with app.db.get_session() as sess:
                    sess.add(instance)
                return web.StatusSuccessResponse(message='添加成功')
            @app.route(join_path(url,'<string:resource_id>'),methods=['put'])
            @app.login_manager.login_required(get_user=True, )
            @web.parse_json
            def put(user,resource_id,data):
                with app.db.get_session() as sess:
                    instances = sess.query(DAL.Draft).filter(model.id == resource_id).all()
                    if not instances: return web.StatusErrorResponse(message='资源不存在')
                    instance = instances[0]
                    if not user.id == instance.author_id:
                        return web.StatusErrorResponse(message='没有权限')
                    update_attrs(instance,data)
                    return web.StatusSuccessResponse(message='修改成功')
            @app.route(join_path(url,'<string:resource_id>'),methods=['get'])
            @app.login_manager.login_required(get_user=True, name='user')
            def get(user,resource_id):
                with app.db.get_session() as sess:
                    instances = sess.query(model).filter(model.id == resource_id).all()
                    if not instances: return web.StatusErrorResponse(message='资源不存在')
                    instance = instances[0]
                    if not user.id == instance.author_id:
                        return web.StatusErrorResponse(message='没有权限')
                    return web.StatusSuccessResponse(data=instance)

            @app.route(join_path(url, '<string:resource_id>'), methods=['delete'])
            @app.login_manager.login_required(get_user=True, name='user')
            def delete(user, resource_id):
                with app.db.get_session() as sess:
                    instances = sess.query(model).filter(model.id == resource_id).all()
                    if not instances: return web.StatusErrorResponse(message='资源不存在')
                    instance = instances[0]
                    if not user.id == instance.author_id:
                        return web.StatusErrorResponse(message='没有权限')
                    sess.query(model).filter(model.id == resource_id).delete()
                    return web.StatusSuccessResponse(message='删除成功')

        add_resource_user_assets(DAL.Draft,Sitemap.Api.Drafts())
