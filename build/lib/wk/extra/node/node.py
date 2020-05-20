

class Node:
    tag='Node'
    self_closing=False
    _attrs={}
    def __init__(self,**kwargs):
        def preprocess(kwargs):
            cls_attr = '_class'
            if cls_attr in kwargs.keys():
                kwargs['class'] = kwargs.pop(cls_attr)
            return kwargs
        self.attrs={}
        self.attrs.update(**self._attrs)
        self.attrs=preprocess(self.attrs)
        self.children=[]
        kwargs=preprocess(kwargs)
        children_name='children'
        if children_name in kwargs.keys():
            self.children=kwargs.pop(children_name)
        self.attrs.update(**kwargs)
    def to_string(self,indent=0,indent_step=2):
        tag_and_attrs_string=' '.join([self.tag]+['%s="%s"'%(name,value) for name,value in self.attrs.items()])
        if self.self_closing:
            return '{indent}<{tag_and_attrs}>\n'.format(indent=' '*indent,tag_and_attrs=tag_and_attrs_string)
        else:
            children_string=''.join([child.to_string(indent=indent+indent_step,indent_step=indent_step) if isinstance(child,Node) else ' '*(indent+indent_step)+str(child)+'\n' for child in self.children])
            if children_string:
                return '{indent}<{tag_and_attrs}>\n' \
                '{children_string}' \
                '{indent}</{tag}>\n'.format(indent=' '*indent,tag_and_attrs=tag_and_attrs_string,children_string=children_string,tag=self.tag)
            else:
                return '{indent}<{tag_and_attrs}></{tag}>\n'.format(indent=' '*indent,tag_and_attrs=tag_and_attrs_string,tag=self.tag)
    def __str__(self):
        return self.to_string()
    def __len__(self):
        return len(self.children)
    def __call__(self, children:list=[]):
        if not isinstance(children,(list,)):
            assert isinstance(children,(Node,str))
            children=[children]
        self.children=children
        return self
    def to_file(self,filepath):
        with open(filepath,'w',encoding='utf-8') as f:
            f.write(self.to_string())
class Html(Node):
    tag = 'html'
class Head(Node):
    tag = 'head'
class Body(Node):
    tag = 'body'
class Header(Node):
    tag = 'header'
class Footer(Node):
    tag = 'footer'
class Link(Node):
    tag = 'link'
    self_closing = True
class Meta(Node):
    tag = 'meta'
    self_closing = True
class Title(Node):
    tag = 'title'
class Script(Node):
    tag = 'script'

class Nav(Node):
    tag = 'nav'
class Div(Node):
    tag = 'div'
class Span(Node):
    tag = 'span'
class H1(Node):
    tag = 'h1'
class H2(Node):
    tag = 'h2'
class H3(Node):
    tag = 'h3'
class H4(Node):
    tag = 'h4'
class H5(Node):
    tag = 'h5'
class H6(Node):
    tag = 'h6'
class P(Node):
    tag = 'p'
class Table(Node):
    tag = 'table'
class Caption(Node):
    tag = 'caption'
class Thead(Node):
    tag = 'thead'
class tbody(Node):
    tag = 'tbody'
class Tr(Node):
    tag = 'tr'
class Td(Node):
    tag = 'td'
class Th(Node):
    tag = 'th'
class Ul(Node):
    tag = 'ul'
class Ol(Node):
    tag = 'ol'
class Li(Node):
    tag = 'li'
class Form(Node):
    tag = 'form'
class Textarea(Node):
    tag = 'textarea'
class Input(Node):
    tag = 'input'
    self_closing = True
class Label(Node):
    tag = 'label'
class Select(Node):
    tag = 'select'
class A(Node):
    tag = 'a'
class B(Node):
    tag = 'b'
class Strong(Node):
    tag = 'strong'
class I(Node):
    tag = 'i'
class Em(Node):
    tag = 'em'
class Strike(Node):
    tag = 'strike'
class Del(Node):
    tag = 'del'
class Hr(Node):
    tag = 'Hr'
    self_closing = True
class Br(Node):
    tag = 'Br'
    self_closing = True
class U(Node):
    tag = 'u'
class Img(Node):
    tag = 'img'
class Sub(Node):
    tag = 'sub'
class Sup(Node):
    tag = 'sup'
class Big(Node):
    tag = 'big'
class Small(Node):
    tag = 'small'
class Button(Node):
    tag = 'button'

def smart_update_dict(dic1={},dic2={}):
    for k,v in dic2.items():
        if not k in dic1.keys():
            dic1[k]=v
        else:
            if isinstance(dic1[k],dict) and isinstance(dic2[k],dict):
                smart_update_dict(dic1[k],dic2[k])
            else:
                dic1[k]=v
