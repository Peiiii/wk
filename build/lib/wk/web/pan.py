import git as g
import os
from wk.basic import PowerDirPath,PointDict,join_path,standard_path

class LocalFSHandle:
    def __init__(self,path):
        os.makedirs(path) if not os.path.exists(path) else None
        assert os.path.exists(path)
        # print("path:",path)
        path=os.path.abspath(path)
        self.lpath=path
        self.curser=PowerDirPath(path)
        self.cmd_dict={
            'newFile':self.newFile,
            'newDir':self.newDir,
            'getFile':self.getFile,
            'getDir':self.getDir,
            'saveFile':self.saveFile,
            'delete':self.delete,
        }
    def add_cmd(self,cmd,func):
        self.cmd_dict[cmd]=func
    @classmethod
    def init(cls,path):
        os.makedirs(path) if not os.path.exists(path) else None
        return cls(path=path)
    @classmethod
    def clear(cls,path):
        PowerDirPath(path).rmself().todir()
    def true_path(self,path):
        return join_path(self.lpath,self.local_path(path))
    def local_path(self,path):
        # print(path)
        try:
            path=standard_path(path,check=True)
        except:
            return None
        return path
    def saveFile(self,filename,location,content):
        location = self.true_path(location)
        f = PowerDirPath(location)/filename
        return f(content)
    def newFile(self,filename,location,content=None):
        location = self.true_path(location)
        loc=PowerDirPath(location)
        return loc.file(filename)(content) if content is not None else loc.file(filename)
    def newDir(self,dirname,location):
        location = self.true_path(location)
        loc = PowerDirPath(location)
        return loc(dirname)
    def delete(self,name,location):
        location = self.true_path(location)
        loc = PowerDirPath(location)
        return (loc/name).rmself()
    def getFile(self,filename,location):
        location = self.true_path(location)
        loc = PowerDirPath(location)
        return (loc/filename)()
    def getDir(self,dirname,location):
        location=self.true_path(location)
        loc = PowerDirPath(location)
        li=(loc/dirname)()
        return [{'name':i,'type':PowerDirPath(loc/dirname/i).type()} for i in li]
    def execute(self,cmd):
        cmd=PointDict.from_dict(cmd)
        op,params=cmd.op,cmd.params
        # if 'location' in params.keys():
        #     params['location']=self.true_path(params['location'])
        if op in self.cmd_dict.keys():
            # print(self.cmd_dict[op](**params))
            # print("params:",params)
            res= self.cmd_dict[op](**params)
            # print("res:",res)
            return res

class Pan(LocalFSHandle):
    def __init__(self,path):
        super().__init__(path)
        self.repo = g.Repo(path)
        git = self.repo.git
        self.git = git
        self.add_cmd('pull',self.pull)
        self.add_cmd('push',self.push)
        self.add_cmd('goback',self.goback)
    @classmethod
    def init(cls, path, github_path):
        os.makedirs(path) if not os.path.exists(path) else None
        repo = g.Repo.init(path)
        git = repo.git
        try:
            git.remote('add', 'origin', github_path)
        except:
            pass
        git.pull('origin', 'master')
        git.config("--global","push.default","simple")
        # git.push("--set-upstream","origin","master")
        # git.branch('--set-upstream-to=origin/master', 'master')
        return cls(path=path)
    def pull(self):
        git=self.git
        git.fetch('--all')
        git.reset('--hard','origin/master')
    def push(self):
        git=self.git
        git.add('.')
        git.commit('-m','test')
        # git.push('origin','master')
        git.push("--set-upstream", "origin", "master")
        # git.push("--set-upstream", "origin", "master",">","log.txt")
    def goback(self,n=1):
        self.git.reset('--hard','HEAD'+'^'*n)
    def destroy(self):
        try:
            PowerDirPath(self.lpath).rmself()
        except:
            pass





demo_code=\
'''
pan = Pan.init('./myspace', github_path='http://github.com/Peiiii/MyCloudSpace')
pan=Pan('./myspace')
repo.pull()
repo.goback(4)
a=pan.getDir('./',location='./myspace')
'''
