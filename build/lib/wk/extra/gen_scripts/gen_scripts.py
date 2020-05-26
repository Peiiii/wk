'''
prerequisites:
jinja2
'''


class Tem:
    def __init__(self, tem_file):
        from jinja2 import Template, Environment
        self.env = Environment()
        self.tem_file = tem_file
        self.tem = self.env.from_string(open(tem_file, 'r', encoding='utf-8').read())

    def render(self, *args, **kwargs):
        return self.tem.render(*args, **kwargs)

    def render_to_file(self, fp, *args, **kwargs):
        with open(fp, 'w', encoding='utf-8') as f:
            s = self.render(*args, **kwargs)
            f.write(s)
        return s


def gen_service(dst_file="./mysite", service_name='mysite', project_dir='/root/projects/mysite', script_file_name='main.py'):
    import pkg_resources
    tmp_path = pkg_resources.resource_filename('wk', 'data/templates/service.sh')
    tem = Tem(tmp_path)
    if dst_file:
        r = tem.render_to_file(fp=dst_file, service_name=service_name,
                               project_dir=project_dir,
                               script_file_name=script_file_name
                               )
    else:
        r = tem.render(service_name=service_name,
                       project_dir=project_dir,
                       script_file_name=script_file_name
                       )
    return r
