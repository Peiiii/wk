from wk import join_path,Pather
import os





class SiteMap(Pather):
    __location__ = '/'

    class Home:
        __title__ = 'home'
    class User:
        login='../login'
    class Admin:
        pass
    class Contents:
        __title__ = 'c'

        class Articles:
            hi2=lambda self:print(self.__location__)
            demo='1345'
            def hi(self):
                print('hi')

        class Documents:
            pass

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


sitemap=SiteMap()

print(sitemap.Contents.structure())


sitemap.Contents.Articles.hi()
sitemap.Contents.Articles.hi2()
print(sitemap.Contents.Articles.demo)
print(sitemap.User.login)
