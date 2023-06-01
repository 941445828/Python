import random
def genrate_code(n):
    rad = 'qwertrfgafxgvaxbasgshjadgjhasdbhxsa'
    code = ''
    for i in range(n):
        ran = random.randint(0,len(rad)-1)
        code += rad[ran]
    return code

def login():
    username = input('请输入用户')
    password = input('请输入密码')
    code1 = genrate_code(5)
    print('验证码是',code1)
    code2 = input('请输入验证码')
    if code1.lower() == code2.lower():
        if username == '111' and password == '111':
            print('登陆成功')
        else:
            print('账户或密码错误')
    else:
        print('验证码错误')

login()
