from wk.extra.linux import *
from wk.io import load_simple_config
if __name__ == '__main__':
    ip = get_local_ip()
    # ip = '127.0.0.1'
    port = 80
    clean_port(port)
    config=load_simple_config(
        # './windows.cfg',
        './config.cfg',
    )
    from wk.web.applications.knowledge_platform import KnowledgePlatform
    app = KnowledgePlatform(__name__, config=config)
    app.run(host=ip,port=port)
