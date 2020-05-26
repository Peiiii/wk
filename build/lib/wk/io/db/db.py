


import json,os,shutil
# from collections import deque
# from uuid import uuid4
from wk.basic import T,PointDict,PowerDirPath,Status,StatusSuccess,StatusError
from ..ioutils import json_load,json_dump

class Piu:
    def __init__(self,path='./db'):
        self.dbpath=path
        self.dicpath=os.path.join(self.dbpath,'data.dic')
        self.dic=self.setup()
    def setup(self):
        if self._exists():return json_load(self.dicpath)
        return self._make()
    def keys(self):
        return self.dic.keys()
    def values(self):
        return self.dic.values()
    def items(self):
        return self.dic.items()
    def add(self, *args, **kwargs):
        assert len(args) == 0 or len(args) == 2
        if len(args):
            assert isinstance(args[0], str)
            kwargs.update({args[0]: args[1]})
        self.dic.update(**kwargs)
        self._save()
    def set(self, *args, **kwargs):
        assert len(args) == 0 or len(args) == 2
        if len(args):
            assert isinstance(args[0], str)
            kwargs.update({args[0]: args[1]})
        self.dic.update(**kwargs)
        self._save()
    def delete(self,key):
        del self.dic[key]
        self._save()
    def get(self,*args,**kwargs):
        return self.dic.get(*args,**kwargs)
    def _save(self):
        json_dump(self.dic,self.dicpath)
    def _exists(self):
        if os.path.exists(self.dbpath) and os.path.exists(self.dicpath):
            return True
        return False
    def _make(self):
        dir=self.dbpath
        shutil.rmtree(dir) if os.path.exists(dir) else None
        os.makedirs(dir)
        dic={}
        json_dump(dic,self.dicpath)
        return dic
class FileDict(PointDict):
    def __init__(self,path):
        self.seta(path=path)
        path = PowerDirPath(self.geta('path'))
        if path.exists():
            assert path.isfile()
            dic=json_load(path)
            assert isinstance(dic,dict)
        else:
            dic={}
            path.tofile()
            json_dump(dic,path,indent=4)
        super().__init__(dic)
    def __setattr__(self, key, value):
        PointDict.__setattr__(self,key,value)
        self._save()
    def __setitem__(self, key, value):
        PointDict.__setitem__(self,key,value)
        self._save()
    def update(self,*args,**kwargs):
        for k,v in kwargs.items():
            self[k]=v
        for arg in args:
            self.update(**arg)
    def _save(self):
        json_dump(self,self.geta('path'),indent=4)




class BackupDB(PointDict):
    def __init__(self, path='./db',ignore_duplicated=True,max_depth=10):
        self.dbpath = path
        self.dicpath = os.path.join(self.dbpath, 'data.json')
        self.configfile=os.path.join(self.dbpath,'config.json')
        self.dic = self.setup()
        self.config=self.setup_configfile()
        self.config.update(ignore_duplicated=ignore_duplicated,max_depth=max_depth)
        self.load_config()
    def setup_configfile(self):
        config=FileDict(self.configfile)
        return config
    def load_config(self):
        for k,v in self.config.items():
            self[k]=v
    def setup(self):
        if self._exists(): return json_load(self.dicpath)
        return self._make()
    def set(self,*args,**kwargs):
        return self.add(*args,**kwargs)
    def add(self, *args, **kwargs):
        assert len(args) == 0 or len(args) == 2
        if len(args):
            assert isinstance(args[0], str)
            kwargs.update({args[0]: args[1]})
        for k,v in kwargs.items():
            if k not in self.dic.keys():
                self.dic[k] = [v]
            elif self.ignore_duplicated and v==self.dic[k][-1]:
                continue
            else:
                self.dic[k].append(v)
                if len(self.dic[k])>self.max_depth:
                    self.dic[k]=self.dic[k][1:]
        self._save()

    def delete(self, key):
        del self.dic[key]
        self._save()

    def get(self,k, default=T.NOT_GIVEN):
        if k not in self.dic.keys():
            if default==T.NOT_GIVEN:
                raise KeyError('No such key named %s'%(k))
            else:
                return default
        return self.dic[k][-1]

    def recover(self,key,step=1):
        assert key in self.dic.keys()
        assert len(self.dic[key])>step
        return self.dic[key].pop()
    def _save(self):
        json_dump(self.dic, self.dicpath,indent=4)

    def _exists(self):
        if os.path.exists(self.dbpath) and os.path.exists(self.dicpath):
            return True
        return False

    def _make(self):
        dir = self.dbpath
        shutil.rmtree(dir) if os.path.exists(dir) else None
        os.makedirs(dir)
        dic = {}
        json_dump(dic, self.dicpath,indent=4)
        return dic
    def execute(self,cmd):
        cmd=PointDict.from_dict(cmd)
        op,params=cmd.op,cmd.params
        if op=='add':
            res=self.add(params['key'],params['value'])
        elif op=='set':
            res=self.set(params['key'],params['value'])
        elif op=='get':
            res=self.get(params['key'],params.get('default',None))
        elif op=='delete':
            res=self.delete(params['key'])
        else:
            assert op=='recover'
            res=self.recover(params['key'],params['step'])
        return res
RecordClassDict={}
class RecordMataClass(type):
    def __new__(cls, name, bases, attrs):
        attrs['__record_type__']=name
        new_cls=type.__new__(cls, name, bases, attrs)
        RecordClassDict[name]=new_cls
        return new_cls
class Record(metaclass=RecordMataClass):
    require_init=False
    require_recover = False
    def __init__(self,dic=None,**kwargs):
        if dic:
            assert isinstance(dic,dict)
            kwargs.update(dic)
        self.seta(dic=kwargs)
    def jsonvalue(self):
        return self.geta('dic')
    def __repr__(self):
        return '%s(%s)'%(self.__class__.__name__,','.join(['%s=%s'%(k,v) for k,v in self.geta('dic').items()]))
    def todict(self):
        dic={
            '@is_record':True,'@record_type':self.__record_type__,'@value':self.jsonvalue()
        }
        return dic
    @classmethod
    def fromdict(cls,dic):
        return cls(**dic)
    def keys(self):
        return self.geta('dic').keys()
    def values(self):
        return self.geta('dic').values()
    def items(self):
        return self.geta('dic').items()
    def __getattr__(self, key ,default=T.NOT_GIVEN):
        return self.geta('dic').get(key,default)
    def __setattr__(self, key, value):
        self.geta('dic')[key]=value
    def set_attribute(self,key,value):
        self.__dict__[key] = value
    def get_attribute(self,*args,**kwargs):
        return self.__dict__.get(*args,**kwargs)
    def seta(self,**kwargs):
        for k,v in kwargs.items():
            self.set_attribute('__%s__'%(k),v)
    def geta(self,key,*args,**kwargs):
        return self.get_attribute('__%s__'%(key),*args,**kwargs)
class PlainRecord(Record):
    def __init__(self,obj,*args,**kwargs):
        self.seta(obj=obj)
        super().__init__(*args,**kwargs)
    def jsonvalue(self):
        return self.geta('obj')
    def __repr__(self):
        return self.geta('obj').__repr__()
    @classmethod
    def fromdict(cls,dic):
        return cls(dic)
class JsonRecord(Record):
    pass
class LinkRecord(Record):
    def __repr__(self):
        return '%s<%s>'%(self.__class__.__name__,','.join(['%s=%s'%(k,v) for k,v in self.geta('dic').items()]))
class FileRecord(LinkRecord):
    require_init = True
    require_recover=True
    def __init__(self,fname=None,fid=None,content=None,encoding='utf-8',*args,**kwargs):
        assert fid or content
        kwargs.update(fname=fname,fid=fid,encoding=encoding)
        if content:self.seta(content=content)
        super().__init__(*args,**kwargs)
    def init(self,key):
        self.seta(helper=key)
        content=self.geta('content',None)
        fid=self.fid
        if fid and content:# write to file
            fp=key.gen_filepath(fid)
            PowerDirPath(fp).tofile()(content,encoding=self.encoding)
        elif fid and not content:# read file
            assert key.get_filepath(fid)
        elif not fid and content:# write to file
            self.fid=key.gen_fid()
            fp=key.gen_filepath(self.fid)
            PowerDirPath(fp).tofile()(content,encoding=self.encoding)
        else:# no file, no content
            raise Exception('Error:File record needs fid or content to be given.')
    def recover(self,helper):
        self.seta(helper=helper)
    def __call__(self, *args, **kwargs):
        helper= self.geta('helper')
        fp=helper.get_filepath(self.fid)
        # print(fp)
        if fp:return PowerDirPath(fp)(*args,**kwargs)

class ImageRecord(FileRecord):
    pass

def record_default(obj):
    return obj.todict() if 'todict' in dir(obj) else obj
def record_hook(dic):
    for key,value in dic.items():
        if isinstance(value,dict):
            if value.get('@is_record', None) and value.get('@record_type', T.NOT_FOUND) != T.NOT_FOUND:
                type = value['@record_type']
                assert type in RecordClassDict.keys()
                cls = RecordClassDict[type]
                new_value = cls.fromdict(value['@value'])
                dic[key]=new_value
    return dic
class FileStorageHelper(Piu):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.filesdir=PowerDirPath(os.path.join(self.dbpath,'files'))
        self.filesdir.todir()
        # print('piu build up...:\nfids:',self.get('fids:'))
        if not self.get('fids',None):self.add(fids=[])
        if  self.get('first_fid',T.NOT_EXISTS)==T.NOT_EXISTS:self.add(first_id='0')
        if not self.get('last_fid',None):self.add(last_fid=self.get('first_fid'))
    def add_fid(self,fid):
        fids = self.get('fids')
        fids.append(fid)
        self.add(last_fid=fid)
        self.add(fids=fids)
    def gen_fid(self):
        last_fid= int(self.get('last_fid'))
        last_fid = str(last_fid + 1)
        self.add(last_fid=last_fid)
        self.add_fid(last_fid)
        # print('new fids:',self.get('fids'))
        return last_fid
    def get_filepath(self,fid):
        # print(self.get('last_fid'))
        return self.filesdir/fid if fid in self.get('fids') else None
    def gen_filepath(self,fid):
        self.add_fid(fid) if not fid in self.get('fids') else None
        return self.filesdir/fid

class Table(PointDict):
    def __init__(self, path='./db'):
        self.dbpath = path
        self.dicpath = os.path.join(self.dbpath, 'data.json')
        self.configfile=os.path.join(self.dbpath,'config.json')
        self.dic = self.setup()
        self.config=self.setup_configfile()
        self.config.update()
        self.load_config()
        self.helper=FileStorageHelper(os.path.join(self.dbpath,'FileStorageHelper'))
    def setup_configfile(self):
        config=FileDict(self.configfile)
        return config
    def load_config(self):
        for k,v in self.config.items():
            self[k]=v
    def setup(self):
        if self._exists(): return json_load(self.dicpath,object_hook=record_hook)
        return self._make()

    def add(self, *args, **kwargs):
        assert len(args)==0 or len(args)==2
        if len(args):
            assert isinstance(args[0],str)
            kwargs.update({args[0]:args[1]})
        for k,v in kwargs.items():
            if not isinstance(v,Record):v=PlainRecord(v)
            if v.require_init: # for example: FileRecord needs to be initialized.
                v.init(self.helper)
            self.dic[k] = v
        self._save()
    def set(self,*args,**kwargs):
        return self.add(*args,**kwargs)
    def delete(self, key):
        del self.dic[key]
        self._save()

    def get(self,k, default=T.NOT_GIVEN):
        if k not in self.dic.keys():
            if default==T.NOT_GIVEN:
                raise KeyError('No such key named %s'%(k))
            else:
                return default
        v= self.dic[k]
        if v.require_recover:v.recover(self.helper)
        return v

    def _save(self):
        json_dump(self.dic, self.dicpath,indent=4,default=record_default)

    def _exists(self):
        if os.path.exists(self.dbpath) and os.path.exists(self.dicpath):
            return True
        return False

    def _make(self):
        dir = self.dbpath
        shutil.rmtree(dir) if os.path.exists(dir) else None
        os.makedirs(dir)
        dic = {}
        json_dump(dic, self.dicpath,indent=4)
        return dic

def demo():
    P = Piu()
    P.add('a', 13)
    P.add('name', 'wangpei')
    P.add('age', 21)
    P.delete('a')
    age = P.get('age')
    print(age)
    x = P.get('x', 30)
    print(x)
if __name__ == '__main__':
    demo()

