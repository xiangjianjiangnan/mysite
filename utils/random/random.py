
from random import choice,randrange
from mysite import settings

# 生成一个随机的字符串，作为邮箱储存的验证码
def get_random_code(code_length):
    code_source = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(code_length):
        # 随机选择一个字符，根据指定的验证码长度，添加到code中
        # random_str = code_source[0:-1]
        # code += random_str
        code += choice(code_source)
    return code




