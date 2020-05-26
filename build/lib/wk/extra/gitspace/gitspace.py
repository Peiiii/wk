'''
Deprecated
'''

from dulwich import porcelain as git
from dulwich.repo import Repo
from wk import FakeOS
from wk import T
import os, shutil, glob

default_remote_location= 'https://OpenGitspace:Gitspace@123456@gitee.com/OpenGitspace/meta'
defalut_user_location='https://OpenGitspace:Gitspace@123456@gitee.com/OpenGitspace/'

def get_default_remote_location(repo):
    return defalut_user_location+repo

class errors:
    class GitSpaceError(Exception):
        def __init__(self, *args):
            super().__init__(*args)


def is_git_dir(path):
    if os.path.exists(path) and os.path.isdir(path):
        dot_git_dir = path + '/.git'
        if os.path.exists(dot_git_dir) and os.path.isdir(dot_git_dir):
            return True
    return False


def is_empty_dir(path):
    assert os.path.exists(path) and os.path.isdir(path)
    if len(os.listdir(path)):
        return False
    else:
        return True

def to_string_iterable(iterable):
    lis=[s.decode() if isinstance(s,bytes) else s for s in iterable]
    return iterable.__class__(lis)
class GitRepo(Repo):
    def __init__(self,path):
        super().__init__(path)

    def clean(self):
        for name in os.listdir(self.path):
            if name=='.git':continue
            path=self.path+'/'+name
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    def active_branch(self):
        return git.active_branch(self).decode()
    def checkout_branch(self,branch='master'):
        git.update_head(self,branch)
        self.clean()
        co_ref = b'HEAD'
        repo_path=self.path
        from dulwich.repo import Repo
        from dulwich.index import build_index_from_tree
        repo = Repo(repo_path)
        indexfile = repo.index_path()
        obj_sto = repo.object_store
        tree_id = repo[co_ref].tree
        build_index_from_tree(repo_path, indexfile, obj_sto, tree_id)
        x=list(obj_sto.iter_tree_contents(tree_id))
        x=[obj_sto.iter_tree_contents(tree_id)]
    def branch_create(self,name):
        git.branch_create(self,name)
    def pull(self, remote_location, branch):
        git.pull(self, remote_location, branch)
    def branch_list(self):
        return list(to_string_iterable(git.branch_list(self)))
    def status(self,silent=False):
        repo = self
        msg = git.status(repo)
        if not silent:
            print(msg)
        return msg
    def add_all(self):
        repo = self
        status=git.status(self)
        paths = status.untracked + status.unstaged
        paths = [p.decode() if isinstance(p, bytes) else p for p in paths]
        paths = [self.path + '/' + p for p in paths]
        if not paths:
            import logging
            logging.warning('Working tree is clean. Nothing to add.')
            return
        paths.append(self.path)
        git.add(repo, paths)
    def commit(self,msg='commit somthing'):
        git.commit(self, msg)
    def push(self, remote_location, branch):
        git.push(self, remote_location, branch)



class GitRepoPlus:
    def __init__(self,path):
        self.grepo=GitRepo(path)
    def _init_branches(self):
        grepo=self.grepo
        # try:
            # grepo.pull()
    def _true_branch_name(self,name):
        import uuid
    def clean(self):
        for name in os.listdir(self.path):
            if name=='.git':continue
            path=self.path+'/'+name
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    def active_branch(self):
        return git.active_branch(self).decode()
    def checkout_branch(self,branch='master'):
        git.update_head(self,branch)
        self.clean()
        co_ref = b'HEAD'
        repo_path=self.path
        from dulwich.repo import Repo
        from dulwich.index import build_index_from_tree
        repo = Repo(repo_path)
        indexfile = repo.index_path()
        obj_sto = repo.object_store
        tree_id = repo[co_ref].tree
        build_index_from_tree(repo_path, indexfile, obj_sto, tree_id)
        x=list(obj_sto.iter_tree_contents(tree_id))
        x=[obj_sto.iter_tree_contents(tree_id)]
    def branch_create(self,name):
        git.branch_create(self,name)
    def pull(self, remote_location, branch):
        git.pull(self, remote_location, branch)
    def branch_list(self):
        return list(to_string_iterable(git.branch_list(self)))
    def status(self,silent=False):
        repo = self
        msg = git.status(repo)
        if not silent:
            print(msg)
        return msg
    def add_all(self):
        repo = self
        status=git.status(self)
        paths = status.untracked + status.unstaged
        paths = [p.decode() if isinstance(p, bytes) else p for p in paths]
        paths = [self.path + '/' + p for p in paths]
        if not paths:
            import logging
            logging.warning('Working tree is clean. Nothing to add.')
            return
        paths.append(self.path)
        git.add(repo, paths)
    def commit(self,msg='commit somthing'):
        git.commit(self, msg)
    def push(self, remote_location, branch):
        git.push(self, remote_location, branch)

def clone(src, path=None, overwrite=False,branch='master'):
    path = path or os.path.basename(src).rsplit('.git', maxsplit=1)[0]
    if os.path.exists(path) and overwrite:
        shutil.rmtree(path)
    assert not os.path.exists(path) or is_empty_dir(path)
    git.clone(src, path)
    repo=GitRepo(path)
    if not branch=='master':
        repo.pull(remote_location=src,branch=branch)
    return repo




class GitSpaceRepo:
    def __init__(self, path, remote_location=None):
        self.repo = Repo(path)
        self.path = os.path.abspath(path)
        self.remote_location = remote_location
        if not 'empty' in self.branch_list():
            self.branch_create('empty')
            br=self.active_branch()
            self.checkout_branch('empty')
            self.clean()
            self.stage()
            git.commit(self.repo,'empty')
            self.checkout_branch(br)
        self.git=git
    def all_remote_branches(self):
        raise NotImplementedError('')
    def log_new_branch(self,branch):
        raise NotImplementedError('')
    def clean(self):
        for name in os.listdir(self.path):
            if name=='.git':continue
            path=self.path+'/'+name
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    def active_branch(self):
        return git.active_branch(self.repo).decode()
    def checkout_branch(self,branch='master'):
        git.update_head(self.repo,branch)
        self.clean()
        co_ref = b'HEAD'
        repo_path=self.path
        from dulwich.repo import Repo
        from dulwich.index import build_index_from_tree
        repo = Repo(repo_path)
        indexfile = repo.index_path()
        obj_sto = repo.object_store
        tree_id = repo[co_ref].tree
        build_index_from_tree(repo_path, indexfile, obj_sto, tree_id)
        x=list(obj_sto.iter_tree_contents(tree_id))
        # print('branch contents:',x)
        x=[obj_sto.iter_tree_contents(tree_id)]
        # self.clean()
    def branch_create_empty(self, name):
        br=self.active_branch()
        self.checkout_branch('empty')
        self.branch_create(name)
        self.checkout_branch(br)
    def branch_create(self,name):
        repo=self.repo
        git.branch_create(repo,name)
    def pull(self, remote_location=None, branch='master'):
        remote_location = remote_location or self.remote_location
        if not remote_location:
            raise Exception('Remote location is not given.')
        repo = self.repo
        git.pull(repo, remote_location, branch)
    def branch_list(self):
        return list(to_string_iterable(git.branch_list(self.repo)))
    def status(self,silent=False):
        repo = self.repo
        msg = git.status(repo)
        if not silent:
            print(msg)
        return msg
    def stage(self):
        repo = self.repo
        status=git.status(self.repo)
        paths = status.untracked + status.unstaged
        paths = [p.decode() if isinstance(p, bytes) else p for p in paths]
        paths = [self.path + '/' + p for p in paths]
        if not paths:
            import logging
            logging.warning('Working tree is clean. Nothing to add.')
            return
        paths.append(self.path)
        git.add(repo, paths)
    def push(self, remote_location=None, branch=None):
        branch=branch or self.active_branch() or 'master'
        # print("branch_to_push:",branch)
        remote_location = remote_location or self.remote_location
        if not remote_location:
            raise Exception('Remote location is not given.')
        repo = self.repo
        self.stage()
        git.commit(repo, 'bare gitspace commit')
        git.push(repo, remote_location, branch)

    @classmethod
    def init(cls, path):
        git.init(path)
        return cls(path)

    @classmethod
    def clone(cls, src, path=None, overwrite=False,branch='master'):
        path = path or os.path.basename(src).rsplit('.git', maxsplit=1)[0]
        if os.path.exists(path) and overwrite:
            shutil.rmtree(path)
        assert not os.path.exists(path) or is_empty_dir(path)
        git.clone(src, path)
        repo=cls(path, src)
        repo.pull(branch=branch)
        return repo

    @classmethod
    def openSpace(cls, path, remote_path=None,branch='master'):
        if not os.path.exists(path) or is_empty_dir(path):
            assert remote_path
            cls.clone(remote_path, path,branch=branch)
            repo = cls(path, remote_path)
            return repo
        elif is_git_dir(path):
            return cls(path, remote_path)
        else:
            raise Exception('A non-empty directory %s already exists and it is not a git repo.' % (path))


class GitSpace(GitSpaceRepo, FakeOS):
    def __init__(self, path, remote_location=None):
        GitSpaceRepo.__init__(self, path, remote_location)
        FakeOS.__init__(self, path)


def open_default(path,branch='master'):
    # url = 'https://OpenGitspace:Gitspace@123456@github.com/OpenGitspace/meta'
    url =default_remote_location
    return GitSpace.openSpace(path, remote_path=url,branch=branch)

class SimpleStore:
    def __init__(self,remote_location=None,cache_dir=None):
        self.remote_location=remote_location or default_remote_location
        self.cache_dir=cache_dir or '.store_cache'
        self._setup()
    def _get_config(self):
        cfg = self.space.openFiledict('.store.cfg')
        return cfg
    def _setup(self):
        space=GitSpace.openSpace(path=self.cache_dir,remote_path=self.remote_location,branch='master')
        cfg=space.openFiledict('.store.cfg')
        if not cfg.get('store_keys'):
            cfg.store_keys=['master','empty']
            space.push()
        self.space=space
    def _add_key_to_config(self,key):
        space=self.space
        cfg = self._get_config()
        if key in cfg.store_keys:return
        cfg.store_keys.append(key)
        cfg._save()
        self.space.push()
    def keys(self):
        cfg=self._get_config()
        # print(cfg)
        # input()
        return cfg.store_keys
    def status(self):
        from wk import PointDict
        info=PointDict(
            current_branch=self.space.active_branch(),
            branches=self.space.branch_list(),
            status=self.space.status(silent=True)
        )
        if self.space.active_branch()=='master':
            info.store_keys=self.keys()
        # info.print()
        print(info)
        return info
    def store(self,key,path,overwrite=False):
        assert os.path.exists(path)
        br=self.space.active_branch()
        space=self.space
        if key in self.keys():
            if not overwrite:
                raise Exception('Key "%s" already exists.'%(key))
            # self.space.pull(branch=key)
            # self.space.clean()
        if key in space.branch_list():
            self._add_key_to_config(key)
            space.checkout_branch(key)
            space.clean()
        else:
            self.space.branch_create_empty(name=key)
            self._add_key_to_config(key)
            self.space.checkout_branch(key)
        # self.status()
        self._copy_to_cache_dir(path)
        # self.status()

        self.space.push()
        # self.status()
        # print('br:',br)
        self.space.checkout_branch(br)
        # self.status()
        # input()
        # self.status()

    def fetch(self,key,dst,default=T.NOT_GIVEN):
        space=self.space
        br=space.active_branch()
        # self.status()
        if key in space.branch_list():
            # use local branch
            space.checkout_branch(key)
        else:
            # pull from remote
            if not key in self.keys():
                if T.NOT_GIVEN(default):
                    raise KeyError('Key %s does not exist.' % (key))
                else:
                    return default
            space.branch_create_empty(key)
            space.checkout_branch(key)
            space.pull(branch=key)
        # self.status()
        self.from_cache_dir_to_path(dst)
        # self.status()
        # input()
        space.checkout_branch(br)
        # self.status()
        # input()
    def from_cache_dir_to_path(self,dst):
        fs=os.listdir(self.cache_dir)
        fs.remove('.git')
        for name in fs:
            path=self.cache_dir+'/'+name
            self._copy(path,dst)
    def _copy_to_cache_dir(self,paths):
        self._copy(paths,self.cache_dir)
    def _copy(self,paths,dst,overwrite=False):
        from wk import copy_dir,copy_file
        if isinstance(paths,str):
            paths=[paths]
        for path in paths:
            if os.path.isdir(path):
                copy_dir(path,dst)
            else:
                copy_file(path,dst,overwrite=overwrite)

def main():
    test()

    pass


def test():
    url=''
    # r=GitSpace.openSpace('MyCloudSpace',url)
    # r=GitSpace.openSpace('piudb',url)
    r = GitSpace.clone(url, overwrite=True)
    # f=r.open('testgit.txt','a')
    # f.write('hi\n')
    # f.close()
    r.pull()
    # r.push()


def demo():
    url="git://github.com/Peiiii/piudb"
    # git.clone(url)
    import os
    rpath = os.path.basename(url)
    open(rpath + '/testgit.txt', 'a').write('hi\n')
    r = Repo(rpath)
    git.add(r, rpath + '/testgit.txt')
    git.commit(r, b'sample commit')
    git.push(r, url, 'master')


if __name__ == '__main__':
    # demo()
    main()
