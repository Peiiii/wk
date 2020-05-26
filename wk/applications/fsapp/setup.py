import shutil,os,glob
def setup_default(out_dir='./mysite',add_as_service=True):
    dir=os.path.dirname(__file__)+'/pjfiles'
    if not os.path.exists(out_dir):os.makedirs(out_dir)
    for i,f in enumerate(glob.glob(dir+'/*')):
        if os.path.isdir(f):continue
        f2=out_dir+'/'+os.path.basename(f)
        shutil.copy(f,f2)
    if not add_as_service:return  True
    from wpkit.linux.tools import add_py_to_service
    add_py_to_service(service_name="mysite",project_dir=out_dir,script_file_path=out_dir+'/main.py')

