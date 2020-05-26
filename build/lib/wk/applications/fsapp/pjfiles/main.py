from wk.extra.linux import *
if __name__ == '__main__':
    ip = get_local_ip()
    port = 80
    clean_port(port)
    files_dir = r'./learning_resources'
    from wk.web.applications.FileServer import FileServer
    app = FileServer(__name__, serve_root=files_dir)
    app.run(host=ip,port=port)