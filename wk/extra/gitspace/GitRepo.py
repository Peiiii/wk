from dulwich import porcelain as git
from dulwich.repo import Repo
from wpkit.fsutil.dir_dict import FakeOS
from wpkit.basic import T
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
        import logging
        logging.warning("Pulling from %s:%s" % (remote_location, branch))
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
        import logging
        logging.warning("Pushing to %s:%s"%(remote_location,branch))
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