
import os,shutil,glob
import inspect
import time

def is_empty_dir(path):
    assert os.path.exists(path)
    if not os.path.isdir(path):
        return False
    if len(os.listdir(path)):
        return False
    else:
        return True
def _copy_dir(src,dst):
    assert os.path.exists(src)
    assert os.path.exists(dst)
    for name in os.listdir(src):
        path=os.path.join(src,name)
        new_path=os.path.join(dst,name)
        if os.path.isdir(path):
            os.mkdir(new_path)
            _copy_dir(path,new_path)
        elif os.path.isfile(path):
            shutil.copy(path,new_path)
def copy_file(src,dst,overwrite=False):
    '''
    if dst is dir: copy into dir
    if dst is file and overwrite: overwrite
    if dst doesn't exist : parent should exist, use shutil.copy
    '''
    assert os.path.isfile(src)
    if os.path.exists(dst):
        if os.path.isdir(dst):
            shutil.copy(src,dst+'/'+os.path.basename(src))
        else:
            if overwrite:
                shutil.copy(src,dst)
            else:
                raise FileExistsError('%s is an existed file.'%(dst))
    else:
        parent=os.path.dirname(dst)
        if parent=='':
            parent='./'
        assert os.path.exists(parent)
        shutil.copy(src,dst)


def copy_dir(src,dst):
    '''
    if dst exists, copy src into dst,
    else mkdir dst and copy src's contents into dst
    '''
    assert os.path.exists(src)
    src=os.path.abspath(src)
    name=os.path.basename(src)
    if os.path.exists(dst):
        assert os.path.isdir(dst)
        newdir=os.path.join(dst,name)
        os.mkdir(newdir)
        _copy_dir(src,newdir)
    else:
        parent_dir=os.path.dirname(dst)
        # assert os.path.exists(parent_dir)
        os.mkdir(dst)
        _copy_dir(src,dst)

def copy_fsitem(src,dst,overwrite=False):
    assert os.path.exists(src)
    if os.path.isdir(src):
        copy_dir(src,dst)
    else:
        copy_file(src,dst,overwrite=overwrite)
def remove_fsitem(path):
    if os.path.isdir(path):
        return shutil.rmtree(path)
    else:
        time=0
        while True:
            try:
                return os.remove(path)
            except:
                time+=1
                if time==3:
                    raise
def merge_dirs(src_dirs,dst_dir):
    if  os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
        a=0
    os.makedirs(dst_dir)
    for dir in src_dirs:
        fs=glob.glob(dir+'/*')
        copy_files_to(fs,dst_dir)

def batch_rename_files(src_dir,handler,out_dir=None,glob_str='*',sort_key_func=None):
    src_dir=os.path.abspath(src_dir)
    fs=glob.glob(src_dir+'/'+glob_str)
    if sort_key_func:
        fs.sort(key=sort_key_func)
    if not out_dir:
        out_dir=os.path.dirname(src_dir)+'/'+os.path.basename(src_dir)+'_rename_output'
        remake(out_dir)
    args=inspect.getfullargspec(handler)[0]
    for i,f in enumerate(fs):
        name=os.path.basename(f)
        if len(args)==1:
            name2=handler(name)
        else:
            name2=handler(name,i)
        if name2:
            f2=out_dir+'/'+name2
            shutil.copy(f,f2)
            print(i,f,f2)
    print('finished.')



def copy_files_to(files,dst,overwrite=False):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for i,f in enumerate(files):
        fn=os.path.basename(f)
        f2=dst+'/'+fn
        if os.path.exists(f2):
            if os.path.samefile(f, f2):
                print("ignoring same file:", f, f2)
                continue
            if not overwrite:
                raise Exception("file %s already exists."%(f2))
            else:
                print("overwriting %s to %s ..."%(f,f2))
                os.remove(f2)
        shutil.copy(f,f2)
def tranverse_files(dir,func):
    fs=glob.glob(dir+'/*')
    for f in fs:
        if os.path.isfile(f):
            func(f)
        elif os.path.isdir(f):
            tranverse_files(f,func)
def tranverse_dirs(dir,func):
    fs=glob.glob(dir+'/*')
    for f in fs:
        if os.path.isfile(f):
            pass
        elif os.path.isdir(f):
            func(f)
            tranverse_dirs(f,func)
def remove(path,not_exist_ok=True):
    if os.path.exists(path):
        if os.path.isdir(path) :
            shutil.rmtree(path)
        else:
            os.remove(path)
    elif not not_exist_ok:
        raise Exception('File or dir %s does not exist'%(path))
def remake(dir,speep_time=0):
    if os.path.exists(dir):
        shutil.rmtree(dir)
        time.sleep(speep_time)
    os.makedirs(dir)
def compare_dirs(src1,src2,dst='./compare_results'):
    files1=glob.glob(src1+'/*.*')
    files2=glob.glob(src2+'/*.*')
    same1=dst+'/1_same'
    same2=dst+'/2_same'
    diff1=dst+'/1_diff'
    diff2=dst+'/2_diff'
    remake(same1)
    remake(same2)
    remake(diff1)
    remake(diff2)
    names1=[os.path.basename(f) for f in files1]
    names2=[os.path.basename(f) for f in files2]
    ds1=set(names1)-set(names2)
    ds2=set(names2)-set(names1)
    ss=set(names1).intersection(set(names2))
    dl1=[src1+'/'+f for f in ds1]
    dl2=[src2+'/'+f for f in ds2]
    sl1=[src1+'/'+f for f in ss]
    sl2=[src2+'/'+f for f in ss]
    copy_files_to(dl1,diff1)
    copy_files_to(dl2,diff2)
    copy_files_to(sl1,same1)
    copy_files_to(sl2,same2)
