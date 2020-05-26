import wk


class NodeMetaClass(type):
    def __new__(cls, name, bases, attrs):
        debug=False
        if name == None:
            debug=True
        dict_attrs=['_attrs','environment']
        for name in dict_attrs:
            if name in attrs.keys():
                _attrs = attrs[name]
                tmp_dict = {}
                assert isinstance(_attrs, dict)
                for base in bases:
                    if hasattr(base, name):
                        base_attrs = getattr(base, name)
                        tmp_dict.update(**base_attrs)
                tmp_dict.update(**_attrs)
                attrs[name] = tmp_dict
        return type.__new__(cls, name, bases, attrs)


class Node(metaclass=NodeMetaClass):
    tag = 'Node'
    self_closing = False
    _attrs = {}
    _children = []
    environment={}
    def __init__(self, **kwargs):
        def preprocess(kwargs):
            cls_attr = '_class'
            if cls_attr in kwargs.keys():
                kwargs['class'] = kwargs.pop(cls_attr)
            return kwargs

        self.attrs = {}
        self.attrs.update(**self._attrs)
        self.attrs = preprocess(self.attrs)
        self.children = self._children
        kwargs = preprocess(kwargs)
        children_name = 'children'
        if children_name in kwargs.keys():
            self.children = kwargs.pop(children_name)
        self.attrs.update(**kwargs)

    def to_string(self, indent=0, indent_step=2):
        tag_and_attrs_string = ' '.join([self.tag] + ['%s="%s"' % (name, value) for name, value in self.attrs.items()])
        if self.self_closing:
            return '<{tag_and_attrs}>'.format(indent=' ' * indent, tag_and_attrs=tag_and_attrs_string)
        else:
            if len(self.children) == 1:
                "Handle such case that the child is text or Var with type of text"
                child = self.children[0]
                if isinstance(child, (str,)):
                    children_string = str(child)
                    return '<{tag_and_attrs}>{children_string}</{tag}>'.format(tag_and_attrs=tag_and_attrs_string,
                                                                               children_string=children_string,
                                                                               tag=self.tag)
                elif isinstance(child, Var) and child.attrs['type'] == 'text':
                    children_string = child.to_string(indent=indent, indent_step=indent_step)
                    return '<{tag_and_attrs}>{children_string}</{tag}>'.format(tag_and_attrs=tag_and_attrs_string,
                                                                               children_string=children_string,
                                                                               tag=self.tag)

            children_string = '\n{indent}'.format(indent=' ' * (indent + indent_step)).join([child.to_string(
                indent=indent + indent_step, indent_step=indent_step) if isinstance(child, (Node,)) else ' ' * (
                    indent + indent_step) + str(child) + '\n' for child in self.children])
            if children_string:
                return '<{tag_and_attrs}>\n{next_indent}' \
                       '{children_string}' \
                       '\n{indent}</{tag}>'.format(next_indent=' ' * (indent + indent_step), indent=' ' * indent,
                                                   tag_and_attrs=tag_and_attrs_string, children_string=children_string,
                                                   tag=self.tag)
            else:
                return '<{tag_and_attrs}></{tag}>'.format(tag_and_attrs=tag_and_attrs_string, tag=self.tag)

    def __str__(self):
        return self.to_string()

    def __len__(self):
        return len(self.children)

    def __call__(self, children: list = []):
        if not isinstance(children, (list,)):
            assert isinstance(children, (Node, str, Var))
            children = [children]
        self.children = children
        return self

    def to_file(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.render())

    def compile(self, **kwargs):
        ''' replace var with specific object , if the object is a list . the insert every element in this list into self.children'''
        if not len(self.children):
            return self
        index=0
        for i in range(len(self.children)):
            child=self.children[index]
            if isinstance(child, str):
                continue
            if isinstance(child, Var):
                name = child.attrs['name']
                if name in kwargs.keys():
                    self.children.pop(index)
                    new_nodes=kwargs[name]
                    if not  isinstance(new_nodes,(tuple,list)):
                        new_nodes=[new_nodes]
                    for new_node in new_nodes:
                        self.children.insert(index,new_node)
                        index+=1
                else:
                    self.children[index] = child.compile(**kwargs)
                    index+=1
            else:
                self.children[index] = child.compile(**kwargs)
                index+=1
        return self

    def render(self, **kwargs):
        render_kwargs={}
        render_kwargs.update(**self.environment)
        render_kwargs.update(**kwargs)
        from jinja2 import Environment
        tem = Environment().from_string(self.to_string())
        return tem.render(**render_kwargs)


class Var(Node):
    tag = 'var'
    _attrs = dict(type='node')

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)

    def to_string(self, indent=0, indent_step=2):
        if len(self.children) == 1:
            child = self.children[0]
            if isinstance(child, (str,)):
                return str(child)
            elif isinstance(child, Var) and child.attrs['type'] == 'text':
                return child.to_string(indent=indent, indent_step=indent_step)

        children_string = '\n{indent}'.format(indent=' ' * (indent)).join([child.to_string(
            indent=indent, indent_step=indent_step) if isinstance(child, (Node,)) else ' ' * (
            indent) + str(child) + '\n' for child in self.children])
        if children_string:
            return children_string
        else:
            return ''


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


class Style(Node):
    tag = 'style'


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
    tag = 'hr'
    self_closing = True


class Br(Node):
    tag = 'br'
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


def smart_update_dict(dic1={}, dic2={}):
    '''if the some-value is also a dict , then try to update only the smaller dict'''
    for k, v in dic2.items():
        if not k in dic1.keys():
            dic1[k] = v
        else:
            if isinstance(dic1[k], dict) and isinstance(dic2[k], dict):
                smart_update_dict(dic1[k], dic2[k])
            else:
                dic1[k] = v
    return dic1
