from flask import Flask, request, Blueprint, abort, send_file, redirect
from wpkit.web import resources, utils
from wpkit.pan import Pan, LocalFSHandle
from wpkit.web.base import MyBlueprint
from wpkit.web.resources import env, get_template_by_name
from wpkit.web.utils import parse_json_and_form,parse_cookies,parse_all
from wpkit.basic import Status,StatusError,StatusSuccess,PointDict
import logging, functools,json
import wpkit


class BluePan(MyBlueprint):
    add_to_sitemap = True
    def __init__(self, import_name=None, name='pan', datapath='./data/pan', url_prefix='/pan',
                  **kwargs):
        # github_path = "git@github.com:Peiiii/MyCloudSpace.git",
        super().__init__(name=name, import_name=import_name, url_prefix=url_prefix, **kwargs)
        self.datapath = wpkit.basic.DirPath(datapath)
        self.db = wpkit.piu.Piu(path=self.datapath.db)
        # print("db:",self.db.dic)
        self.panpath = self.datapath / 'pans'
        def user_panpath(email):
            return self.panpath/email
        # self.pan = None
        self.pans={}
        self.config_statics({
            "/files": self.panpath
        })
        self.usman = wpkit.web.utils.UserManager(dbpath=self.datapath.usman.db, home_url=self.url_prefix)
        usman = self.usman
        @self.usman.login_required
        @parse_all
        def getUrl(user_email,location, name):
            # print("getUrlK")
            res = 'http://%s:%s' % (
                self.app.host, self.app.port) + self.url_prefix + '/files/'+user_email+"/" + self.pans[user_email].local_path(
                location + '/' + name)
            print("res", res)
            return res

        rd_post_github_path=redirect(location=self.url_prefix+'/post_github_path')


        def check_pan(func):
            @parse_cookies
            @functools.wraps(func)
            def wrapper(user_email,*args, **kwargs):
                user=self.usman.get_user(user_email)

                if not user.get('initialized', None):
                    github_path=None
                    try:
                        github_path = user.get('github_path', None)
                        print("get github_path:",github_path)
                        if not github_path:
                            return rd_post_github_path
                        self.pans[user_email]= Pan.init(user_panpath(user_email), github_path=github_path)
                    except:
                        # raise
                        Pan.clear(user_panpath(user_email))
                        print("error occured when init pan, github_path:",github_path or None)
                        return redirect(location=self.url_prefix+'/post_github_path')
                    print('Initializing Pan at %s' % (self.panpath))
                    user.update(initialized=True)
                    self.usman.update_user(user_email,user)

                self.pans[user_email] = Pan(user_panpath(user_email))
                self.pans[user_email].add_cmd('getUrl', getUrl)
                return func(*args,**kwargs)
            return wrapper

        def check_github_path(func):
            @parse_cookies
            @functools.wraps(func)
            def wrapper(user_email,*args, **kwargs):
                user=usman.get_user(user_email)
                if not user.get('github_path',None):
                    return redirect(location=self.url_prefix+'/post_github_path')
                return func(*args, **kwargs)

            return wrapper

        self.route('/login', methods=['post'])(usman.login(redirect_to=redirect(location=self.url_prefix)))
        self.route('/login', methods=['get'])(usman.login_page)
        self.route('/signup', methods=['post'])(usman.signup)
        self.route('/signup', methods=['get'])(usman.signup_page)

        @self.route('/post_github_path',methods=['GET'])
        def do_get_post_github_path():
            # print("hello")
            # return abort(404)
            return get_template_by_name('form').render(
                action=self.url_prefix + '/post_github_path',
                method='POST',
                name='github_path',
                msg='Input github path'
            )
        @self.route('/post_github_path', methods=['POST'])
        @parse_all
        def do_post_github_path(user_email,github_path):
            user=self.usman.get_user(user_email)
            print("github_path:", github_path)
            if github_path:
                user.update(github_path=github_path)
                self.usman.update_user(user_email, user)
                return redirect(location=self.url_prefix)
            else:
                return "error"

        @self.route('/', methods=['get'])
        @usman.login_required
        @check_pan
        @check_github_path
        def do_pan_get():
            return resources.get_template_by_name('pan').render()

        @self.route('/', methods=['POST'])
        def do_pan_post():
            return

        @self.route('/cmd', methods=['post'])
        @usman.login_required
        @utils.parse_all
        def do_cmd(user_email,cmd):
            user=usman.get_user(user_email)
            print('cmd:', cmd)
            try:

                res = self.pans[user_email].execute(cmd)
                res=StatusSuccess(data=res)
            except:
                # raise
                res=StatusError()
            print('res:', res)
            return utils.jsonify(res)

        @self.route('/upload', methods=['POST', 'GET'])
        @self.usman.login_required
        @utils.parse_all
        def do_upload(user_email,info):
            file = request.files['file']
            if isinstance(info, str):
                info = json.loads(info)
            info = PointDict.from_dict(info)
            path = self.pans[user_email].local_path(info.location)
            path = self.pans[user_email].local_path(path + '/' + info.filename)
            path=user_panpath(user_email)+"/"+path
            file.save(path)
            print('path:', path)
            print('file:', file)
            return StatusSuccess(msg="Uploading succeeded.")
