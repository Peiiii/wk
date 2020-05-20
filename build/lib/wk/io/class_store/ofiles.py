import os,shutil,glob,json
from .. ioutils import json_dump,json_load,read_txt,write_txt,read_config,write_config

class ObjectFile:
    def __init__(self,path,default=None):
        self.path=path
        if not os.path.exists(path):
            open(path,'w').close()
        if self.is_empty():
            self.write(default)
    def is_empty(self):
        with open(self.path) as f:
            s=f.read()
            if s=='':
                return True
        return False
    def __call__(self, obj=None):
        if obj is None:
            return self.read()
        return self.write(obj)
    def read(self):
        return json_load(self.path)
    def write(self,obj):
        return json_dump(obj, self.path)
class SimpleListFile(ObjectFile):
    def __init__(self,path,split_char='\n'):
        self.path=path
        self.split_char=split_char
        super().__init__(self.path,default=[])
    def write(self,obj):
        obj=self.split_char.join(obj)
        return write_txt(obj,self.path)
    def read(self):
        text=read_txt(self.path).strip()
        return text.split(self.split_char)
class DictFile(dict):
    def __init__(self,path):
        self.path=path
        if path.exists():
            assert os.path.isfile(path)
            dic=json_load(path)
            assert isinstance(dic,dict)
        else:
            dic={}
            open(path,'w').close()
            json_dump(dic,path,indent=4)
        super().__init__(dic)
    def __setattr__(self, key, value):
        dict.__setattr__(self,key,value)
        self._save()
    def __setitem__(self, key, value):
        dict.__setitem__(self,key,value)
        self._save()
    def update(self,*args,**kwargs):
        for k,v in kwargs.items():
            self[k]=v
        for arg in args:
            self.update(**arg)
    def _save(self):
        json_dump(self,self.path,indent=4)

class SimpleConfigFile(dict):
    def __init__(self,path,splitchar='=',comment_tag='#',sync=True):
        self.path=path
        self.splitchar=splitchar
        self.sync=sync
        super().__init__(read_config(path,splitchar=splitchar,comment_tag=comment_tag))
    def __setitem__(self, key, value):
        res=dict.__setitem__(self,key,value)
        if self.sync:
            self._save()
        return res
    def save(self):
        return self._save()
    def _save(self):
        return self.write()
    def write(self):
        write_config(self,self.path,splitchar=self.splitchar)

class NumberFile(ObjectFile):
    def __init__(self,path,default=0):
        super().__init__(path,default)
