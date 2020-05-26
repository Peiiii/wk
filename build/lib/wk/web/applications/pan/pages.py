# import wpkit
# from wpkit.web import bps
# app=wpkit.web.get_default_app(__name__)
# app.register_blueprint(bps.bp_pan.bp_pan(app,url_prefix='/pan'))


from wpkit.node import *
from wpkit.node import components
from wpkit.node.Q import *
from wpkit.node.components import *

# body=Body(style="background-color:#ffffff;")(
#     Div(_class="row",style="width:300px;height:300px;background-color:#fafafa"),
#     Div(_class="row",style="width:300px;height:300px;background-color:yellow;")
# )
post_script = Text("var data={cmd:{op:1,params:[2]}};console.log(data);res=postJson('/pan/data',data);console.log(res)")
body = Div(style=StyleAttr(height="100%", width="100%"))(
    QBox().css(height='{{h1}}%'),
    QBox()(
        QBox(style=StyleAttr(float="left", width="calc({{w}}%)", background_color="#eeeeee"))(
            QButton(onclick=post_script)("Click Me")
        ),
        QBox(id=3)(
            QCell()("Hello")
        ).css(float="right", width="calc({{100-w}}%)")
    ).css(height='{{100-h1}}%')
)
from wpkit.web import resources
body = Div(_class='container')(
    link.csslink(href='/pkg-resource/css/jquery-resizable.css'),
    Script(src='/pkg-resource/js/jquery-resizable.js'),
    Script()(
        resources.get_js_string_by_name('my.js')
    ),
    Script(src="/pkg-resource/pkgs/vue-grid-layout/vue-grid-layout.umd.min.js"),
    Script(src='/pkg-resource/pkgs/vue-draggable-resizable/vue-draggable-resizable.js')(),
    link.csslink(href='/pkg-resource/pkgs/vue-draggable-resizable/vue-draggable-resizable.css'),
    Script()(
        '''
        function getDir(location,dirname){
                var cmd={cmd:{op:"getDir",params:{location:location,dirname:dirname}}};
        console.log(cmd);var res=postJson('/pan/cmd',cmd).responseJSON;console.log(res);
        return res;
            }
        function getFile(location,filename){
            var cmd={cmd:{op:"getFile",params:{location:location,filename:filename}}};
        console.log(cmd);var res=postJson('/pan/cmd',cmd).responseJSON;console.log(res);
        return res;
        }
        $(document).ready(()=>{
            
        })
        '''
    ),
    Div()(
        resources.get_template_string_by_name('tmp')
    ),
    QRow()(
        resources.get_template_string_by_name('test')
    )
)
panpage = components.Sitebase().render(body=body)
# testobj=body
# panpage["body"].css(padding=0, margin=0,background="black",color="white")
panpage["body"].css(padding=0, margin=0)
testobj = body
panpage = panpage.compile().render(h1=8, w=8)
