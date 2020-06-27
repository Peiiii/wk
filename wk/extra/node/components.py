from wk.extra.node import *


class Urls:
    class js:
        bootstrap = 'https://cdn.staticfile.org/twitter-bootstrap/4.5.0/js/bootstrap.min.js'
        jquery = 'https://cdn.staticfile.org/jquery/3.5.1/jquery.min.js'
        vue = 'https://cdn.staticfile.org/vue/2.6.11/vue.min.js'
        react = 'https://cdn.staticfile.org/react/16.13.1/cjs/react.production.min.js'
        popper = 'https://cdn.staticfile.org/popper.js/2.4.0/umd/popper.min.js'
        marked = 'https://cdn.staticfile.org/marked/1.1.0/marked.min.js'
        jwerty = 'https://cdn.staticfile.org/jwerty/0.3.2/jwerty.min.js'
        font_awesome = 'https://cdn.staticfile.org/font-awesome/5.13.0/js/all.min.js'
        jgrowl = 'https://cdn.staticfile.org/jquery-jgrowl/1.4.7/jquery.jgrowl.min.js'
        alertify = 'https://cdn.staticfile.org/AlertifyJS/1.13.1/alertify.min.js'
        zico = 'http://ico.z01.com/zico.min.js'
        storejs = 'https://cdn.staticfile.org/store.js/2.0.12/store.everything.min.js'

        class highlightjs:
            highlightjs = 'https://cdn.staticfile.org/highlight.js/10.0.3/highlight.min.js'

            class languages:
                java = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/java.min.js'
                javascript = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/javascript.min.js'
                julia = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/julia.min.js'
                kotlin = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/kotlin.min.js'
                makefile = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/makefile.min.js'
                markdown = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/markdown.min.js'
                matlab = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/matlab.min.js'
                php = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/php.min.js'
                python = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/python.min.js'
                c = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/c.min.js'
                c_like = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/c-like.min.js'
                cpp = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/cpp.min.js'
                css = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/css.min.js'
                http = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/http.min.js'
                go = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/go.min.js'
                rust = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/rust.min.js'
                shell = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/shell.min.js'
                ruby = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/ruby.min.js'
                sql = 'https://cdn.staticfile.org/highlight.js/10.0.3/languages/sql.min.js'

    class css:
        bootstrap = 'https://cdn.staticfile.org/twitter-bootstrap/4.5.0/css/bootstrap.min.css'
        font_awesome = 'https://cdn.staticfile.org/font-awesome/5.13.0/css/all.min.css'
        jgrowl = 'https://cdn.staticfile.org/jquery-jgrowl/1.4.7/jquery.jgrowl.min.css'
        alertify = 'https://cdn.staticfile.org/AlertifyJS/1.13.1/css/alertify.min.css'
        zico = 'https://ico.z01.com/zico.min.css'

        class highlightjs:
            default = 'https://cdn.staticfile.org/highlight.js/10.0.3/styles/default.min.css'
            github = 'https://cdn.staticfile.org/highlight.js/10.0.3/styles/github.min.css'
            rainbow = 'https://cdn.staticfile.org/highlight.js/10.0.3/styles/rainbow.min.css'
            ocean = 'https://cdn.staticfile.org/highlight.js/10.0.3/styles/ocean.min.css'
            tomorrow = 'https://cdn.staticfile.org/highlight.js/10.0.3/styles/tomorrow.min.css'

            class atom:
                dark = 'https://cdn.staticfile.org/highlight.js/10.0.3/styles/atom-one-dark.min.css'
                light = 'https://cdn.staticfile.org/highlight.js/10.0.3/styles/atom-one-light.min.css'


class QUrlScript(Script): _attrs = dict(type='text/javascript')


class QStyleLink(Link): _attrs = dict(rel="stylesheet", type="text/css")


class QLinks:
    class bootstrap(QStyleLink): _attrs = dict(href=Urls.css.bootstrap)

    class font_awesome(QStyleLink): _attrs = dict(href=Urls.css.font_awesome)

    class jgrowl(QStyleLink): _attrs = dict(href=Urls.css.jgrowl)

    class alertify(QStyleLink): _attrs = dict(href=Urls.css.alertify)

    class zico(QStyleLink): _attrs = dict(href=Urls.css.zico)


class QScripts:
    class jquery(QUrlScript): _attrs = dict(src=Urls.js.jquery)

    class popper(QUrlScript): _attrs = dict(src=Urls.js.popper)

    class bootstrap(QUrlScript): _attrs = dict(src=Urls.js.bootstrap)

    class jwerty(QUrlScript): _attrs = dict(src=Urls.js.jwerty)

    class font_awesome(QUrlScript): _attrs = dict(src=Urls.js.font_awesome)

    class jgrowl(QUrlScript): _attrs = dict(src=Urls.js.jgrowl)

    class alertify(QUrlScript): _attrs = dict(src=Urls.js.alertify)

    class zico(QUrlScript): _attrs = dict(src=Urls.js.zico)

    class storejs(QUrlScript): _attrs = dict(src=Urls.js.storejs)


class QWindow(Div):
    _attrs = dict(_class='QWindow')

    def __init__(self, width="300px", height="300px", position="static"):
        super().__init__(
            style="width:{width};height:{height};position:{position};background-color:{{blue}};"
                  "border:green 2px solid;color:white;display:flex;".format(width=width, height=height,
                                                                            position=position)
        )
        self.__call__([
            Var(name='content')("This is  a window.")
        ])


class QCenterDiv(Div):
    _attrs = dict(style="text-align:center;")


class QListItem(Div):
    def __init__(self):
        super().__init__(
            style="width:100%;padding:20px;box-sizing:border-box;"
        )


class QList(Div):
    _attrs = dict(_class="QList")

    def __init__(self, color="black"):
        super().__init__(
            style='width:100%;height:100%;overflow:scroll;color:{color};box-sizing:border-box;'.format(color=color)
        )
        self.__call__(
            Var(name="items")([
                QListItem()([
                    QCenterDiv()("This is a demo QListItem.")
                ])
            ])
        )


class QDocument(Html):
    environment = dict(
        blue='#1D93EC'
    )

    def __init__(self):
        super().__init__()
        self.__call__([
            Head()([
                Meta(encoding='utf-8'),
                Title()(
                    Var(name="title", type='text')("Hello World !")
                ),
                QLinks.bootstrap(),
                QScripts.jquery(),
                QScripts.bootstrap(),
            ]),
            Var(name="body")([
                Body()([
                    QWindow(height="150px").compile(
                        content=Form(action='/search')([
                            Input(type="text", placeholder="{{placeholder  or 'Input something.'}}",
                                  name="search-keywords", value="{{input_fill or ''}}"),
                            Button(type='submit')('Search')
                        ])
                    ),
                    QWindow(width="300px", height="400px").compile(
                        content=QList()([
                            Var(name="search_result")([
                                QListItem()("Hi")
                            ])
                        ])
                    )
                ])
            ])
        ])


def html(args):
    default_args = dict(
        title='Html Demo',
        contents=''
    )
    smart_update_dict(default_args, args)
    args = default_args
    return Html()([
        Head()([
            Meta(charset='utf-8'),
            Title()(args['title']),
        ]),
        Body()(args['contents'])
    ])


def form_demo(args={}):
    default_args = dict(
        action='', method='post', style='background-color:#1D93EC;color:white',
        username=dict(type='text', name='username', placeholder='username'),
        password=dict(type='password', name='password', placeholder='password'),
        submit_btn=dict(type='submit', style="background-color:#1D93EC;color:white")
    )
    smart_update_dict(default_args, args)
    args = default_args
    username = args.pop('username')
    password = args.pop('password')
    submit_btn = args.pop('submit_btn')

    return Form(**args)([
        Label()(Input(**username)),
        Label()(Input(**password)),
        Button(**submit_btn)("Submit")
    ])


def demo():
    f = r'D:\work\wk\data/test.html'
    x = Node()('hi')
    # x = html("hi")
    # x = form_demo()
    blue = "#1D93EC"
    x = html(dict(
        contents=[
            Div(style='background-color:{{blue}};color:white;min-height:50px')([
                form_demo(dict(
                    action="http:/127.0.0.1:80/",
                    username=dict(placeholder="input your username...")
                ))
            ])
        ]
    ))
    with open(f, 'w') as fp:
        fp.write(x.render(blue=blue))
    print(x)


def demo2():
    f = r'D:\work\wk\data/test.html'
    doc = QDocument()
    doc.compile()
    x = doc.render()
    doc.to_file(f)
    # with open(f,'w') as fp:
    #     fp.write(x)
    print(x)


if __name__ == '__main__':
    demo2()
