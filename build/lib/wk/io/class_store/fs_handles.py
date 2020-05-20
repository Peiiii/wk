import os,shutil,glob,json,pickle
from wk.basic import get_relative_path,standard_path,split_path,PowerDirPath,DirPath
from ..fsutils import copy_dir
from .ofiles import ObjectFile,SimpleListFile,SimpleConfigFile,NumberFile,DictFile
class DirDict(object):
    def __init__(self,name=None,realpath=None,*args,**kwargs):
        if realpath and os.path.exists(realpath):
            realpath=os.path.abspath(realpath)
        self.realpath = realpath
        if realpath:
            name=name or os.path.basename(realpath)
        self.name=name
        self.hooked=realpath is not None
    def loadjson(self,fn,encoding='utf-8'):
        path = self.join(fn)
        with open(path,'r',encoding=encoding) as f:
            return json.load(f)
    def dumpjson(self,fn,obj,encoding='utf-8'):
        path=self.join(fn)
        with open(path,'w',encoding=encoding) as f:
            json.dump(obj,f)
    def savetxt(self,fn,string,encoding='utf-8'):
        path=self.join(fn)
        with open(path,'w',encoding=encoding) as f:
            f.write(string)
    def appendTo(self,path):
        if not isinstance(path,DirDict):
            path=DirDict(realpath=path)
        path.append(self)
    def append(self,path):
        if not isinstance(path,DirDict):
            path=DirDict(path)
        if not path.exists():
            self.makedirs(path.name)
        else:
            self.copy(path)
    def copy(self,path):
        assert self.exists()
        if not isinstance(path,DirDict):
            path=DirDict(realpath=path)
        assert path.exists()
        new_path=self.join(path.name)
        assert not os.path.exists(new_path)

        if os.path.isdir(path.realpath):
            copy_dir(path.realpath,new_path)
        else:
            shutil.copy(path.realpath,new_path)
    def makedirs(self,path):
        assert self.hooked
        assert self.exists()
        path = self.join(path)
        os.makedirs(path)
    def mkdir(self,name):
        assert self.hooked
        assert self.exists()
        assert self.secure(name)
        path=self.join(name)
        os.mkdir(path)

    def join(self,path):
        return self.realpath+'/'+path
    def listdir(self):
        return os.listdir(self.realpath)
    def exists(self):
        if not self.realpath:return False
        return os.path.exists(self.realpath)
    def isdir(self):
        return os.path.isdir(self.realpath)
    def isfile(self):
        return os.path.isfile(self.realpath)
    def ismount(self):
        return os.path.ismount(self.realpath)
    def islink(self):
        return os.path.islink(self.realpath)
    def getsize(self):
        return os.path.getsize(self.realpath)
    def getatime(self):
        return os.path.getatime(self.realpath)
    def getmtime(self):
        return os.path.getmtime(self.realpath)
    def getctime(self):
        return os.path.getctime(self.realpath)
    def secure(self,name):
        escapes=['/','\\']
        for ch in escapes:
            if ch in name:
                return False
        return True
    @classmethod
    def from_realpath(cls,path):
        realpath=os.path.abspath(path)
        name=os.path.basename(path)
        return cls(name=name,realpath=realpath)

class FakeOS:
    def __init__(self,path=None):
        if  path and os.path.exists(path):
            path=os.path.abspath(path)
        self.path=standard_path(path) if path else path
    def _relpath(self,root,path):
        return get_relative_path(root,path)
    def _standard_path(self,*args,**kwargs):
        return standard_path(*args,**kwargs)
    def _split_path(self,*args,**kwargs):
        return split_path(*args,**kwargs)
    def _fakepath(self,path):
        return get_relative_path(self.path,path)
    def _truepath(self,path):
        if not self.path:
            return standard_path(path)
        return self.path+'/'+standard_path(path)
    def glob(self,pathname='./',recursive=False):
        pathname=self._truepath(pathname)
        fs=glob.glob(pathname=pathname,recursive=recursive)
        fs=[self._fakepath(path) for path in fs]
        return fs
    def tranverse_info(self,path,depth=-1,format=True):
        return self.info(path,depth,format)
    def info(self, path,depth=2,format=True):
        path = self._truepath(path)
        return PowerDirPath(path).tranverse_info(depth=depth,format=format)
    def open(self, file, mode='r'):
        file = self._truepath(file)
        return open(file, mode)
    def openDB(self,path):
        path=self._truepath(path)
        from wpkit.piu import BackupDB
        return BackupDB(path)
    def openFiledict(self,path):
        path=self._truepath(path)
        from wpkit.piu import FileDict
        return FileDict(path)
    def openObjectfile(self,path):
        path=self._truepath(path)
        return ObjectFile(path)
    def openSimpleListfile(self,path):
        path=self._truepath(path)
        return SimpleListFile(path)
    def openFolder(self,path):
        path=self._truepath(path)
        from wpkit.fsutil import Folder
        return Folder(path)
    def dir(self,name):
        path=self._truepath(name)
        p=PowerDirPath(path)
        p.todir()
        return p
    def file(self,name):
        path = self._truepath(name)
        p = PowerDirPath(path)
        p.tofile()
        return p
    def read(self, fp, mode='r', encoding='utf-8'):
        fp=self._truepath(fp)
        with open(fp, mode=mode, encoding=encoding) as f:
            return f.read()

    def write(self, fp, s, mode='w', encoding='utf-8'):
        fp=self._truepath(fp)
        with open(fp, mode=mode, encoding=encoding) as f:
            f.write(s)
    def newfile(self,path,mode='w',encoding='utf-8'):
        path = self._truepath(path)
        open(path,mode=mode,encoding=encoding).close()
    def writefile(self,path,s,mode='w',encoding='utf-8'):
        path = self._truepath(path)
        open(path,mode=mode,encoding=encoding).write(s)
    def exists(self,path):
        path = self._truepath(path)
        return os.path.exists(path)
    def isdir(self,path):
        path = self._truepath(path)
        return os.path.isdir(path)
    def isfile(self,path):
        path = self._truepath(path)
        return os.path.isfile(path)
    def islink(self,path):
        path = self._truepath(path)
        return os.path.islink(path)
    def ismount(self,path):
        path = self._truepath(path)
        return os.path.ismount(path)
    def dirname(self,path):
        return os.path.dirname(path)
    def basename(self,path):
        return os.path.basename(path)
    def iterfiles(self,path='/'):
        names = self.listdir(path)
        files=[]
        for name in names:
            if self.isfile(name):
                files.append(name)
        pathes = [self.path + '/' + name for name in files]
        return pathes
    def iterpath(self,path='/'):
        names=self.listdir(path)
        pathes=[self.path+'/'+name for name in names]
        return pathes
    def listdir(self,path='/'):
        path=self._truepath(path)
        return os.listdir(path)
    def rmfile(self,path):
        path=self._truepath(path)
        return os.remove(path)
    def remove(self,path):
        if self.isdir(path):
            return self.rmtree(path)
        if self.isfile(path):
            return self.rmfile(path)
    def rmself(self):
        shutil.rmtree(self.path)
    def rmtree(self,path):
        path = self._truepath(path)
        return shutil.rmtree(path)
    def mkdir(self,path):
        path = self._truepath(path)
        return os.mkdir(path)
    def makedirs(self,path):
        path = self._truepath(path)
        return os.makedirs(path)
    def moveto(self,path,overwrite=False):
        if os.path.exists(path):
            if not overwrite:
                raise Exception('%s already exists.'%(path))
            else:
                shutil.rmtree(path)
        # print(self.path,path)
        copy_dir(self.path,path)
    def copy(self,src,dst):
        src = self._truepath(src)
        dst = self._truepath(dst)
        return shutil.copy(src,dst)
    def copydir(self,src,dst):
        src = self._truepath(src)
        dst = self._truepath(dst)
        return copy_dir(src,dst)
    def rename(self,src,dst):
        src = self._truepath(src)
        dst = self._truepath(dst)
        return os.rename(src,dst)
    def move(self,src,dst):
        src = self._truepath(src)
        dst = self._truepath(dst)
        return shutil.move(src,dst)



class FSItem:
    def __repr__(self):
        return '<%s.%s object:%s>'%(self.__module__,self.__class__.__name__,self.path)

class File(FSItem):
    def __init__(self,path,makefile=False):
        self.path=path
        if makefile:
            if not os.path.exists(path):
                open(self.path,'w').close()

class TextFile(File):
    def __init__(self,path,default=''):
        super().__init__(path,makefile=True)
        if self.read()=='':
            self.write(default)
    def read(self):
        with open(self.path,'r',encoding='utf-8') as f:
            return f.read()
    def write(self,s):
        with open(self.path,'w',encoding='utf-8') as f:
            f.write(s)



class Folder(FakeOS,FSItem):
    def __init__(self,path,writable=False):
        self.writable=writable
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            assert os.path.isdir(path)
        path=os.path.abspath(path)
        self.path=path
        FakeOS.__init__(self,path)
    def clean(self):
        for ch in self.listdir():
            if self.isdir(ch):
                self.rmtree(ch)
            else:
                self.remove(ch)
    def eat(self,path,overwrite=False):
        assert os.path.exists(path)
        if os.path.isdir(path):
            copy_dir(path,self.path)
        else:
            copy_file(path,self.path,overwrite=overwrite)


    def parse_path(self,path):
        items=self._split_path(path)
        return items
    def child(self,name):
        assert not '/' in name
        assert not '\\' in name
        path=self.path+'/'+name
        assert os.path.exists(path)
        if os.path.isdir(path):
            return Folder(path)
        elif os.path.isfile(path):
            return File(path)
        else:
            raise Exception('% should be a file or dir'%(path))
    def route_item(self,items):
        if not items:
            return self
        name=items[0]
        items=items[1:]
        if name=='/':
            return self.route_item(items)
        else:
            if name in self.listdir():
                ch=self.child(name)
                if not len(items):
                    return ch
                else:
                    return ch.route_item(items)
            else:
                raise Exception('%s is not in %s'%(name,self.path))
    def __getitem__(self, item):
        items=self.parse_path(item)
        return self.route_item(items)
    def __setitem__(self, path, value):
        tp=self._truepath(path)
        if os.path.exists(tp):
            if self.writable:
                PowerDirPath(tp).rmself()
            else:
                raise Exception('%s already exists.'%(tp))
        if value is None:
            os.makedirs(tp)
            return
        if isinstance(value,str):
            assert os.path.exists(value)
            if os.path.isfile(value):
                value=File(value)
            else:
                assert os.path.isdir(value)
                value=Folder(value)
        if isinstance(value,Folder):
            value.moveto(tp)
        elif isinstance(value,File):
            shutil.copy(value.path,tp)

