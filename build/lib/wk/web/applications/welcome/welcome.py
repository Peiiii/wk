from wpkit.web.base import MyBlueprint
from wpkit.web import utils,resources

class BlueWelcomePage(MyBlueprint):
    # add_to_sitemap = True
    def __init__(self,import_name=None,name='welcome',url_prefix='/welcome',**kwargs):
        super().__init__(name=name,import_name=import_name,url_prefix=url_prefix,add_to_sitemap=False,**kwargs)
        @self.route('/')
        def do_root():
            return resources.get_template_by_name('welcome.tem').render(links=self.app.sitemap)
    def register(self, app, *args,**kwargs):
        self.app=app
        super().register(app,*args,**kwargs)