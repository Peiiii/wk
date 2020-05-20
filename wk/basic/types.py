import os,shutil,glob
class _T(str):
    def __call__(self, s):
        if s.upper()==self or s==self:
            return True
        else:
            return False
CONST_TYPE=_T
class TMetaClass(type):
    def __new__(cls, name, bases, attrs):
        dic=attrs.copy()
        for k,v in attrs.items():
            if isinstance(v,_T):
                dic[k]=_T(k)
        return type.__new__(cls, name, bases, dic)

class T(metaclass=TMetaClass):
    NOT_FOUND=_T()
    NOT_EXISTS=_T()
    NO_VALUE=_T()
    NOT_IMPLEMENTED=_T()
    NOT_ALLOWED=_T()
    EMPTY=_T()
    NO_SUCH_VALUE=_T()
    NO_SUCH_ATTR=_T()
    NOT_GIVEN=_T()
    FOLDER=_T()
    FILE=_T()
    DIR=_T()
    LINK=_T()
    MOUNT=_T()
    IMAGE=_T()
    TEXT=_T()
    VIDEO=_T()
    AUDIO=_T()
    JSON=_T()
    TXT=_T()
    PY=_T()
    JPG=_T()
    PNG=_T()
    JPEG=_T()
    GIF=_T()
    PGM=_T()
    BMP=_T()
    JS=_T()
    MP4=_T()
    AVI=_T()
    IMAGE_FILE_EXTS=[JPG,JPEG,PNG,GIF,PGM,BMP]


class EnumTypeMetaClass(type):
    def __new__(cls, name, bases, attrs):
        dic=attrs.copy()
        for k,v in attrs.items():
            if isinstance(v,_T):
                dic[k]=v
            else:
                dic[k]=_T(k)
        return type.__new__(cls, name, bases, dic)
class WT(metaclass=EnumTypeMetaClass):
    Error=0
def get_file_ext(path):
    name=os.path.basename(path)
    if not '.' in path:return None
    ext=name.rsplit('.',maxsplit=1)[-1]
    if ext=='':ext=None
    return ext
def read_file(path,type=None,encoding=None):
    assert os.path.isfile(path)
    type=type or get_file_ext(path) or 'TXT'
    if type.upper() in T.IMAGE_FILE_EXTS:
        from PIL import Image
        return Image.open(path)
    else:
        if not encoding:
            encoding='utf-8'
        with open(path,'r',encoding=encoding) as f:
            return f.read()

class IterObject(dict):
    __no_value__='<__no_value__>'
    def __getattr__(self, key):
        v=self.get(key,self.__no_value__)
        if v is self.__no_value__:
            self[key]=IterObject()
            return self[key]
        else:
            return v
    def __setattr__(self, key, value):
        self[key]=value

class Path(str):
    __no_value__ = '<__no_value__>'
    def __init__(self,*args,**kwargs):
        super().__init__()
    def __getattr__(self, item):
        return self/item
    def __setattr__(self, key, value):
        self.__dict__[key]=value
    def __truediv__(self, other):
        return Path(self+'/'+other)
    def __call__(self,s=T.NO_VALUE):
        if T.NO_VALUE:return None
        return self/s
    def relative_path(self,path):
        assert path.startswith(self)
        if self=='':
            pass
        else:
            if path.startswith(self):
                path=path[len(self):]
            path=path.lstrip('/')
        return self.__class__(path)

class StrictPath:
    def __init__(self,s):
        self.__value__=Path(self.__strict__(s))
    def __strict__(self,s):
        prefix='/' if s.startswith('/') or s.startswith("\\") else ''
        def remove_all(lis,item):
            if item in lis:
                lis2=lis.copy()
                for i in lis:
                    if i==item:
                        lis2.remove(i)
                return lis2

            else:
                return lis
        lis=s.split('/')
        lis2=[]
        for i in lis:
            lis2+=i.split('\\')
        lis=lis2
        lis=remove_all(lis,'/')
        lis=remove_all(lis,"\\")
        lis=remove_all(lis,'')
        return prefix+'/'.join(lis)
    def __getattr__(self, item):
        return self/item
    def __truediv__(self, other):
        return StrictPath(self.__value__/other).__value__
    def __call__(self, s=''):
        if s=='':return self.__value__
        return StrictPath(self.__value__/s)
    def __repr__(self):
        return "<StrictPath:'%s'>"%(self.__value__)
    def __str__(self):
        return self.__value__
def join_path(*args):
    return StrictPath('/'.join(args))()
def standard_path(p,check=False):
    assert len(p)
    # if (len(p)<=4 and p[1:]=='://') or (len(p)==3 and p[1:]==':/'):return p[:3]
    # print(p)
    p=str(StrictPath(p))
    # print(p)
    # if not '/' in p:return p
    p=p.split('/')
    assert len(p)
    res=[]
    p.reverse()
    while True:
        if not len(p):
            if len(res)>1 and '.' in res:
                for char in res:
                    if char=='.':
                        res.remove(char)
            path='/'.join(res)
            if len(path)==2 and path[1]==':':
                path=path+'/'
            return path
        i=p.pop()
        if i=='':
            res.append('')
            continue
        elif i=='.':
            if not len(res):res.append('.')
        elif i=='..':
            if check:return False
            if not len(res) or res[-1]=='.':raise Exception('Error,path has reached the top when another ".." shew up.')
            else:
                res.pop()
                if not len(res):res.append('.')
        else:res.append(i)
def split_path(path):
    path=standard_path(path)
    items=path.split('/')
    if items[0]=='':
        items[0]='/'
    return items

def join_standard_path(*args):
    path=join_path(*args)
    return standard_path(path)
def get_relative_path(root,child):
    path=child
    path=standard_path(path)
    root=standard_path(root)
    # print("path:,root:",path,root)
    assert path.startswith(root)
    return path[len(root):]
class SecureDirPath(str):

    __no_value__ = '<__no_value__>'
    def __init__(self,s):
        super().__init__()
    def __getattr__(self, item):
        return self/item
    def __truediv__(self, other):
        return SecureDirPath(StrictPath(self+'/'+other))
    def __call__(self):
        assert os.path.exists(self)
        return self.__read__()
    def file(self,fn):
        fp=self/fn
        return fp
    def __read__(self):
        import os
        if os.path.isfile(self):
            with open(self,'r',encoding='utf-8') as f:
                return f.read()
        if os.path.isdir(self):
            return os.listdir(self)

class DirPath(str):
    __type_file__ = T.FILE
    __type_dir__ = T.DIR
    __type_link__ =T.LINK
    __type_mount__=T.MOUNT
    __type_not_exists__=T.NOT_EXISTS
    __no_value__ = T.NO_VALUE
    # __type_file__ = '<type:file>'
    # __type_dir__ = '<type:dir>'
    # __type_link__ = '<type:link>'
    # __type_mount__='<type:mount>'
    # __type_not_exists__='<type:not_exists>'
    # __no_value__ = '<__no_value__>'
    def __init__(self,s):
        super().__init__()
    def __getattr__(self, item):
        return self/item
    def __truediv__(self, other):
        return DirPath(StrictPath(self+'/'+other))
    def __call__(self, s=__no_value__,*args,**kwargs):
        assert os.path.exists(self)
        if s is self.__no_value__:
            return self.__read__(*args,**kwargs)
        else:
            return self.__write__(s,*args,**kwargs)
    def info(self,format=False,with_path=False):
        assert self.exists()
        info=FSItemInfo()
        info.atime=self.getatime()
        info.ctime=self.getctime()
        info.mtime=self.getmtime()
        info.type=self.type()
        info.name=self.basename()
        info.size=os.path.getsize(self)
        if with_path:
            info.path=self.abspath()
        if format:
            info.pretty_format()
        return info
    def tranverse_info(self,depth=-1,format=False):
        info=self.info(format=format)
        if depth==1:
            return info
        if self.isdir():
            info.children={}
            for item in self.children():
                info.children.update({item.basename():item.tranverse_info(depth=depth-1,format=format)})
        return info
    def standard(self):
        return self.__class__(standard_path(self))
    def tranverse_files(self,func):
        from wpkit.fsutil import tranverse_files
        tranverse_files(self,func)
    def tranverse_dirs(self,func):
        from wpkit.fsutil import tranverse_dirs
        tranverse_dirs(self,func)
    def deepglob(self,s,res=[]):
        res+=self.glob(s)
        for d in self.dirs():
            res=d.deepglob(s,res)
        return res
    def glob(self,s):
        fs=glob.glob(self.join_path(s))
        fs=[self.__class__(f) for f in fs]
        return fs
    def children(self):
        children=[self.join_path(item) for item in self.listdir()]
        return children
    def files(self):
        items=[]
        for item in self.children():
            if item.isfile():
                items.append(item)
        return items
    def dirs(self):
        items=[]
        for item in self.children():
            if item.isdir():
                items.append(item)
        return items
    def join_path(self,path):
        return self/path
    def list(self):
        assert self.isdir()
        return os.listdir(self)
    def listdir(self):
        return self.list()
    def type(self):
        if self.isfile():return self.__type_file__
        if self.isdir():return self.__type_dir__
        if self.islink():return self.__type_link__
        if self.ismount():return self.__type_mount__
        return self.__type_not_exists__
    def isfile(self):
        return os.path.isfile(self)
    def isdir(self):
        return os.path.isdir(self)
    def islink(self):
        return os.path.islink(self)
    def ismount(self):
        return os.path.ismount(self)
    def isabs(self):
        return os.path.isabs(self)
    def abspath(self):
        return self.__class__(os.path.abspath(self))
    def lexists(self):
        return os.path.lexists(self)
    def exists(self):
        return os.path.exists(self)
    def basename(self):
        return os.path.basename(self)
    def dirname(self):
        name=os.path.dirname(self) if os.path.dirname(self)!='' else '.'
        return self.__class__(name)
    def getatime(self):
        return os.path.getatime(self)
    def getctime(self):
        return os.path.getctime(self)
    def getmtime(self):
        return os.path.getmtime(self)
    def getsize(self):
        assert self.isfile()
        return os.path.getsize(self)
    def add(self,s):
        assert self.isfile()
        with open(self,'a',encoding='utf-8') as f:
            f.write(s)
        return self
    def file(self,fn,encoding='utf-8'):
        fp=self/fn
        if not os.path.exists(fp):
            with open(fp,'w',encoding=encoding) as f:
                pass
        return fp
    def size(self):
        assert self.isfile()
        return os.path.getsize(self)
    def todir(self):
        if not os.path.exists(self):
            os.makedirs(self)
        else:assert self.isdir()
        return self
    def tofile(self):
        if not os.path.exists(self):
            self.dirname().todir().file(self.basename())
        else:
            assert self.isfile()
        return self
    def __write__(self,s,encoding='utf-8',*args,**kwargs):
        assert os.path.isfile(self) or os.path.isdir(self)
        if os.path.isfile(self):
            with open(self,'w',encoding=encoding) as f:
                f.write(s)
                return self
        else:
            s2 = self / s
            os.mkdir(s2) if not os.path.exists(s2) else None
            return s2
    def __read__(self,*args,**kwargs):
        import os
        if os.path.isfile(self):
            return read_file(self)
        if os.path.isdir(self):
            return os.listdir(self)


class PowerDirPath(DirPath):
    '''
    This class can be very distructive.
    Be Really Careful !!!
    '''
    def rmself(self):
        assert os.path.isdir(self) or os.path.isfile(self)
        if os.path.isdir(self):
            shutil.rmtree(self)
        else:
            os.remove(self)
        return self

    def __truediv__(self, other):
        return PowerDirPath(DirPath(self).__truediv__(other))

class PointDict(dict):
    __no_value__='<__no_value__>'
    def __getattr__(self, key ,default=T.NOT_GIVEN):
        if key in self.keys():
            return self[key]
        elif default!=T.NOT_GIVEN:
            return default
        raise KeyError('No such key named %s'%(key))
    def __setattr__(self, key, value):
        self[key]=value
    def __call__(self, key , value=__no_value__):
        if value is self.__no_value__:
            self[key]=PointDict()
        else:
            self[key]=value
        return self[key]
    def set_attribute(self,key,value):
        self.__dict__[key] = value
    def get_attribute(self,*args,**kwargs):
        return self.__dict__.get(*args,**kwargs)
    def seta(self,**kwargs):
        for k,v in kwargs.items():
            self.set_attribute('__%s__'%(k),v)
    def geta(self,key,*args,**kwargs):
        return self.get_attribute('__%s__'%(key),*args,**kwargs)
    @classmethod
    def from_dict(cls,dic):
        dic2=cls()
        for k,v in dic.items():
            if not isinstance(v,dict):
                dic2[k]=v
            else:
                dic2[k]=cls.from_dict(v)
        return dic2
    def print(self):
        import json
        print(json.dumps(self,sort_keys=True,indent=4))
    def print1(self,depth=0,step=5,space_around_delimiter=1,fillchar=' ',cell_border='|',delimiter=':'):
        import re
        def len_zh(data):
            temp = re.findall('[^a-zA-Z0-9.]+', data)
            count = 0
            for i in temp:
                count += len(i)
            return (count)
        for k,v in self.items():
            for i in range(depth):
                print(fillchar*step,end='')
                print(cell_border,end='')
            print(k.rjust(step-len_zh(k),fillchar),end=' '*space_around_delimiter+delimiter+' '*space_around_delimiter)
            if not isinstance(v,PointDict):
                print(v)
            else:
                print('\n',end='')
                v.print1(depth=depth+1,step=step,space_around_delimiter=space_around_delimiter,
                          cell_border=cell_border,fillchar=fillchar,delimiter=delimiter)
    def pprint1(self):
        self.print1(step=5, space_around_delimiter=0, fillchar='`', cell_border='|', delimiter=':')

class FSItemInfo(PointDict):
    def pretty_format(self):
        self.atime=to_datetime_str(self.atime)
        self.ctime=to_datetime_str(self.ctime)
        self.mtime=to_datetime_str(self.mtime)
        self.size=pretty_format_size(self.size)
        return self


def dir_tree(dir):
    dic=PointDict()
    items=os.listdir(dir)
    for item in items:
        path=dir+'/'+item
        if os.path.isdir(path):
            dic[item]=dir_tree(path)
        else:
            dic[item]=item
    return dic


def pretty_format_size(size):
    def gen_str(size,type):
        if size%1==0:return '%d %s'%(size,type)
        return '%.2f %s'%(size,type)
    def inrange(s):
        if size>=0 and size <1000:
            return True
    if inrange(size):return gen_str(size,'Bytes')
    size/=1024
    if inrange(size):return gen_str(size,'KB')
    size/=1024
    if inrange(size):return gen_str(size,'MB')
    size/=1024
    if inrange(size):return gen_str(size,'GB')
    size/=1024
    if inrange(size):return gen_str(size,'TB')
    size/=1024
    return gen_str(size,'PB')
def to_datetime_str(t):
    import time
    t=time.gmtime(t)
    return time.strftime('%Y-%m-%d %H:%M:%S',t)
class FileDirDict(PointDict):
    __type_file__='<type:file>'
    __type_dir__='<type:dir>'
    __type_link__='<type:link>'
    def set_info(self,info):
        return self.seta(info=info)
    def get_info(self):
        return self.geta('info')
    def info(self,*args,**kwargs):
        if len(args)!=0:
            return self.get_info()[args[0]]
        if len(kwargs)!=0:
            info=self.get_info()
            info.update(**kwargs)
            return self.set_info(info)
        return self.get_info()
    def generate_info(self):
        path=self.path()
        info=path.info()
        info.update(path=path)
        info.update(abspath=path.abspath())
        self.set_info(info)
    def set_type(self,type):
        return self.set_attribute('__type__',type)
    def get_type(self,*args,**kwargs):
        return self.get_attribute('__type__',*args,**kwargs)
    def set_size(self,size):
        return self.set_attribute('__size__',size)
    def get_size(self,*args,**kwargs):
        return self.get_attribute('__size__',*args,**kwargs)
    def get_path(self):
        return self.geta('path')
    def set_path(self,path):
        return self.seta(path=path)
    def path(self):
        return self.get_path()
    def print_size(self):
        print(self.auto_size_str())
    def auto_size_str(self):
        size = self.get_size()
        return self.pretty_format_size(size)
    def pretty_format_size(self,size):
        def gen_str(size,type):
            if size%1==0:return '%d %s'%(size,type)
            return '%.2f %s'%(size,type)
        def inrange(s):
            if size>=0 and size <1000:
                return True
        if inrange(size):return gen_str(size,'Bytes')
        size/=1024
        if inrange(size):return gen_str(size,'KB')
        size/=1024
        if inrange(size):return gen_str(size,'MB')
        size/=1024
        if inrange(size):return gen_str(size,'GB')
        size/=1024
        if inrange(size):return gen_str(size,'TB')
        size/=1024
        return gen_str(size,'PB')
    def size_str(self,type='Bytes'):
        size=self.size_format(type=type)
        if type=='Bytes':
            return '%d %s'%(size,type)
        return '%.2f %s'%(size,type)
    def info_format(self):
        return self.format_info(self.info())
    def format_info(self,info):
        info2=PointDict()
        for fd in ['atime','ctime','mtime']:
            v=info.get(fd,self.__no_value__)
            if v:
                info2[fd]=self.format_time(v)
        fd='size'
        v=info.get(fd,self.__no_value__)
        if v:
            info2[fd] = self.pretty_format_size(v)
        info3=PointDict(info)
        info3.update(info2)
        return info3


    def size_format(self,type='Bytes'):
        size=self.get_size()
        # size=self.size()
        return self.format_size(size=size,type=type)
    def format_time(self,t):
        import time
        t=time.gmtime(t)
        return time.strftime('%Y-%m-%d %H:%M:%S',t)
    def format_size(self,size,type='Bytes'):
        if type=='Bytes':return size
        size/=1024
        if type=='KB':return size
        size/=1024
        if type=='MB':return size
        size/=1024
        if type=='GB':return size
        size/=1024
        if type=='TB':return size
        else:
            raise Exception('Type %s not supported.'%(type))
    def set_face(self,string):
        self.set_attribute('__face__',string)
    def default_face(self):
        items=[]
        for k,v in self.items():
            items.append('%s:%s'%(k,v))
        return '<%s>'%(','.join(items))
    def __repr__(self):
        s=self.get_attribute('__face__',None)
        if s:
            return s
        else:
            return self.default_face()
    def print2(self,depth=0,step=5,space_around_delimiter=0,fillchar=' ',cell_border='|',delimiter=':'):
        import re
        def len_zh(data):
            temp = re.findall('[^a-zA-Z0-9.]+', data)
            count = 0
            for i in temp:
                count += len(i)
            return (count)
        for k,v in self.items():
            for i in range(depth):
                print(fillchar*step,end='')
                print(cell_border,end='')
            print(k.rjust(step-len_zh(k),fillchar),end=' '*space_around_delimiter+delimiter+' '*space_around_delimiter)
            if not isinstance(v,PointDict):
                print(v)
            if v.path().isfile():
                print('\n',end='')
                v.info_format().print1(depth=depth+1,step=step,space_around_delimiter=space_around_delimiter,
                          cell_border=cell_border,fillchar=fillchar,delimiter=delimiter)
            else:
                print('\n',end='')
                v.print2(depth=depth+1,step=step,space_around_delimiter=space_around_delimiter,
                          cell_border=cell_border,fillchar=fillchar,delimiter=delimiter)
    def pprint2(self):
        return self.print2(step=5, space_around_delimiter=0, fillchar='`', cell_border='|', delimiter=':')
class DirTree(FileDirDict):
    def __init__(self,path):
        path=DirPath(path)
        self.set_path(path)
        self.generate_info()
        size=0
        n=0
        N=0
        for item in path():
            n+=1
            p2=path/item
            if p2.isdir():
                self[item]=DirTree(p2)
                N+=self[item].info('N')
            elif p2.isfile():
                N+=1
                file=FileDirDict(name=item)
                file.set_path(p2)
                file.generate_info()
                fsize = p2.getsize()
                file.info(size=fsize)
                file.set_size(size=fsize)
                file.update(size=file.auto_size_str())
                self[item]=file
            size+=self[item].info('size')
        self.info(size=size,n=n,N=N)
    def size(self):
        size=0
        for k,v in self.items():
            path=self.geta('path')/k
            if path.isfile():
                size+=path.size()
            elif path.isdir():
                size+=v.size()
        return size
    def pppprint(self):
        return self.pprint2()

class Status(PointDict):
    def __init__(self,success=True,msg="success",code=0,data=None,*args,**kwargs):
        super().__init__(success=success,msg=msg,code=code,data=data,*args,**kwargs)
class StatusSuccess(Status):
    def __init__(self,success=True,msg="success",code=0,data=None,*args,**kwargs):
        super().__init__(success=success,msg=msg,code=code,data=data,*args,**kwargs)
class StatusError(Status):
    def __init__(self,success=False,msg="failure",code=-1,data=None,*args,**kwargs):
        super().__init__(success=success,msg=msg,code=code,data=data,*args,**kwargs)