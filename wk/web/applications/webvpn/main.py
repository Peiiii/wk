from wpkit.web.apputils import *

class Webvpn(MyBlueprint):
    url_prefix = '/webvpn'
    nickname = 'WebVPN'
    add_to_sitemap = True
    def add_handlers(self):
        @self.route('/')
        def do_home():
            headers=request.headers
            print(headers)
            return "Hi"

