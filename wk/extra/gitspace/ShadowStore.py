from .StoreItem import *
from .utils import generate_hash

_BRANCH_LIST='remote_branch_list'
USER_HOME=os.path.expanduser('~')
STORE_HOME=USER_HOME+'/.store'
BRANCH_LIST_DIR=STORE_HOME+'/BranchLists'
SHADOW_STORE_HOME=STORE_HOME+'/ShadowStores'
def get_default_shadowstore_path():
    return SHADOW_STORE_HOME+'/main'

class ShadowStore:
    def __init__(self,path=None,remote_location=None,sync_keys=False):
        remote_location=remote_location or default_remote_location
        path=path or get_default_shadowstore_path()
        self.path=path
        self.remote_location=remote_location
        print("Creating empty branch...")
        # self.folder=StoreFolder.openStorefolder(self.path,remote_location=self.remote_location,remote_branch='empty')
        self.rbl=get_default_remote_branch_list(remote_location=self.remote_location)
        print("Create empty branch successful")
        if sync_keys:
            self.sync_keys()
        print("Init shadow store finish.")
    def sync_keys(self):
        # self.folder.rbl.sync_list()
        self.rbl.sync_list()
        return self.keys()
    def keys(self):
        # return self.folder.rbl.read_list()
        return self.rbl.read_list()
    def is_legal_key(self,key):
        legal_chars=StoreItem.legal_path_chars+['/']
        if StoreItem.delimiter in key:
            return False
        for ch in key:
            if not ch in legal_chars:
                return False
        return True
    def key_to_branch(self,key):
        assert self.is_legal_key(key)
        remote_branch = key.replace('/', StoreItem.delimiter)
        return remote_branch
    def get(self,key,path=None,overwrite=False):
        path=path or './'
        if os.path.exists(path):
            if os.path.isfile(path):
                if overwrite:
                    remove_fsitem(path)
                else:
                    raise FileExistsError('File %s already exists.'%(path))
            if os.path.isdir(path):
                tp=path+'/'+os.path.basename(key)
                if os.path.exists(tp):
                    if (os.path.isdir(tp) and not is_empty_dir(tp)) or os.path.isfile(tp):
                        if overwrite:
                            remove_fsitem(tp)
                        else:
                            raise FileExistsError('File %s already exists.' % (tp))
        remote_branch=self.key_to_branch(key)
        # print(remote_branch,self.keys())
        assert remote_branch in self.keys()
        print("exporting... %s,%s"%(path,remote_branch))
        StoreItem.export(path,remote_location=self.remote_location,remote_branch=remote_branch,cache_dir=self.path)
        return True
    def set(self,key,path,recursive=False,add_more=None):
        remote_branch=self.key_to_branch(key)
        if not recursive:
            StoreItem.uploadStoreitem(path,remote_location=self.remote_location,remote_branch=remote_branch,cache_dir=self.path,add_more=add_more)
        else:
            StoreItem.uploadStoreitemRecursive(path,remote_location=self.remote_location,remote_branch=remote_branch,cache_dir=self.cache_dir)

