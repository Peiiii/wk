from wpkit.web.applications.welcome import BlueWelcomePage
from wpkit.web.applications.sitemap import BlueSitemap
from wpkit.web.applications.post_and_download import BluePostAndDownload
from wpkit.web.applications.fsserver import LocalFSServer
from wpkit.web.applications.dbserver import DBServer
from wpkit.web.applications.pan import BluePan
from wpkit.web.applications.board import BlueBoard
from wpkit.web.applications.static import BlueStatic
from wpkit.web.applications.blogserver import BlogServer
from wpkit.web.applications.osserver import OSServer
# from wpkit.web.applications.all import BlueBoard,DBServer,LocalFSServer,BlueWelcomePage,BlueSitemap,BluePostAndDownload,BluePan
from wpkit.web.base import Application,MyBlueprint
from wpkit.pkg_info import is_linux
from wpkit.web.resources import pkg_document_path
class DemoApp(Application):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.register_blueprint(BlueBoard(url_prefix='/board'))
        self.register_blueprint(DBServer(url_prefix='/db'))
        self.register_blueprint(LocalFSServer(url_prefix='/fs',path="./"))
        self.register_blueprint(BlueWelcomePage(url_prefix='/'))
        self.register_blueprint(BluePan(url_prefix="/pan"))
        self.register_blueprint(OSServer(url_prefix="/os",nickname='OS'))
        self.register_blueprint(BlogServer(url_prefix="/blogs",default_root_path='./data/blogs'))
        self.register_blueprint(BlogServer(url_prefix="/documents",nickname='Documentation',default_root_path=pkg_document_path))
        self.sitemap['Blogs']='/blogs/view='
        self.register_blueprint(BlueSitemap(url_prefix='/sitemap'))

        if is_linux():
            self.register_blueprint(BluePostAndDownload(url_prefix='/post_and_download'))

def demo(port=80,host=None,import_name=None):
    from wpkit.linux import get_local_ip,clean_port
    clean_port(port)
    host=host or get_local_ip()
    app = DemoApp(import_name or "__main__")
    print(app.url_map)
    app.run(port=port,host=host)
if __name__ == '__main__':
    import fire
    fire.Fire(demo)

