def smart_update_dict(dic1={},dic2={}):
    for k,v in dic2.items():
        if not k in dic1.keys():
            dic1[k]=v
        else:
            if isinstance(dic1[k],dict) and isinstance(dic2[k],dict):
                smart_update_dict(dic1[k],dic2[k])
            else:
                dic1[k]=v
def inrange(n,rg):
    if n>=rg[0] and n<= rg[1]:return True
    return False
def split_dict(dic,keys):
    dic2={}
    for key in keys:
        if key in dic.keys():
            dic2[key]=dic[key]
    return dic2
