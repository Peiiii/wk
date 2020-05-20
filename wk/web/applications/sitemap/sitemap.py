from wpkit.web.base import  MyBlueprint
from wpkit.web import utils,resources
class BlueSitemap(MyBlueprint):
    def __init__(self,import_name=None,name='sitemap',sitemap={},url_prefix='/sitemap',**kwargs):
        super().__init__(name=name,import_name=import_name,url_prefix=url_prefix,add_to_sitemap=False,**kwargs)
        @self.route('/')
        def do_root():
            temf = resources.default_templates['sitemap']
            return utils.render(open(temf, 'r', encoding='utf-8').read(), sitemap=self.get_sitemap())
    def register(self, app,*args,**kwargs):
        def get_sitemap():
            return app.sitemap
        self.get_sitemap=get_sitemap
        return MyBlueprint.register(self,app,*args,**kwargs)