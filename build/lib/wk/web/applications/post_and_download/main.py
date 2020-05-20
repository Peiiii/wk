'''
requirements:
Linux with wget installed.
'''
from wpkit.web import utils,resources
from flask import request
from wpkit.web.base import MyBlueprint
import os
class BluePostAndDownload(MyBlueprint):
    add_to_sitemap = True
    url_prefix = '/post_and_download'
    def __init__(self,import_name=None,name='PostAndDownload',data_dir='/var/www/html',url_prefix='/post_and_download',**kwargs):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.download_url = self.url_prefix + '/download'
        super().__init__(name=name,import_name=import_name,url_prefix=url_prefix,**kwargs)
    def register(self, app, options, first_registration=False):
        if not hasattr(app, 'sitemap'):
            app.sitemap = {}
        if self.add_to_sitemap:
            app.sitemap['Download']=self.download_url
        return MyBlueprint.register(self, app, options, first_registration=first_registration)
    def add_handlers(self):
        self.add_static('/download', self.data_dir)
        import wpkit.linux as pylinux
        if utils.pkg_info.is_linux():
            download_func=pylinux.tools.wget_download
        else:
            import wget
            download_func=wget.download

        @self.route('/', methods=['GET'])
        def do_post_get():
            return utils.render(resources.get_default_template_string('post'))

        @self.route('/', methods=['POST'])
        def do_post_post():
            data = request.get_json()
            url = data['url']
            print('get url: %s' % url)
            download_func(url, self.data_dir)
            return 'seccess'
