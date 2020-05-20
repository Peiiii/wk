def smart_update_dict(dic1={},dic2={}):
    for k,v in dic2.items():
        if not k in dic1.keys():
            dic1[k]=v
        else:
            if isinstance(dic1[k],dict) and isinstance(dic2[k],dict):
                smart_update_dict(dic1[k],dic2[k])
            else:
                dic1[k]=v