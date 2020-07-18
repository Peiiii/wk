# presentation_layer
from wk import web

class PageLoader:

    def __init__(self,sitename='zspt'):
        self.site_env = web.get_site_environment(sitename)
    def article_write_page(self,context={}, *args, **kwargs):
        return self.quick_page('ArticleWritePage.tem', context=context, *args, **kwargs)
    def home_page(self,context={}, *args, **kwargs):
        return self.quick_page('HomePage.tem', context=context, *args, **kwargs)
    def user_home_page(self,context={}, *args, **kwargs):
        return self.quick_page('UserHomePage.tem', context=context, *args, **kwargs)

    def quick_page(self, template, context={}, *args, **kwargs):
        context.update(*args)
        context.update(**kwargs)
        return self.site_env.get_template(template).render(context=context, **kwargs)



