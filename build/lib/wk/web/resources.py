import pkg_resources, os
from wk.io import load_simple_config
from .utils import SecureDirPath, PointDict, Path, DirPath
from wk import pkg_info
from jinja2 import Environment, PackageLoader, \
    BaseLoader, FileSystemLoader, \
    ChoiceLoader, DictLoader, PrefixLoader

data_path = DirPath(pkg_info.pkg_data_dir)
pkg_data_path = data_path
pkg_static_path = data_path + '/static'
pkg_document_path = pkg_data_path / 'documents'
pkg_templates_dir = DirPath(data_path) / 'templates'
pkg_js_dir = DirPath(data_path) / 'static' / 'js'
pkg_modules_dir = DirPath(data_path)  / 'modules'

default_templates = PointDict.from_dict({
    'welcome': pkg_resources.resource_filename('wk', 'data/templates/welcome.html'),
    'files': pkg_resources.resource_filename('wk', 'data/templates/files.html'),
    'board': pkg_resources.resource_filename('wk', 'data/templates/board.html'),
    'sitemap': pkg_resources.resource_filename('wk', 'data/templates/sitemap.html'),
    'post': pkg_resources.resource_filename('wk', 'data/templates/post.html'),
    'outsite': pkg_resources.resource_filename('wk', 'data/templates/outsite.html')
})
default_static_dir = SecureDirPath(pkg_info.pkg_dir) / 'data' / 'static'


class TemplateLoader:
    def __init__(self, root):
        self.root = root
        self.env=Environment(loader=FileSystemLoader(self.root))
        self.frame_env=Environment(block_start_string='<%',block_end_string='%>',variable_start_string='<@',variable_end_string='@>',loader=FileSystemLoader(self.root))
    def load_frame(self,fn):
        return self.frame_env.get_template(fn).render()
    def load(self, fn):
        return self.env.get_template(fn)
        # return self.frame_env.get_template(fn).render()
    def load_plain(self,fn):
        path = self.root + '/' + fn
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    def subdir(self, name):
        root = self.root + '/' + name
        return TemplateLoader(root)


Parts = TemplateLoader(root=pkg_data_path + "/parts")
Sites = TemplateLoader(root=pkg_static_path + '/sites')


def get_default_template_string(tem):
    return open(default_templates[tem], 'r', encoding='utf-8').read()


env = Environment(loader=PackageLoader('wk.data', 'templates'))
sys_env = env


def get_template_by_name(fn='base'):
    if not '.' in fn: fn += '.html'
    return env.get_template(fn)


def get_template_string_by_name(fn):
    if not fn.endswith('.html'): fn += '.html'
    return (pkg_templates_dir / fn)()


def get_js_string_by_name(fn):
    if not fn.endswith('.js'): fn += '.js'
    return (pkg_js_dir / fn)()

def get_module_environment(name):
    module_path=pkg_modules_dir+'/'+name
    _loader=ChoiceLoader([
        FileSystemLoader(module_path),
        PrefixLoader({
            'pkg':FileSystemLoader(pkg_data_path)
        })
    ])
    env=Environment(loader=_loader)
    return env


def get_env(path=None):
    path = path or './'
    _loader = ChoiceLoader([
        FileSystemLoader(path),
        PrefixLoader({
            'sys': ChoiceLoader([
                FileSystemLoader(data_path + '/static'),
                FileSystemLoader(data_path + '/templates')
            ]),
            'user': ChoiceLoader([
                FileSystemLoader('data/templates'),
                FileSystemLoader('data/user/templates'),
            ])
        }),
        ChoiceLoader([
            FileSystemLoader('data/templates'),
            FileSystemLoader('data/user/templates'),
            FileSystemLoader(data_path + '/static'),
            FileSystemLoader(data_path + '/templates'),
        ])
    ])
    env = Environment(
        loader=_loader
    )
    return env


pkg_tem_loader = ChoiceLoader([
    FileSystemLoader(data_path + '/static'),
    FileSystemLoader(data_path + '/templates')
])
pkg_env = Environment(
    loader=pkg_tem_loader
)


# class Pages:
#     base=pkg_env.get_template('base.html')
#     links=get_template_by_name('links')
#     view_text_file=pkg_env.get_template('view_file.tem')
#     view_markdown_file=pkg_env.get_template('view_md.tem')
def get_one_exist_path(paths):
    for path in paths:
        if os.path.exists(path):
            return path
    return None


def get_exist_template_from_env(env, tems):
    for tem in tems:
        try:
            return env.get_template(tem)
        except:
            pass


def get_page_template(path):
    if os.path.isdir(path):
        dirname = path
        env = get_env(dirname)
        tem = get_exist_template_from_env(env, ['index.page', 'map.tem'])
        return tem
    else:
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        env = get_env(dirname)
        if path.endswith('.page'):
            return env.get_template(basename)


def get_book(path):
    config = load_simple_config(path)
    env = get_env(os.path.dirname(path))
    tem = env.get_template('book.tem')
    os_url = config.get('os_url', '/os')
    book_path = config.get('book_path', './')
    return tem.render(os_url=os_url, book_path=book_path)
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
