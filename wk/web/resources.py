import pkg_resources, os
from wk.io import load_simple_config
from .utils import SecureDirPath, PointDict, Path, DirPath
from wk import pkg_info
from jinja2 import Environment, PackageLoader
import jinja2
from jinja2 import Environment, \
        BaseLoader, FileSystemLoader, \
        ChoiceLoader, DictLoader, PrefixLoader

data_path = DirPath(pkg_info.pkg_data_dir)
pkg_data_path=data_path
pkg_document_path=pkg_data_path/'documents'
pkg_templates_dir = DirPath(data_path) / 'templates'
pkg_js_dir = DirPath(data_path) / 'static' / 'js'
default_templates = PointDict.from_dict({
    'welcome': pkg_resources.resource_filename('wpkit', 'data/templates/welcome.html'),
    'files': pkg_resources.resource_filename('wpkit', 'data/templates/files.html'),
    'board': pkg_resources.resource_filename('wpkit', 'data/templates/board.html'),
    'sitemap': pkg_resources.resource_filename('wpkit', 'data/templates/sitemap.html'),
    'post': pkg_resources.resource_filename('wpkit', 'data/templates/post.html'),
    'outsite': pkg_resources.resource_filename('wpkit', 'data/templates/outsite.html')
})
default_static_dir = SecureDirPath(pkg_info.pkg_dir) / 'data' / 'static'


def get_default_template_string(tem):
    return open(default_templates[tem], 'r', encoding='utf-8').read()


env = Environment(loader=PackageLoader('wpkit.data', 'templates'))
sys_env=env

def get_template_by_name(fn='base'):
    if not '.' in fn: fn += '.html'
    return env.get_template(fn)


def get_template_string_by_name(fn):
    if not fn.endswith('.html'): fn += '.html'
    return (pkg_templates_dir / fn)()


def get_js_string_by_name(fn):
    if not fn.endswith('.js'): fn += '.js'
    return (pkg_js_dir / fn)()


def get_env(path=None):
    path=path or './'
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
pkg_tem_loader=ChoiceLoader([
                FileSystemLoader(data_path + '/static'),
                FileSystemLoader(data_path + '/templates')
            ])
pkg_env=Environment(
    loader=pkg_tem_loader
)
class Pages:
    base=pkg_env.get_template('base.html')
    links=get_template_by_name('links')
    view_text_file=pkg_env.get_template('view_file.tem')
    view_markdown_file=pkg_env.get_template('view_md.tem')
def get_one_exist_path(paths):
    for path in paths:
        if os.path.exists(path):
            return path
    return None
def get_exist_template_from_env(env,tems):
    for tem in tems:
        try:
            return env.get_template(tem)
        except:
            pass
def get_page_template(path):
    if os.path.isdir(path):
       dirname=path
       env=get_env(dirname)
       tem=get_exist_template_from_env(env,['index.page','map.tem'])
       return tem
    else:
        dirname=os.path.dirname(path)
        basename=os.path.basename(path)
        env=get_env(dirname)
        if path.endswith('.page'):
            return env.get_template(basename)

def get_book(path):
    config=load_simple_config(path)
    env=get_env(os.path.dirname(path))
    tem=env.get_template('book.tem')
    os_url=config.get('os_url','/os')
    book_path=config.get('book_path','./')
    return tem.render(os_url=os_url,book_path=book_path)
