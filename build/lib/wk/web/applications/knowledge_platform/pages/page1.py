from wk.extra.node import *
from wk.web.resources import Sites
Site=Sites.subdir('zspt')

class CONST:
    blue = '#0088cc'
    green = '#16a085'

class Parts:
    class structure:
        searchFilePage = lambda: Site.load_frame('SearchFiles.tem')
        article = lambda: Site.load_frame('Article.tem')
        editArticlePage = lambda: Site.load_frame('EditArticle.tem')

    class plain:
        homePage = lambda: Site.load_plain('homePage.tem')
        navigator = lambda: Site.load_plain('Navigator.tem')
        articleCard = lambda: Site.load_plain('ArticleCard.tem')
        article = lambda: Site.load_plain('Article.tem')
        userHomePage=lambda :Site.load_plain('UserHomePage.tem')
        userVisitPage=lambda :Site.load_plain('UserVisitPage.tem')
        editArticlePage=lambda :Site.load_plain('EditArticle.tem')
        uploadPage=lambda :Site.load_plain('Upload.tem')
        # searchFilePage=lambda :Site.load_plain('SearchFiles.tem')
        successPage=lambda :Site.load_plain('SuccessPage.tem')
        fileListPage = lambda: Site.load_plain('FileList.tem')
        defaultSearchPage = lambda: Site.load_plain('DefaultSearchPage.tem')
        redirectPage = lambda: Site.load_plain('RedirectPage.tem')

    homePage = lambda: Site.load('homePage.tem')
    navigator=lambda :Site.load('Navigator.tem')
    articleCard=lambda :Site.load('ArticleCard.tem')
    article=lambda :Site.load('Article.tem')
    userHomePage = lambda: Site.load('UserHomePage.tem')
    userVisitPage = lambda: Site.load('UserVisitPage.tem')
    editArticlePage = lambda: Site.load('EditArticle.tem')
    uploadPage = lambda: Site.load('Upload.tem')
    # searchFilePage = lambda: Site.load('SearchFiles.tem')
    successPage = lambda: Site.load('SuccessPage.tem')
    fileListPage= lambda :Site.load('FileList.tem')
    defaultSearchPage= lambda :Site.load('DefaultSearchPage.tem')


class DefaultPageBase(Html):
    environment = dict(
        # blue='#1D93EC',
        blue='#0088cc',
        green='#16a085',
        gray='#E0E0E0'
    )

    def __init__(self):
        super().__init__()
        self.__call__([
            Head()([
                Meta(encoding='utf-8'),
                Meta(name="viewport", content="width=device-width, initial-scale=1, shrink-to-fit=no"),
                Title()(
                    Var(name="title", type='text')("知识库")
                ),
                # '<link rel="icon" href="/pkg-resource/sites/zspt/img/favicon.ico" type="image/x-icon" />',
                '<link rel="icon" href="/pkg-resource/imgs/icon/svg/知识库.svg" type="image/x-icon" />',
                QLinks.bootstrap(),
                QLinks.font_awesome(),
                QLinks.alertify(),
                QLinks.zico(),
                QScripts.jquery(),
                QScripts.popper(),

                QScripts.jwerty(),
                QLinks.font_awesome(),
                QLinks.jgrowl(),
                QScripts.jgrowl(),
                QScripts.zico(),
                QScripts.storejs(),
            ]),
            Body()([
                Var(name='body')("Add your content here"),
                QScripts.alertify(),
                QScripts.bootstrap(),
            ])
        ])

class HomePage(DefaultPageBase):
    environment = dict(
        active=0
    )
    def __init__(self):
        super().__init__()
        self.compile(
            body=[
                Parts.plain.navigator(),
                Parts.plain.homePage()
            ]
        )
class PostPage(DefaultPageBase):
    environment = dict(
        active=2,
    )
    def __init__(self):
        super().__init__()
        self.compile(
            title="Post Your Content",
            body=[
                Site.load('post.html').render(
                    navigator=Parts.plain.navigator()
                )
            ]
        )

class UploadPage(DefaultPageBase):
    environment = dict(
        active=3,
    )
    def __init__(self):
        super().__init__()
        self.compile(
            title="Post Your Content",
            body=[
                Parts.plain.navigator(),
                Parts.plain.uploadPage(),
            ]
        )

class DefaultSearchPage(DefaultPageBase):
    def __init__(self):
        super().__init__()
        self.compile(
            title='Search',
            body=[
                Parts.defaultSearchPage().render()
            ]
        )
class SearchResultPage(DefaultPageBase):
    def __init__(self):
        super().__init__()
        self.compile(
            title='知识树',
            body=[
                Parts.plain.navigator(),
                Parts.defaultSearchPage().render(),
                Var(name='result')("No Result."),
            ]
        )

class ArticleCard(Div):
    def __init__(self):
        super().__init__()
        self.__call__([
            Parts.plain.articleCard(),
        ])

class ArticlePage(DefaultPageBase):
    def __init__(self,):
        super().__init__()
        self.compile(
            body=[
                Parts.plain.navigator(),
                Parts.structure.article(),
            ]
        )

class FileSearchPageBase(DefaultPageBase):
    environment = dict(
        blue='#1D93EC',
        active=1
    )

    def __init__(self):
        super().__init__()
        self.compile(
            body=[
                Parts.plain.navigator(),
                Parts.structure.searchFilePage(),
            ]
        )

class UserHomePage(DefaultPageBase):
    def __init__(self):
        super().__init__()
        self.compile(
            body=[
                Parts.plain.navigator(),
                Parts.plain.userHomePage(),
            ]
        )
class UserVisitPage(DefaultPageBase):
    def __init__(self):
        super().__init__()
        self.compile(
            body=[
                Parts.plain.navigator(),
                Parts.plain.userVisitPage(),
            ]
        )
class EditArticlePage(DefaultPageBase):
    def __init__(self):
        super().__init__()
        self.compile(
            body=[
                Parts.plain.navigator(),
                Parts.structure.editArticlePage(),
            ]
        )
class ErrorPage(DefaultPageBase):
    def __init__(self,message='Error!'):
        super().__init__()
        self.compile(
            body=[
                Parts.plain.navigator(),
                message
            ]
        )

class NoPermissionPage(DefaultPageBase):
    def __init__(self,message='你没有权限修改该文章!'):
        super().__init__()
        self.compile(
            body=[
                Parts.plain.navigator(),
                message
            ]
        )

class PublishSuccessPage(DefaultPageBase):
    def __init__(self,message='发布成功!',link=None,link_text='前往查看'):
        super().__init__()
        self.compile(
            body=[
                Parts.plain.navigator(),
                Parts.successPage().render(message=message,link=link,link_text=link_text)
            ]
        )
class RedirectPage(DefaultPageBase):
    def __init__(self):
        super().__init__()
        self.compile(
            body=[
                Parts.plain.navigator(),
                Parts.plain.redirectPage(),
            ]
        )
