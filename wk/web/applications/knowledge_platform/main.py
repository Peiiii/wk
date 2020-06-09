from wk import web, join_path, FakeOS, Folder
from . import pages, engines
import jieba
import os, shutil, glob, json
from flask import jsonify

'''
Site Structure:
    /               :search home
    /tree           :knowledge tree
    /f      :search files, to view files
    /u/<id>         :user home page
    /p/<id>         :read article
    /join           :sign up
    /login          :login
    /logout         :logout
    
    /static
    /files
    /pkg-resource
Contents:
    文章
    题目
    文件
    问答
    知识树
**已完成Next Step: 
    实现文章的发布、删除
    publish: 
    delete:
    private:
    三张表：用户文章列表、公开文章列表、回收站文章列表
    文档引擎三？四？张表：公开文章列表、回收站文章列表、所有文章列表
    每个用户文章列表: 私有、公开、回收站
    用户发布文章时：
        
    用户删除文章时：
Bug:
    用户退出登录后，访问其他用户主页时，导航栏还有其他用户的头像,没有对其他用户进行区分
Next:
    已发布文章取消发布?
    查看已删除的文章？恢复文章？彻底删除？
    搜索引擎清空索引的方法？
    文档引擎更新方法？清空方法？
    
NextNextStep:
    实现文章的推荐
    实现文章的组织方式（结构化的系统）
    文件的筛选方式
Future:
    问答、视频、评论系统、内容自动生成
    
'''


class KnowledgePlatform(web.MyBlueprint):
    url_prefix = '/'

    def __init__(self, import_name, config={}, *args, **kwargs):
        super().__init__(import_name, *args, **kwargs)
        self.config = config
        serve_root = config['serve_root']

        class ENGINE:
            IndexEngine = engines.IndexEngine
            SearchEngine = engines.SearchEngine
            StaticStorageEngine = engines.StaticStorageEngine
            DocumentStorageEngine = engines.DocumentStorageEngine

        class PATH:
            serve_root = config['serve_root']
            user_manager = serve_root + '/user_manager'
            static_storage_engine = serve_root + '/static_storage_engine'
            index_engine = serve_root + '/index_engine'
            document_storage_engine = serve_root + '/document_storage_engine'

        class Sitemap:
            home = '/'
            signup = '/join'
            login = '/login'
            logout = '/logout'
            search_file = '/files'
            upload = '/upload'
            editor = '/editor'

            class article:
                # new = '/article/new'
                edit = '/article/edit'
                new = edit
                publish = '/article/publish'
                delete = '/article/delete'

            class prefix:
                article = '/p'
                user = '/u'
                static_files = '/f'
                pkg_resource = '/pkg-resource'

        class URL:
            home = join_path(self.url_prefix, Sitemap.home)
            signup = join_path(self.url_prefix, Sitemap.signup)
            login = join_path(self.url_prefix, Sitemap.login)
            logout = join_path(self.url_prefix, Sitemap.logout)
            search_file = join_path(self.url_prefix, Sitemap.search_file)
            upload = join_path(self.url_prefix, Sitemap.upload)
            editor = join_path(self.url_prefix, Sitemap.editor)


            class article:
                new = join_path(self.url_prefix, Sitemap.article.new)
                edit = join_path(self.url_prefix, Sitemap.article.edit)
                publish = join_path(self.url_prefix, Sitemap.article.publish)
                delete = join_path(self.url_prefix, Sitemap.article.delete)

                class getter:
                    edit =lambda id: join_path(self.url_prefix, Sitemap.article.edit)+'?article_id=%s'%(id)
                    publish =lambda id: join_path(self.url_prefix, Sitemap.article.publish)+'?article_id=%s'%(id)
                    delete =lambda id: join_path(self.url_prefix, Sitemap.article.delete)+'?article_id=%s'%(id)

            class prefix:
                article = join_path(self.url_prefix, Sitemap.prefix.article)
                user = join_path(self.url_prefix, Sitemap.prefix.user)
                static_files = join_path(self.url_prefix, Sitemap.prefix.static_files)
                pkg_resource = join_path(self.url_prefix, Sitemap.prefix.pkg_resource)


        self.serve_root = serve_root
        self.usman = web.UserManager(PATH.user_manager,
                                     User=engines.User,
                                     home_url=URL.home,
                                     signup_url=URL.signup,
                                     login_url=URL.login,
                                     logout_url=URL.logout, )
        self.usman.register(self)
        self.index_engine = ENGINE.IndexEngine(PATH.index_engine)
        self.search_engine = ENGINE.SearchEngine(self.index_engine)
        self.static_storage_engine = ENGINE.StaticStorageEngine(PATH.static_storage_engine, check_when_start=True)
        self.document_engine = ENGINE.DocumentStorageEngine(PATH.document_storage_engine,
                                                            index_engine=self.index_engine, usman=self.usman,
                                                            id2url=lambda id: join_path(URL.prefix.article, id))
        app=self
        class Context(web.Context):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.update(
                    URL=URL,
                    get_user=app.usman.get_user,
                    get_article=app.document_engine.get,
                    get_user_link=lambda id:join_path(URL.prefix.user,id),
                    get_article_link=lambda aid:join_path(URL.prefix.article,aid),
                )

        # ###################Site Home Page####################
        @self.route(Sitemap.home, methods=['get'])
        @self.usman.get_user_context(arg_name='user')
        @web.parse_args
        def do_search(search_keywords, user):
            context = Context(user=user)
            if not search_keywords:
                return pages.HomePage().render(context=context)
            else:
                doc_ids = self.search_engine.search(search_keywords)
                docs = [self.document_engine.get(doc_id) for doc_id in doc_ids]
                docs = [pages.ArticleCard(doc) for doc in docs]
                return pages.SearchResultPage().compile(result=docs).render(context=context)

        # ###################Read Article####################
        @self.route(Sitemap.prefix.article + '/<string:id>')
        @self.usman.get_user_context(arg_name='user')
        def do_article(id, user):
            context = Context(user=user)
            doc = self.document_engine.get(id)
            return pages.ArticlePage(doc).render(context=context)

        # ###################Visit User Home Page####################
        @self.route(Sitemap.prefix.user + '/<string:id>')
        @self.usman.get_user_context(arg_name='user')
        def do_user(id, user):
            user_visit = self.usman.get_user(id)
            if not user_visit:
                return pages.ErrorPage(message='User Not Found.').render()
            user_visit['articles'] = [self.document_engine.get_info(doc_id) for doc_id in user_visit['articles']]

            context = Context(user=user_visit)
            if not user or id != user['id']:
                return pages.UserVisitPage().render(context=context)
            else:
                return pages.UserHomePage().render(context=context)

        # ###################Article New Edit Publish Delete######################
        @self.route(Sitemap.article.new, methods=['post', 'get'])
        @self.usman.login_required
        @self.usman.get_user_context(arg_name='user')
        @web.parse_from(web.get_form, web.get_json, web.get_url_args)
        def do_new_edit_article(article_id, object, user):
            document = object
            context = Context(user=user, article=None)
            if article_id:
                # 编辑文章
                if not user.is_own_article(article_id):
                    return pages.NoPermissionPage().render(context=context)
                if document:
                    # post
                    self.document_engine.update_document(article_id, document)
                    return web.ActionRedirect(location=URL.home, message="上传成功!").jsonify()
                else:
                    # get
                    document = self.document_engine.get(article_id)
                    context.article = document
                    return pages.EditArticlePage().render(context=context)
            else:
                # 创建新文章
                doc = object
                if doc is None:
                    # get
                    return pages.EditArticlePage().render(context=context)
                else:
                    # post
                    print(doc)
                    res = self.document_engine.check(doc)
                    if not res['success']:
                        return jsonify(res)
                    ret = self.document_engine.new(user,doc)
                    print("saved, info : %s" % (ret))
                    return web.ActionRedirect(location='/', message="上传成功!").jsonify()

        ###################Publish Article#####################
        @self.route(Sitemap.article.publish, methods=['post', 'get'])
        @self.usman.login_required
        @self.usman.get_user_context(arg_name='user')
        @web.parse_from(web.get_form, web.get_json, web.get_url_args)
        def do_publish_article(article_id, user):
            context = Context(user=user, article=None)
            assert article_id,user
            if not user.is_own_article(article_id):
                return pages.NoPermissionPage().render(context=context)
            if not self.document_engine.is_private(article_id):
                return web.StatusErrorResponse(message='你不能发布该文章').jsonify()
            url=self.document_engine.publish(user,article_id)
            return web.ActionRedirect(location=url,message='发布成功!').jsonify()

        ###################Delete Article#####################
        @self.route(Sitemap.article.delete, methods=['post', 'get'])
        @self.usman.login_required
        @self.usman.get_user_context(arg_name='user')
        @web.parse_from(web.get_form, web.get_json, web.get_url_args)
        def do_delete_article(article_id,  user):
            context = Context(user=user, article=None)
            assert article_id, user
            if not user.is_own_article(article_id):
                return pages.NoPermissionPage().render(context=context)
            ret = self.document_engine.delete_article(user, article_id)
            return web.ActionRefresh(message=ret or '删除成功').jsonify()

        # ##################Search Files##########################
        @self.route(Sitemap.search_file + '/', methods=['post', 'get'])
        @self.usman.get_user_context(arg_name='user')
        @web.parse_args
        def do_search_files(search_keywords, user):
            context = Context(user=user)
            if not search_keywords:
                return pages.FileSearchPageBase().render(context=context)
            keywords = []
            for word in search_keywords.split():
                keywords += list(jieba.cut(word))
            result = self.static_storage_engine.search(keywords)
            result = [self.static_storage_engine.file_info(file) for file in result]
            for file in result:
                print(file)
                file['url'] = join_path(URL.prefix.static_files, file['id'])
            result = [
                         pages.FileCard(x) for x in result
                     ] or "无结果"
            x = pages.FileSearchPageBase().compile(search_result=result).render(input_fill=search_keywords,
                                                                                context=context)
            return x

        # ###################File Get And Upload######################

        @self.route(Sitemap.prefix.static_files + '/<string:id>', methods=['get'])
        def do_get_static_files(id):
            return self.static_storage_engine.send_file(id)

        @self.route(Sitemap.upload, methods=['get', 'post'])
        @self.usman.get_user_context(arg_name='user')
        @web.parse_files
        def do_upload(file, image, user):
            context = Context(user=user)
            if file:
                info = self.static_storage_engine.saveFile(file)
                return web.jsonify({'link': URL.prefix.static_files + '/' + info['id']})
            elif image:
                info = self.static_storage_engine.saveImage(image)
                return web.jsonify({'link': URL.prefix.static_files + '/' + info['id']})
            else:
                return pages.UploadPage().render(context=context)
