import os,shutil,glob,json,uuid,time
from ..ioutils import json_dump,json_load
class FileDB:
    def __init__(self,save_dir,remake_dir=False,check_keys=False):
        '''
        info.json:
            {
                "files":{
                    "file_key1":{
                        "save_filename":"nwdqw",
                        "original_filename":"test.csv"
                    },
                    "file_key2":{
                        ...
                    }
                }
            }
        '''
        self.save_dir=save_dir
        self.files_dir=save_dir+'/files'
        self.info_file=save_dir+'/info.json'
        if remake_dir:
            if os.path.exists(save_dir):
                shutil.rmtree(save_dir)
                time.sleep(0.01)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)
        if not os.path.exists(self.info_file):
            json_dump({},self.info_file)
        if check_keys:
            self._check_keys()

    def eat_file(self,file,key=None,overwrite=False):
        assert os.path.exists(file)
        key=key or self._gen_file_key()
        dst = self.files_dir + '/' + key
        if key in self._get_file_dict().keys():
            if not overwrite:
                raise Exception("Key %s already exists but overwrite option is False."%(key))
            else:
                os.remove(dst)
        shutil.copy(file,dst)
        info={
            "original_filename":os.path.basename(file),
            "save_filename":key
        }
        self._add_to_file_dict(key,info)

    def _gen_file_key(self):
        key=uuid.uuid4().hex
        return key
    def _get_file_dict(self):
        info = json_load(self.info_file)
        return info['files']
    def _add_to_file_dict(self,key,info):
        info=json_load(self.info_file)
        info['files'][key]=info
        json_dump(info,self.info_file)
    def _check_keys(self,raise_error=True):
        ''' assume that info.json files_dir exists. '''
        files=self._get_file_dict()
        files_in_json=[info['save_filename'] for info in files.values()]
        files_exists=os.listdir(self.files_dir)
        if not set(files_in_json)==set(files_exists):
            if raise_error:
                raise Exception("Files exist are not the same as the list in info file.")
            else:
                return False
        return True
