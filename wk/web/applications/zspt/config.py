from wk import Pather



def create_sitemap(url_prefix,site_data_dir_name):
    class Sitemap(Pather):
        __location__ = url_prefix

        class Home:
            __title__ = ''

        class Api:
            class Validation:
                send_sms_url = 'sms'
                send_email_url = 'email'

        class Auth:
            class Qq:
                class Callback:
                    pass

        class User:
            login = '../login'
            logout = '../logout'
            register = '../register'

            class Home: pass

        class Admin:
            pass

        class Assets:
            class Css: pass

            class Imgs: pass

            class Js: pass

            class Pkgs: pass

            class Site:
                __title__ = 'sites/' + site_data_dir_name

        class Contents:
            class Articles:
                new='write'
                edit='write'

            class Documents:
                new ='upload'

            class Collections:
                pass

            class Entries:
                pass

            class Videos:
                pass

            class Questions:
                pass

            class Answers:
                pass

            class KnowledgeCards:
                pass

            class MindMaps:
                pass

            class Notes:
                pass
    return Sitemap()
