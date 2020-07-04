import time,datetime,random,uuid,json
def to_chinese_date(t):
    date=datetime.datetime.fromtimestamp(t)
    date=date.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
    return date
def get_time_formated(format='%Y-%m-%d %H:%M:%S'):
    import time
    return time.strftime(format, time.localtime())

def gen_random_key():
    return uuid.uuid4().hex
def gen_sms_code(length=6):
    s=''
    for i in range(length):
        n=random.randint(0,9)
        s+=str(n)
    return s
def gen_validation_code(length=6):
    s=''
    for i in range(length):
        n=random.randint(0,9)
        s+=str(n)
    return s
def generate_random_id():
    return uuid.uuid4().hex
def generate_hash(s, times=1):
    assert times >= 1
    import hashlib
    m = hashlib.md5()

    def gen():
        m.update(s.encode('utf-8'))
        return m.hexdigest()[:10]

    for i in range(times):
        data = gen()
    return data

def eval_json_string(text):
    try:
        return json.loads(text)
    except:
        return None
def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def is_all_alphabet(text=''):
    for char in text:
        if not char.isalpha():
            return False
    return True


def is_all_alphabet_or_digit(text=''):
    for char in text:
        if not char.isalpha() and not char.isdigit():
            return False
    return True
