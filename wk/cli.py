import argparse
import os
os.environ['ANSI_COLORS_DISABLED']="1"
import wk

def run_default():
    words = 'Hello, I am wpkit2 ,use me !'
    length = 50
    print('*' * length)
    print(words.center(length, '*'))
    print('*' * length)
def main_bold():
    parser = argparse.ArgumentParser()
    parser.add_argument('-command', type=str)
    args = parser.parse_args()
    if args.command is None:
        run_default()
    elif args.command=='deploy':
        pass
def main():
    import fire
    class Cli:
        @staticmethod
        def hi():
            run_default()

        @staticmethod
        def downtee( key, path=None, overwrite=False):
            from wk.extra.gitspace import Store
            store = Store()
            store.get(key, path=path, overwrite=overwrite)

        @staticmethod
        def uptee( key, path, recursive=False):
            from wk.extra.gitspace import Store
            store = Store()
            store.set(key, path, recursive)

        @staticmethod
        def deploy(service,*args,**kwargs):
            if service=='fsapp':
                from wk.applications import fsapp
                fsapp.setup_default(*args,**kwargs)
            else:
                print("Service %s is not valid."%(service))
    fire.Fire(Cli)
    # Cli.uptee('wpkit2','../dist/wpkit2-0.0.1.3-py3-none-any.whl')

if __name__ == '__main__':
    main()
