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
        def hi(self):
            run_default()
        def deploy(self,service,*args,**kwargs):
            if service=='fsapp':
                from wk.applications import fsapp
                fsapp.setup_default(*args,**kwargs)
            else:
                print("Service %s is not valid."%(service))
    fire.Fire(Cli)

if __name__ == '__main__':
    main()