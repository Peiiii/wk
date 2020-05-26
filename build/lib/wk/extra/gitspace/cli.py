from wk.extra.gitspace import Store

import fire
class Cli:

    @classmethod
    def download(cls,key,path=None,overwrite=False):
        from wk.extra.gitspace import Store
        store = Store()
        store.get(key,path=path,overwrite=overwrite)
    @classmethod
    def upload(cls,key,path,recursive=False):
        from wk.extra.gitspace import Store
        store = Store()
        store.set(key,path,recursive)
if __name__ == '__main__':
    fire.Fire(Cli)