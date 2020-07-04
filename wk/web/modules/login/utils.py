import wk
import re
def checkEmail(email):

    c = re.compile(r'^\w+@(\w+\.)+(com|cn|net)$')
    s = c.search(email)
    if s:
        return True
    return False


def checkPhone(number):
    n=number
    info=[]
    if re.match(r'1[3,4,5,7,8]\d{9}', n):
        # print("您输入的的手机号码是：\n", n)
        # 中国联通：
        # 130，131，132，155，156，185，186，145，176
        if re.match(r'13[0,1,2]\d{8}', n) or \
                re.match(r"15[5,6]\d{8}", n) or \
                re.match(r"18[5,6]", n) or \
                re.match(r"145\d{8}", n) or \
                re.match(r"176\d{8}", n):
            info.append("该号码属于：中国联通")

        # 中国移动
        # 134, 135 , 136, 137, 138, 139, 147, 150, 151,
        # 152, 157, 158, 159, 178, 182, 183, 184, 187, 188；
        elif re.match(r"13[4,5,6,7,8,9]\d{8}", n) or \
                re.match(r"147\d{8}|178\d{8}", n) or \
                re.match(r"15[0,1,2,7,8,9]\d{8}", n) or \
                re.match(r"18[2,3,4,7,8]\d{8}", n):
            info.append("该号码属于：中国移动")
        else:
            # 中国电信
            # 133,153,189
            info.append("该号码属于：中国电信")
        return True
    else:
        return False
