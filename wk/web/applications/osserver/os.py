from wpkit.fsutil import FakeOS
from wpkit.web.apputils import MyBlueprint,parse_json_and_form,\
    StatusError,StatusSuccess,Status,jsonify,request,\
    get_env,Pages,send_file,get_page_template
import os

class CloudOS(FakeOS):
    def __init__(self, path=None):
        super().__init__(path)
        self.cmd_dict={}
    def execute(self,cmd):
        op=cmd['op']
        params=cmd['params']
        if op in dir(self):
            attr=self.__getattribute__(op)
        else:
            attr=self.cmd_dict[op]
        return attr(*params)
    def add_cmd(self,func):
        import functools
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        self.cmd_dict[func.__name__]=wrapper
        return wrapper
    def savefiles(self,files,dst):
        dst=self._truepath(dst)
        for name,file in files.items():
            fn=dst+'/'+name
            file.save(fn)
    def set_files_url_prefix(self,url_prefix):
        self.files_url_prefix=url_prefix
    def geturl(self,path=None,truepath=None):
        if truepath:
            path=truepath
        else:
            path = self._truepath(path)
        path = self._fakepath(path)
        if path == '.' or path=='/': path = ''
        path = self._standard_path(self.files_url_prefix +"/"+ path)
        return path
    def getfile(self,path):
        path=self._truepath(path)
        return send_file(path)
    def getpage(self,path):
        truepath=self._truepath(path)
        tem=get_page_template(truepath)
        print("page:",tem)
        dir=path if os.path.isdir(path) else os.path.dirname(path)
        fs = self.listdir(dir)

        map = dict({f: self.geturl(dir+'/'+f) for f in fs})
        return tem.render(map=map)



class OSServer(MyBlueprint):
    def __init__(self,url_prefix='/os',default_root_path='./',*args,**kwargs):

        self.root_path=default_root_path
        self.os=CloudOS(self.root_path)
        self.root_path=self.os.path
        self.debug=True
        super().__init__(url_prefix=url_prefix, add_to_sitemap=False, *args, **kwargs)
    def add_handlers(self):
        self.add_static('/files',self.root_path)
        @self.route('/')
        def do_root():

            return Pages.base.render()
        @self.os.add_cmd
        def getpage(path):
            path=self.os._truepath(path)
            tem=get_page_template(path)
            if tem:
                return tem.render()
        self.os.set_files_url_prefix(self.url_prefix+'/files')
        @self.route('/cmd',methods=['GET','POST'])
        @parse_json_and_form
        def do_cmd(cmd):
            print("cmd:",cmd)
            try:
                res = self.os.execute(cmd)
                if cmd['op'] in ['getfile']:
                    return res
                return jsonify(StatusSuccess(data=res))
            except:
                if self.debug:
                    raise
                else:
                    return jsonify(StatusError())
        @self.route('/upload',methods=['GET','POST'])
        @parse_json_and_form
        def do_upload(dst):
            files=request.files
            print("files:",files)
            self.os.savefiles(files,dst)
            return StatusSuccess(msg="Files saved !")

if __name__ == '__main__':
    OSServer(url_prefix='/',default_root_path='./data/os').run()


