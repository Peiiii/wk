from flask import Flask, request, Blueprint, abort, send_file
from wpkit.web import resources,utils
from wpkit.pan import Pan
from wpkit.web.base import MyBlueprint
from wpkit.web.resources import env
import wpkit

class BlueStatic(MyBlueprint):
    def __init__(self,import_name=None,name='static',url_prefix='/',static_dir='./',template=None,debug=False,**kwargs):
        super().__init__(name=name,import_name=import_name,url_prefix=url_prefix,**kwargs)
        def tprint(*args, **kwargs):
            if debug:
                print('**info:', *args, **kwargs)
        import os
        template = resources.default_templates['files'] if not template else template
        @self.route('/', defaults={'req_path': ''})
        @self.route(utils.join_path('/', '<path:req_path>'))
        def dir_listing(req_path):
            tprint('req_path:',req_path)
            BASE_DIR = static_dir
            # print(static_dir)
            abs_path = os.path.join(BASE_DIR, req_path)
            abs_path=os.path.abspath(abs_path)
            # print(abs_path)
            if not os.path.exists(abs_path):
                return abort(404)
            if os.path.isfile(abs_path):
                # print(abs_path)
                return send_file(abs_path)
            if os.path.isdir(abs_path):
                fns = os.listdir(abs_path)
                fps = [utils.join_path(self.url_prefix,url_prefix, req_path, f) for f in fns]
                return utils.render(open(template, 'r', encoding='utf-8').read(), files=zip(fps, fns))

if __name__ == '__main__':
    BlueStatic(__name__).run()