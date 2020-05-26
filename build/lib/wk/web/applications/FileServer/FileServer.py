from wk.web import Application,MyBlueprint,request,parse_args
from wk.extra import node
from wk import join_path,FakeOS
from . import pages
import jieba

class FileServer(MyBlueprint):
    url_prefix = '/'
    def __init__(self,import_name,serve_root,*args,**kwargs):
        super().__init__(import_name,*args,**kwargs)
        self.serve_root=serve_root
        self.files_location='/files'
        self.file_engine=FakeOS(self.serve_root)
        self.add_static('/files',self.serve_root)


        @self.route('/', methods=['get'])
        def do_root():
            return pages.SearchPageBase().render()

        @self.route('/search', methods=['post', 'get'])
        @parse_args
        def do_search(search_keywords):
            keywords=[]
            for word in search_keywords.split():
                keywords+=list(jieba.cut(word))
            print(keywords)
            result = self.file_engine.search(keywords)
            # print(result)
            result= [self.file_info(file) for file in result]

            result=[
                pages.FileCard(x) for x in result
            ] or "无结果"
            x = pages.SearchPageBase().compile(search_result=result).render(input_fill=search_keywords)
            return x
    def file_info(self,file):
        url=join_path(self.url_prefix,self.files_location,file)
        info=self.file_engine.info(file)
        info.update(url=url)
        return info
