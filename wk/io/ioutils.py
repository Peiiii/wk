

def pickle_dump(obj,fp):
    import pickle
    with open(fp,'wb') as f:
        pickle.dump(obj,f)
def pickle_load(fp):
    import pickle
    with open(fp,'rb') as f:
        return pickle.load(f)
def json_load(f,encoding='utf-8',*args,**kwargs):
    import json
    with open(f,'r',encoding=encoding) as fp:
        return json.load(fp,*args,**kwargs)
def json_dump(obj,fp,encoding='utf-8',*args,**kwargs):
    import json
    with open(fp,'w',encoding=encoding) as f:
        json.dump(obj,f,*args,**kwargs)
def read_txt(path,encoding='utf-8'):
    with open(path,'r',encoding=encoding) as f:
        return f.read()
def write_txt(txt,path,encoding='utf-8'):
    with open(path,'w',encoding=encoding) as f:
        f.write(txt)
def write_config(config,path,splitchar='='):
    open(path,'w').close()
    f=open(path,'a')
    for k,v in config.items():
        if isinstance(v,str):
            f.write('%s %s %s\n' % (key,splitchar,value))
        else:
            f.write('[%s]\n'%(k))
            assert isinstance(v,dict)
            for key,value in v.items():
                f.write('%s %s %s\n' % (key,splitchar,value))
def read_config(path,splitchar='=',comment_tag='#'):
    f=open(path,'r')
    config={}
    section_open=False
    current_section=None
    while True:
        s=f.readline()
        if not s:
            break
        if s.strip()=='':
            continue
        s=s.strip()
        if s.startswith('#'):
            continue
        if s.startswith('[') and s.endswith(']'):
            s=s[1:-1]
            assert '[' not in s and ']' not in s
            current_section=s
            config[current_section]={}
            section_open=True
            continue
        key,value=s.split(splitchar)
        key=key.strip()
        value=value.strip()
        if section_open:
            config[current_section][key]=value
        else:
            config[key]=value
    f.close()
    return config
def load_simple_config(fp,line_split='\n',pair_split='=',encoding="utf-8"):
    with open(fp,'r',encoding=encoding) as f:
        lines=f.read().strip().split(line_split)
        dic={}
        for line in lines:
            if line.strip().startswith('#'):continue
            line=line.strip()
            key,value=line.split(pair_split)
            key=key.strip()
            value=value.strip()
            dic[key]=value
        return dic
def dump_iterables_to_string(lis,template):
    if not template:
        return lis
    assert isinstance(template, (list, tuple, set))
    length = len(template)
    next_template = None
    cls = template[0]
    if length == 1:
        return str(lis)
    else:
        if cls in [list, set, tuple]:
            lis=list(lis)
            assert length>=2
            splitchar=template[1]
            if length>=3:
                next_template=template[2]
            if next_template:
                for i,item in enumerate(lis):
                    item = dump_iterables_to_string(item,next_template)
                    lis[i]=item
            text = splitchar.join(lis)
            return text
        elif cls in [dict]:
            assert length>=3
            item_split=template[1]
            kv_split=template[2]
            items=[]
            for k,v in lis.items():
                if next_template:
                    v=dump_iterables_to_string(v,next_template)
                text=kv_split.join([k,v])
                items.append(text)
            text=item_split.join(items)
            return text

def load_iterables_from_string(text='',template=[list,'\n']):
    '''
    # [list,'\n',[dict,' ',':',[list,' ',[list,',']]]]
    '''
    if not template:
        return text
    assert isinstance(template, (list, tuple, set))
    length = len(template)
    next_template=None
    cls = template[0]
    if length==1:
        return cls(text)
    else:
        if cls in [list,set,tuple]:
            assert length>=2
            splitchar=template[1]
            if length>=3:
                next_template=template[2]
            items=text.split(splitchar)
            if next_template:
                for i,item in enumerate(items):
                    items[i]=load_iterables_from_string(item,next_template)
            items=cls(items)
            return items
        elif cls in [dict]:
            assert length >= 3
            item_split=template[1]
            kv_split=template[2]
            if length>=4:
                next_template=template[3]
            dic={}
            items=text.split(item_split)
            for item in items:
                k,v =item.split(kv_split,maxsplit=1)
                if next_template:
                    v = load_iterables_from_string(v, next_template)
                dic[k]=v
            return dic
