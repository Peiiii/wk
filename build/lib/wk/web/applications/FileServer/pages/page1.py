from wk.extra.node import *
from wk.extra.node import boostrap as bs

class SearchPageBase(Html):
    environment = dict(
        blue='#1D93EC'
    )
    def __init__(self):
        super().__init__()
        self.__call__([
            Head()([
                Meta(encoding='utf-8'),
                Meta(name="viewport",content="width=device-width, initial-scale=1, shrink-to-fit=no"),
                Title()(
                    Var(name="title",type='text')("高中学习资源下载")
                ),
                QLinks.bootstrap()
            ]),
            Body()([
                Var(name='body')([
                    Div(style="max-width:30em;",_class="m-auto p-3 pt-5  max-vh-30")(
                        Form(action='/search',_class="m-auto")([
                            '''
                            <div class="input-group mb-3">
  <input type="text" class="form-control" placeholder="{{placeholder  or '输入关键词，如“数学立体几何”'}}" name="search-keywords", value="{{input_fill or ''}}">
  <div class="input-group-append">
    <button class="btn btn-success" type="submit" id="basic-addon2">Search</button>
  </div>
</div>
                            '''
                        ])
                    ),
                    Div(_class="list-group p-2 m-auto text-center",style="max-width:40em;")(
                        Var(name="search_result")(
                            Div()("Nothing to show.")
                        )
                    )
                ]),
                QScripts.jquery(),
                QScripts.popper(),
                QScripts.bootstrap(),
            ])
        ])


class FileCard(Div):
    def __init__(self,file):
        super().__init__(_class='card')
        self.__call__([
            # A(href=file['url'])([
            #     bs.Badges.secondary(file['name'])
            # ]),
            # bs.Badges.success(file['size']),
            '''
      <li class="list-group-item" ><a href="{url}">{name}</a><span class="badge badge-secondary ml-2">{size}</span></li>
 '''.format(name=file['name'],size=file['size'],url=file['url'])
        ])