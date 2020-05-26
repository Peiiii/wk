'''
dependencies:
linux: wget lsof
'''

import os,subprocess,time,shutil
test_link= 'https://dn3.freedownloadmanager.org/5/5.1-latest/fdm5_x64_setup.exe'
test_git_link='https://github.com/myhub/tr'
def shell_cmd(cmd):
    p=subprocess.Popen(cmd,shell=True)
    p.wait()
    return p.returncode
def chmod(mode,dst):
    return shell_cmd('chmod %s %s'%(mode,dst))
def clean_port(port=8000): # prerequisite: lsof
    os.system('kill -9 `lsof -i:%s -t`'%(port))
def wget_download(url,out_dir=None,log_file=None): # prerequisite: wget
    dir_str,log_str='',''
    if out_dir is not  None:
        dir_str='-P '+out_dir
    if log_file is not  None:
        log_str = ' > ' + log_file + ' 2>&1 &'
    cmd = 'wget %s %s %s'%(dir_str,url,log_str)
    p=subprocess.Popen(cmd,shell=True)
    return p
def git_clone(url,out_dir=''):
    cmd='git clone %s %s'%(url,out_dir)
    p=subprocess.Popen(cmd,shell=True,)
    p.wait()
    return p.returncode
def zip_dir(src,dst=None):
    dst = dst or src+'.zip'
    cmd='zip -rl %s %s'%(dst,src)
    r=shell_cmd(cmd)
    return r
def add_bash_script_as_service(bpath):
    name=os.path.basename(bpath)
    cmd='rm -f /etc/init.d/%s;cp %s /etc/init.d/;cd /etc/init.d/;chmod +x %s;\
     chkconfig --add %s;chkconfig %s on'%(name,bpath,name,name,name)
    return  shell_cmd(cmd)
def add_py_to_service(service_name,project_dir,script_file_path):
    project_dir=os.path.abspath(project_dir)
    script_file_path=os.path.abspath(script_file_path)
    from ..gen_scripts import gen_scripts
    gen_scripts.gen_service(dst_file=project_dir+'/'+service_name,service_name=service_name,
                            project_dir=project_dir,script_file_name=script_file_path)
    add_bash_script_as_service(project_dir+'/'+service_name)

if __name__ == '__main__':
    # git_clone(git_link)
    # d=os.path.basename(git_link)
    # zip_dir(d,'tr.zip')
    # add_bash_file_service('/root/projects/mysite/mysite')
    add_py_to_service(service_name='mysite',project_dir='/root/projects/mysite',script_file_path='main.py')
    pass