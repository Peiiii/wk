import os
pkg_dir=os.path.dirname(__file__)
pkg_data_dir=pkg_dir+'/data'
pkg_scripts_dir=pkg_data_dir+'/shell_scripts'
pkg_documents_dir=pkg_data_dir+'/documents'
pkg_static_dir=pkg_data_dir+'/static'
pkg_templates_dir=pkg_data_dir+'/templates'

def is_linux():
    import sys
    pf=sys.platform
    if pf=='linux':
        return True
    return False

def is_windows():
    import sys
    pf=sys.platform
    if pf=='win32':
        return True
    return False

