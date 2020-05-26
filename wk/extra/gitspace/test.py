from wpkit.gitspace.StoreFolder import StoreFolder,StoreFile
from wpkit.basic import get_time_formated
from wpkit.utils import SimpleListFile


def main():

    # test3()
    # test5()
    # test6()
    # test7()
    # test8()
    test9()
    # test10()

    pass
def test10():
    folder = StoreFolder.openStorefolder(path='folder-deploy', remote_branch='folder-deploy',
                                         force_pull=False, overwrite=True)
def test9():
    StoreFolder.export('export',remote_branch='folder',overwrite=True)
def test8():
    folder = StoreFolder.openStorefolder(path='folder', remote_branch='folder',
                                         force_pull=False, overwrite=True)
    folder.eatStore(path='deploy')
    folder.upload()

def test7():
    file=StoreFile.openStorefile(path='msyh', remote_branch='msyh.ttf',
                                         force_pull=False, overwrite=True)
    file.upload()

def test6():
    folder = StoreFolder.openStorefolder(path='remote_branch_list', remote_branch='remote_branch_list',
                                         force_pull=True, overwrite=True)
    repo=folder.repo
    # repo.checkout_branch('remote_branch_list')
    # folder.rmfile('test.json')

    folder.upload()
def test5():
    folder=StoreFolder.openStorefolder(path='folder',remote_branch='folder',
                                       force_pull=False,overwrite=True)
    folder.status()
    add_content(folder)
    folder.upload()
    folder._pull_remote_branch_list()
    repo=folder.repo
    # repo.pull(folder.remote_location,'remote_branch_list')
    x=folder._read_remote_branch_list()
    print(x)
    folder.status()






def add_content(folder):
    dic = folder.openFiledict('test.json')
    if not dic.get('times',None):
        dic.times=[]
    time = get_time_formated()
    dic.times.append(time)
    dic._save()
def add_file(folder):
    from uuid import uuid4
    # folder=StoreFile()
    folder.newfile(uuid4().hex+'.txt')
def test1():
    folder = StoreFolder('./folder',remote_branch='folder')
    repo = folder.repo
    print(dict(repo.refs))
    add_content(folder)
    add_file(folder)
    folder.upload()

def test2():
    StoreFolder.export('export',remote_branch='folder',overwrite=True)
    import os,shutil
def test3():
    folder = StoreFile('./file', remote_branch='file')
    repo = folder.repo
    print(dict(repo.refs))
    add_content(folder)
    folder.upload()
def test4():
    StoreFile.export('export', remote_branch='file', overwrite=True)


if __name__ == '__main__':
    main()
# test1()
# test2()

# test3()
# test4()


# ref='refs/remotes/origin/bgs-1'
# repo.checkout_branch(ref)
#
# a=folder.openFieldict('test.json')
# a.time=get_time_formated()
# folder.upload()
