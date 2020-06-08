from wk.extra.node import *
from wk.web.resources import Sites
Site=Sites.subdir('zspt')

class CONST:
    blue = '#0088cc'
    green = '#16a085'

class Parts:
    class plain:
        navigator = lambda: Site.load_plain('Navigator.tem')
        articleCard = lambda: Site.load_plain('ArticleCard.html')
        article = lambda: Site.load_plain('Article.html')
        userHomePage=lambda :Site.load_plain('UserHomePage.tem')
        userVisitPage=lambda :Site.load_plain('UserVisitPage.tem')
        editArticlePage=lambda :Site.load_plain('EditArticle.tem')
        uploadPage=lambda :Site.load_plain('Upload.tem')
    navigator=lambda :Site.load('Navigator.tem')
    articleCard=lambda :Site.load('ArticleCard.html')
    article=lambda :Site.load('Article.html')
    uploadPage = lambda: Site.load('Upload.tem')

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
                    Var(name="title", type='text')("title")
                ),
                QLinks.bootstrap(),
                QLinks.font_awesome(),
                QLinks.alertify(),
                QScripts.jquery(),
                QScripts.popper(),
                QScripts.bootstrap(),
                QScripts.jwerty(),
                QLinks.font_awesome(),
                QLinks.jgrowl(),
                QScripts.jgrowl(),


            ]),
            Body()([
                Var(name='body')("Add your content here"),
                QScripts.alertify(),
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
                Site.load('home.html').render()
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
                Site.load('DefaultSearchPage.html').render()
            ]
        )
class SearchResultPage(DefaultPageBase):
    def __init__(self):
        super().__init__()
        self.compile(
            title='Search',
            body=[
                Parts.plain.navigator(),
                Site.load('DefaultSearchPage.html').render(),
                Var(name='result')("No Result."),
            ]
        )

class ArticleCard(Div):
    def __init__(self,doc):
        super().__init__()
        self.__call__([
            Site.load('ArticleCard.html').render(
                article=doc
            )
        ])

class ArticlePage(DefaultPageBase):
    def __init__(self,article):
        super().__init__()
        self.compile(
            body=[
                Parts.plain.navigator(),
                Parts.article().render(article=article)
            ]
        )
class FileCard(Div):
    def __init__(self, file):
        super().__init__(_class='card')
        self.__call__([
            '''
      <li class="list-group-item" ><a href="{url}">{name}</a><span class="badge badge-secondary ml-2">{size}</span></li>
 '''.format(name=file['name'], size=file['size'], url=file['url'])
        ])

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
                Site.load('SearchFiles.html').render(),
                Div(_class="list-group p-2 m-auto text-center", style="max-width:40em;")(
                    Var(name="search_result")(
                        Div()("Nothing to show.")
                    )
                )
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
                Parts.plain.editArticlePage(),
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