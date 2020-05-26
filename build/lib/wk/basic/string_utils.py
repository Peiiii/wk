
def get_time_formated(format='%Y-%m-%d %H:%M:%S'):
    import time
    return time.strftime(format,time.localtime())
def generate_hash(s,times=1):
    assert times>=1
    import hashlib
    m = hashlib.md5()
    def gen():
        m.update(s.encode('utf-8'))
        return m.hexdigest()[:10]
    for i in range(times):
        data=gen()
    return data