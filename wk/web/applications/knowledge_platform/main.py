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
Next Step:
    实现文章的发布、删除
    publish: 
    delete:
    private:
    三张表：用户文章列表、公开文章列表、回收站文章列表
    文档引擎三？四？张表：公开文章列表、回收站文章列表、所有文章列表、每个用户文章列表
    用户发布文章时：
        
    用户删除文章时：
    
    
    
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

            class prefix:
                article = join_path(self.url_prefix, Sitemap.prefix.article)
                user = join_path(self.url_prefix, Sitemap.prefix.user)
                static_files = join_path(self.url_prefix, Sitemap.prefix.static_files)
                pkg_resource = join_path(self.url_prefix, Sitemap.prefix.pkg_resource)

        class Context(web.Context):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.update(
                    URL=URL
                )

        self.serve_root = serve_root
        self.usman = web.UserManager(PATH.user_manager,
                                     home_url=URL.home,
                                     signup_url=URL.signup,
                                     login_url=URL.login,
                                     logout_url=URL.logout, )
        self.usman.register(self)
        self.document_engine = ENGINE.DocumentStorageEngine(PATH.document_storage_engine,
                                                            id2url=lambda id: join_path(URL.prefix.article, id))
        self.index_engine = ENGINE.IndexEngine(PATH.index_engine)
        self.search_engine = ENGINE.SearchEngine(self.index_engine)
        self.static_storage_engine = ENGINE.StaticStorageEngine(PATH.static_storage_engine, check_when_start=True)

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
        def do_edit(article_id, object, user):
            document = object
            context = Context(user=user, article=None)
            if article_id:
                if document:
                    self.document_engine.update_document(article_id, document)
                    return web.ActionRedirect(location=URL.home, message="上传成功!").jsonify()
                else:
                    # 编辑文章
                    document = self.document_engine.get(article_id)
                    context.article = document
                    return pages.EditArticlePage().render(context=context)
            else:
                # 创建新文章
                doc = object
                if doc is None:
                    return pages.EditArticlePage().render(context=context)
                print(doc)
                res = self.document_engine.check(doc)
                if not res['success']:
                    return jsonify(res)
                doc['author'] = user['id']

                ret = self.document_engine.save(doc)
                user['articles'].append(ret['id'])
                self.usman.set_user(user['id'], user)

                print("saved, info : %s" % (ret))
                self.index_engine.add_document(ret['id'], doc['text'])
                return web.ActionRedirect(location='/', message="上传成功!").jsonify()

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
