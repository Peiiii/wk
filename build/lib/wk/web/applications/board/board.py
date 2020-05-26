from flask import request
from wpkit.web import resources,utils
from wpkit import piu,basic
from wpkit.web.base import MyBlueprint

class BlueBoard(MyBlueprint):
    def __init__(self, import_name=None, name='board', datapath='./data/board', url_prefix='/pan', **kwargs):
        super().__init__(name=name, import_name=import_name, url_prefix=url_prefix, **kwargs)
        self.datapath = basic.DirPath(datapath)
        self.db = piu.Piu(path=self.datapath.db)
        @self.route('/')
        def do_board():
            data = self.db.get('board_data', '')
            return  resources.get_template_by_name('board').render(content=data)
        @self.route('/post', methods=['POST'])
        def do_board_post():
            data = request.get_json()
            self.db.add('board_data', data['content'])
            return 'success'


