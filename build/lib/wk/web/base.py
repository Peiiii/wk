from flask import Blueprint, Flask, request, send_file, abort, redirect
from wpkit.web.resources import get_template_by_name, default_static_dir
from wpkit.web.utils import join_path, render, rename_func
import uuid, os, logging,inspect,copy


class Application(Flask):
    def __init__(self, import_name=None, enable_CORS=True, host_pkg_resource=True, *args, **kwargs):
        super().__init__(import_name=import_name, *args, **kwargs)
        if enable_CORS:
            try:
                from flask_cors import CORS
                CORS(self, resources=r'/*')
            except:
                logging.warning("CORS is enabled but Flask_cors is not found, install it!")
        self.sitemap = {}
        self.static_map={}
        if host_pkg_resource:
            self.host_pkg_resource()

    def register_blueprint(self, blueprint, url_prefix=None, **options):
        url_prefix = url_prefix or blueprint.url_prefix
        Flask.register_blueprint(self, blueprint, url_prefix=url_prefix, **options)

    def run(self, host="127.0.0.1", port=80, debug=None, load_dotenv=True, **options):
        self.host = host
        self.port = port
        self.debug = debug
        Flask.run(self, host, port, debug, load_dotenv)

    def get_sitemap(self):
        return self.sitemap
    def host_pkg_resource(self):
        self.add_static(url_prefix="/pkg-resource", static_dir=default_static_dir)

    def add_static(self, url_prefix='/files', static_dir='./'):
        self.config_statics({url_prefix: static_dir})

    def config_statics(self, static_map={}):
        self.host_statics(static_map)

    def host_statics(self, static_map={}):
        self.static_map.update(static_map)
        for k, v in static_map.items():
            self._add_static(url_prefix=k, static_dir=v)

    def _add_static(self, url_prefix='/files', static_dir='./', template=None):
        template = get_template_by_name("files") if not template else template
        url_prefix = url_prefix.rstrip('/')

        @self.route(url_prefix + '/', defaults={'req_path': ''})
        @self.route(url_prefix + join_path('/', '<path:req_path>'))
        @rename_func("dir_listing_" + uuid.uuid4().hex)
        def dir_listing(req_path):
            BASE_DIR = static_dir
            abs_path = os.path.join(BASE_DIR, req_path)
            abs_path=os.path.abspath(abs_path)
            if not os.path.exists(abs_path):
                return abort(404)
            if os.path.isfile(abs_path):
                return send_file(abs_path)
            if os.path.isdir(abs_path):
                fns = os.listdir(abs_path)
                fps = [join_path(url_prefix, req_path, f) for f in fns]
                return template.render(files=zip(fps, fns))



class PredfinedKeysMetaClass(type):
    def __new__(cls, name ,bases,attrs):
        key='__predefined_keys__'
        last_base=bases[-1]
        if hasattr(last_base,key):
            base_dic=getattr(last_base,key)
        else:
            base_dic={}
        dic=copy.deepcopy(base_dic)
        for k,v in attrs.items():
            if not inspect.isfunction(v):
                if not k.startswith('__'):
                    dic[k]=v
        attrs[key]=dic
        return type.__new__(cls,name,bases,attrs)
class BpAtrribute:
    def __init__(self,obj=None,inherit=True,run_when_making_class=False):
        self.obj=obj
        if obj is not None:
            inherit=False
        self.inherit=inherit
        self.run_when_making_class=run_when_making_class
class MyBlueprint(Blueprint,metaclass=PredfinedKeysMetaClass):
    import_name = None
    name = None
    add_to_sitemap = False
    url_prefix = None
    host_pkg_resource = True
    static_map = {}
    nickname = None
    enable_CORS = True
    def __init__(self, import_name=None, name=None,add_to_sitemap=None, url_prefix=None, host_pkg_resource=None, static_map={},
                 nickname=None, enable_CORS=None, **kwargs):


        predefined_keys=copy.deepcopy(self.__predefined_keys__)
        # print(predefined_keys)
        arg_dict=dict(import_name=import_name,name=name,add_to_sitemap=add_to_sitemap, url_prefix=url_prefix,
                      host_pkg_resource=host_pkg_resource, static_map=static_map,
                 nickname=nickname, enable_CORS=enable_CORS)
        res_dict={}
        for k,v in arg_dict.items():
            if isinstance(v,dict):
                pre_val=predefined_keys.get(k,None) or {}
                v = v or {}
                v.update(pre_val)
                res_dict[k]=v
            else:
                if v is not None:
                    res_dict[k]=v
                else:
                    res_dict[k]=predefined_keys.get(k,None)
        # print(res_dict)
        import_name=res_dict['import_name']
        name=res_dict['name']
        add_to_sitemap=res_dict['add_to_sitemap']
        url_prefix=res_dict['url_prefix']
        host_pkg_resource=res_dict['host_pkg_resource']
        static_map=res_dict['static_map']
        nickname=res_dict['nickname']
        enable_CORS=res_dict['enable_CORS']

        if not import_name: import_name = "__main__"
        if not name: name = self.__class__.__name__ + uuid.uuid4().hex
        super().__init__(name=name, import_name=import_name, url_prefix=url_prefix, **kwargs)
        self.static_map = {}
        self.nickname = nickname
        self.blueprints={}
        self._blueprint_order=[]
        self.add_to_sitemap=add_to_sitemap
        self.visit_link=None
        self.host_statics(static_map)
        self.enable_CORS = enable_CORS
        if host_pkg_resource:
            self.host_pkg_resource()
        self.app = Application(self.import_name, enable_CORS=self.enable_CORS)
        self.add_handlers()

    def add_handlers(self):
        pass
    def get_visit_link(self):
        pass
    def get_url(self,url=''):
        from wpkit.basic import standard_path
        return standard_path(self.url_prefix+'/'+url)
    def register(self, app, options, first_registration=False):
        if not hasattr(app, 'sitemap'):
            app.sitemap = {}
        self.app=app
        name = self.nickname if self.nickname else self.name
        if self.add_to_sitemap:
            app.sitemap[name] =self.get_visit_link() or self.visit_link or self.url_prefix
        Blueprint.register(self, app, options, first_registration)

    def run(self, host="127.0.0.1", port=80, debug=True, show_url_map=True):
        self.host = host
        self.port = port
        self.debug = debug
        self.app.register_blueprint(self, url_prefix=self.url_prefix)
        if show_url_map:
            print(self.app.url_map)
        self.app.run(host=host, port=port, debug=self.debug)

    def host_pkg_resource(self):
        self.add_static(url_prefix="/pkg-resource", static_dir=default_static_dir)

    def add_static(self, url_prefix='/files', static_dir='./'):
        self.config_statics({url_prefix: static_dir})

    def config_statics(self, static_map={}):
        self.host_statics(static_map)

    def host_statics(self, static_map={}):
        self.static_map.update(static_map)
        for k, v in static_map.items():
            self._add_static(url_prefix=k, static_dir=v)

    def _add_static(self, url_prefix='/files', static_dir='./', template=None):
        template = get_template_by_name("files") if not template else template
        url_prefix = url_prefix.rstrip('/')
        @self.route(url_prefix + '/', defaults={'req_path': ''})
        @self.route(url_prefix + join_path('/', '<path:req_path>'))
        @rename_func("dir_listing_" + uuid.uuid4().hex)
        def dir_listing(req_path):
            # print("req_path:",req_path)
            BASE_DIR = static_dir
            abs_path = os.path.join(BASE_DIR, req_path)
            abs_path=os.path.abspath(abs_path)
            # print(BASE_DIR,abs_path)
            if not os.path.exists(abs_path):
                return abort(404)
            if os.path.isfile(abs_path):
                return send_file(abs_path)
            if os.path.isdir(abs_path):
                fns = os.listdir(abs_path)
                fps = [join_path(self.url_prefix, url_prefix, req_path, f) for f in fns]
                return template.render(files=zip(fps, fns))


if __name__ == '__main__':
    bp = MyBlueprint(__name__, url_prefix='/', static_map={"/": "../../"})
    app = Application(__name__)
    app.register_blueprint(bp, url_prefix='/files')
    app.run()
