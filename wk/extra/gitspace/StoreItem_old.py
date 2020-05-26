from .GitRepo import default_remote_location,GitRepo,is_git_dir
from wpkit.fsutil import Folder,copy_file,copy_dir,copy_fsitem,remove_fsitem,is_empty_dir
from wpkit.piu import FileDict
from wpkit.basic import T,TMetaClass,CONST_TYPE
import os,shutil,glob,uuid,random
from wpkit.ofile import SimpleListFile
_T=CONST_TYPE
class CONST(metaclass=TMetaClass):
    remote_branch_list=_T()
    master=_T()
    empty=_T()

# TODO: improve performance


class StoreItem(Folder):
    '''
    issue: Branch name has a limit
    '''
    delimiter='.-.'
    special_branches = ['master', 'empty', 'remote_branch_list']
    legal_path_chars = [str(i) for i in range(10)]+[chr(i) for i in range(65, 91)]+[chr(i) for i in range(97, 123)]+list('._-')
    def status(self,repo=None):
        repo=repo or self.repo
        from wpkit.basic import PointDict
        info=PointDict(
            current_branch=repo.active_branch(),
            local_branches=repo.branch_list(),
            status=repo.status()
        )
        print(info)
        return info
    def __init__(self,path,remote_location=None,remote_branch=None):
        remote_location = remote_location or default_remote_location
        assert remote_branch
        if not os.path.exists(path):
            os.makedirs(path)
        path=os.path.abspath(path)
        Folder.__init__(self,path)
        if is_git_dir(path):
            repo=GitRepo(path)
        else:
            repo=GitRepo.init(path)
        self.repo=repo
        self.path=path
        self.remote_location=remote_location or default_remote_location
        self.remote_branch=remote_branch
        self.data_list=['.git','.type.store'] # clean except
        self.info_list=['.git','.type.store','.more.store']  # copy except
        self.typefile=self.openFiledict('.type.store')

        self.init_branches()
        print("Init StoreFolder finished.")
    def _try_pull_remote(self):
        try:
            self._pull_remote()
        except:
            import logging
            logging.warning("Can't pull remote branch %s , maybe because local branch has already been updates."%(self.remote_branch))
    def _pull_remote(self):
        repo=self.repo
        repo.pull(self.remote_location,self.remote_branch)
    def _push_self(self):
        repo=self.repo
        repo.add_all()
        repo.commit()
        repo.push(self.remote_location,self.remote_branch)
    def _push_if_not_exists(self):
        if not self.remote_branch in self._read_remote_branch_list():
            self._push_self()
    def _pull_else_push_self(self):
        remote_branch=self.remote_branch
        if not remote_branch in self._read_remote_branch_list():
            self._push_self()
        else:
            self._try_pull_remote()


    def _pull_remote_branch_list(self,repo=None,remote_location=None,remote_branch='remote_branch_list',hard=False):
        repo=repo or self.repo
        remote_location=remote_location or self.remote_location
        pull=False
        if not 'remote_branch_list' in repo.branch_list():
            repo.branch_create('remote_branch_list')
            pull=True
        if hard:
            pull=True
        if pull:
            try:
                br = repo.active_branch()
                repo.checkout_branch('remote_branch_list')
                repo.clean()
                repo.add_all()
                repo.commit()
                repo.pull(remote_location, branch=remote_branch)
                repo.checkout_branch(br)
            except:
                print("Can't pull remote_branch_list, maybe because local branch is already updated.")

    def init_branches(self,repo=None):
        '''
        A store repo has 3 branches: master , empty , remote_branch_list, remote_branch
        '''
        repo=repo or self.repo
        if not repo.branch_list():
            repo.commit() # create master
        if not 'empty' in repo.branch_list():
            repo.branch_create('empty')
            repo.checkout_branch('empty')
            repo.clean()
            repo.commit()
            repo.checkout_branch('master')
        if not self.remote_branch in repo.branch_list():
            repo.branch_create(self.remote_branch)
            repo.checkout_branch(self.remote_branch)
            repo.clean()
            repo.commit()
            repo.checkout_branch('master')
        self._pull_remote_branch_list(hard=False)
        repo.checkout_branch(self.remote_branch)

    def _read_remote_branch_list(self,pull=False):
        repo=self.repo
        br = repo.active_branch()
        repo.checkout_branch(CONST.remote_branch_list)
        if pull:
            self._pull_remote_branch_list(repo)
        lf = self.openSimplelistfile(CONST.remote_branch_list)
        li = lf.read()
        repo.checkout_branch(br)
        return li
    def _add_to_remote_branch_list(self,branch):
        repo=self.repo
        br=repo.active_branch()
        self._pull_remote_branch_list(hard=True)
        repo.checkout_branch(CONST.remote_branch_list)
        # repo.pull(self.remote_location,CONST.remote_branch_list)
        lf=self.openSimplelistfile(CONST.remote_branch_list)
        li=lf.read()
        # print("original:",li)
        li.append(branch)
        li=list(set(li))
        # print("now:",li)
        lf.write(li)
        repo.add_all()
        repo.commit()
        repo.push(self.remote_location,CONST.remote_branch_list)
        repo.checkout_branch(br)
    def iter_contentpath(self):
        lis=[]
        for name in self.listdir():
            if name in self.info_list:
                continue
            else:
                path=self.path+'/'+name
                lis.append(path)
        return lis
    def set_type(self,type):
        self.typefile.type=type
        return type
    def get_type(self):
        if not self.typefile.get('type'):
            return None
        return self.typefile.type
    @classmethod
    def pull(cls,remote_location=None,remote_branch=None,path=None,overwrite=False):
        '''
        Make sure dirs,branch exist,pull from remote
        '''
        remote_location=remote_location or default_remote_location
        remote_branch=remote_branch or 'master'
        if os.path.exists(path) and len(os.listdir(path)):
            if overwrite:
                shutil.rmtree(path)
            else:
                raise FileExistsError("Can't pull because folder %s is not empty."%(path))
        if not os.path.exists(path):
            os.makedirs(path)
        repo=GitRepo.init(path)
        if not repo.branch_list():
            repo.add_all()
            repo.commit()
        if not remote_branch in repo.branch_list():
            repo.branch_create(remote_branch)
            repo.checkout_branch(remote_branch)
            repo.clean()
        repo.pull(remote_location,branch=remote_branch)
        item=cls(repo.path,remote_location=remote_location,remote_branch=remote_branch)
        type=item.get_type()
        if not type:
            type=item.set_type(T.FOLDER)
            import logging
            logging.warning('StoreItem %s has no type, so we set it as %s'%(item.path,type))
        if type==T.FOLDER:
            return StoreFolder(repo.path,remote_location=remote_location,remote_branch=remote_branch)
        else:
            assert type==T.FILE
            return StoreFile(repo.path,remote_location=remote_location,remote_branch=remote_branch)
    @classmethod
    def openStorefolder(cls,path,remote_location=None,remote_branch=None,force_pull=False,overwrite=False):
        remote_location=remote_location or default_remote_location
        if not is_git_dir(path):
            force_pull=True
        if not force_pull:
            item=StoreFolder(path,remote_location=remote_location,remote_branch=remote_branch)
        else:
            item=StoreFolder.pull(remote_location=remote_location,remote_branch=remote_branch,path=path,overwrite=overwrite)
        return item
    @classmethod
    def openStorefile(cls,path,remote_location=None,remote_branch=None,force_pull=False,overwrite=False):
        remote_location=remote_location or default_remote_location
        if not is_git_dir(path):
            force_pull=True
        if not force_pull:
            item=StoreFile(path,remote_location=remote_location,remote_branch=remote_branch)
        else:
            item=StoreFile.pull(remote_location=remote_location,remote_branch=remote_branch,path=path,overwrite=overwrite)
        return item
    def upload(self,remote_location=None,remote_branch=None,overwrite=True):
        # Todo:get remote branch list
        # deprecated !!!
        remote_loacation=remote_location or self.remote_location
        remote_branch=remote_branch or self.remote_branch
        assert remote_loacation and remote_branch
        assert remote_branch !='master'
        repo=self.repo
        repo.add_all()
        repo.commit()
        # br=repo.active_branch()
        if not remote_branch in repo.branch_list():
            repo.branch_create(remote_branch)
        repo.checkout_branch(remote_branch)
        repo.push(remote_loacation,remote_branch)
        # repo.checkout_branch(br)
        if not remote_branch in self._read_remote_branch_list():
            self._add_to_remote_branch_list(remote_branch)
    @classmethod
    def export(cls,path,remote_branch,remote_location=default_remote_location,name=None,cache_dir='.tmp',overwrite=False):
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        def _export_dir(obj,path,cache_dir):
            for p in obj.iter_contentpath():
                copy_fsitem(p, path)
            more = obj.morefile.copy()
            # obj.rmself()
            for nm, br in more.items():
                br_cache_dir=cache_dir+'/'+br
                cls.export(path, remote_location=remote_location, remote_branch=br, name=nm, cache_dir=br_cache_dir,overwrite=overwrite)
        this_dir=cache_dir+'/.this'
        obj=StoreItem.pull(remote_location=remote_location,remote_branch=remote_branch,path=this_dir)
        name = name or remote_branch.split(cls.delimiter)[-1]
        if isinstance(obj,StoreFolder):
            if not os.path.exists(path):
                os.makedirs(path)
            assert os.path.isdir(path)
            path=path+'/'+name
            if os.path.exists(path):
                if overwrite:
                    shutil.rmtree(path)
                else:
                    raise Exception("Can't export to %s because path already existed and overwrite is not True")
            os.mkdir(path)
            _export_dir(obj,path,cache_dir)
        else:
            assert isinstance(obj,StoreFile)
            if os.path.exists(path):
                assert os.path.isdir(path)
                if name:
                    path=path+'/'+name
                ps=obj.iter_contentpath()
                ps.sort()
                p=ps[0]
                # path=path+'/'+os.path.basename(p)
                copy_fsitem(p, path)

            else:
                for p in obj.iter_contentpath():
                    copy_fsitem(p, path)
            # obj.rmself()
        # remove_fsitem(cache_dir)
        # shutil.rmtree(cache_dir)
    @classmethod
    def uploadStoreitem(cls,path, remote_location, remote_branch, cache_dir,add_more=None):
        assert os.path.exists(path)
        if os.path.isdir(path):
            tmp = StoreFolder(cache_dir, remote_location=remote_location, remote_branch=remote_branch)
        else:
            tmp = StoreFile(cache_dir, remote_location=remote_location, remote_branch=remote_branch)
        tmp.clean()
        if os.path.isfile(path):
            tmp.eat(path)
        else:
            if add_more:
                for k,v in add_more.items():
                    tmp.addmore(k,v)
            for p in os.listdir(path):
                p = path + '/' + p
                tmp.eat(p)
        tmp.upload(remote_location=remote_location, remote_branch=remote_branch)
    @staticmethod
    def is_legal_path_to_upload(path):
        path=os.path.basename(path)
        legal_path_chars=StoreItem.legal_path_chars
        # print(legal_path_chars)
        if StoreItem.delimiter in path:
            import logging
            logging.warning('Illegal path "%s"!' % (path))
            return False
        for ch in path:
            if ch not in legal_path_chars:
                import logging
                logging.warning('Illegal path "%s"!'%(path))
                return False
        return True

    @classmethod
    def uploadStoreitemRecursive(cls,path, remote_location=None, remote_branch=None,
                                 cache_dir='.store.upload.cache',depth=-1,check_path=True):
        # todo: check branch name
        # assert remote_branch not in cls.special_branches
        assert depth>=0 or depth==-1
        assert os.path.exists(path)
        if check_path:
            assert cls.is_legal_path_to_upload(path)
        remote_location=remote_location or default_remote_location
        assert remote_branch
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        target_dir=cache_dir+'/target'
        store_dir=cache_dir+'/stores'
        os.makedirs(target_dir)
        copy_fsitem(path,target_dir)
        path=target_dir+'/'+os.path.basename(path)
        return cls._uploadStoreitemRecursive(path, remote_location, remote_branch, cache_dir=store_dir,depth=depth,check_path=check_path)
    @classmethod
    def _uploadStoreitemRecursive(cls,path, remote_location, remote_branch, cache_dir,depth=0,check_path=True):
        assert os.path.exists(path)
        if check_path:
            assert cls.is_legal_path_to_upload(path)
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        os.makedirs(cache_dir)
        print('path:',path)
        if depth==0:
            if os.path.isdir(path):

                tmp = StoreFolder(cache_dir, remote_location=remote_location, remote_branch=remote_branch)
                tmp.clean()
                for p in os.listdir(path):
                    p = path + '/' + p
                    tmp.eat(p)
            else:
                tmp = StoreFile(cache_dir, remote_location=remote_location, remote_branch=remote_branch)
                tmp.clean()
                tmp.eat(path)
        else:
            import uuid
            if os.path.isdir(path):
                self_cache_dir = cache_dir+'/self-cache-' + uuid.uuid4().hex
                more={}
                for name in os.listdir(path):
                    p=path+"/"+name
                    if check_path:
                        assert cls.is_legal_path_to_upload(p)
                    item_cache_dir=cache_dir+'/item-cache-'+name
                    os.mkdir(item_cache_dir)
                    item_branch=remote_branch+cls.delimiter+name
                    cls._uploadStoreitemRecursive(path=p,remote_location=remote_location,remote_branch=item_branch,cache_dir=item_cache_dir,depth=depth-1)
                    more[name]=item_branch
                os.mkdir(self_cache_dir)
                tmp = StoreFolder(self_cache_dir, remote_location=remote_location, remote_branch=remote_branch)
                tmp.morefile.update(more)
            else:
                tmp = StoreFile(cache_dir, remote_location=remote_location, remote_branch=remote_branch)
                tmp.clean()
                tmp.eat(path)
        tmp.upload(remote_location=remote_location, remote_branch=remote_branch)
        remove_fsitem(path)
    def is_empty(self):
        names=self.listdir()
        for name in names:
            if name not in self.data_list:
                return False
        return True
    def clean(self):
        names=self.listdir()
        for name in names:
            if name in self.data_list:
                continue
            self.remove(name)
            if name=='.more.store':
                self.openFiledict(name)

class StoreFolder(StoreItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.morefile = self.openFiledict('.more.store')
        self.set_type(T.FOLDER)
    def addmore(self,name,branch):
        self.morefile[name]=branch
    def eatStore(self,path,name=None,remote_location=None,remote_branch=None,upload=True,overwrite=False,cache_dir='.tmp',in_depth=0):
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        os.makedirs(cache_dir)
        assert os.path.exists(path)
        if not name:
            name=os.path.basename(os.path.abspath(path))
        remote_location = remote_location or self.remote_location
        assert remote_location
        if not remote_branch:
            assert self.remote_branch
            remote_branch=self.remote_branch+self.delimiter+name
        if upload:
            StoreItem.uploadStoreitem(path,remote_location=remote_location,remote_branch=remote_branch,cache_dir=cache_dir)
        self.morefile[name]=remote_branch

class StoreFile(StoreItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_type(T.FILE)





