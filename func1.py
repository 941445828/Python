islogin = False

good = 'ceshi'
def add_chrd(goodname):
    global islogin
    if islogin == True:
        print('登录成功')
        if goodname:
            print('{}加入成功'.format(goodname))
        else:
            print('没有商品名称')
    else:
        print('账户或密码错误，请重新输入')
        attempts = 0
        while attempts < 2:
            u = input('请输入你的账户: ')
            p = input('请输入你的密码: ')
            islogin = login(u, p)
            if islogin:
                break
            else:
                attempts += 1
                print('账户或密码错误，请重新输入')
        if attempts == 2:
            print('尝试次数超过限制，请稍后再试')
def login(username, password):
    if username == '176' and password == '176':
        return True
    else:
        return False

u = input('请输入你的账户: ')
p = input('请输入你的密码: ')
islogin = login(u, p)
add_chrd(good)




