# -*- coding=UTF-8 -*-


def heart(word):

    print('\n'.join([''.join([(word[(x - y) % len(word)] if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (
                x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(30, -30, -1)]))
def heart2(title='I Love You'):
    import turtle
    import time
    def liujia():
        for i in range(200):
            turtle.right(1)
            turtle.forward(1)

    turtle.color('red', 'pink')
    turtle.pensize(2)
    turtle.speed(10)
    turtle.goto(0, 0)

    turtle.begin_fill()
    turtle.left(140)
    turtle.forward(112)
    liujia()
    turtle.left(120)
    liujia()
    turtle.forward(112)
    turtle.end_fill()
    turtle.pensize(5)
    turtle.up()
    turtle.goto(-50, 142.7)
    turtle.left(50)
    turtle.down()
    turtle.forward(60)
    turtle.left(90)
    turtle.forward(25)
    turtle.up()
    turtle.goto(37.5, 142.7)
    turtle.down()
    turtle.forward(25)
    turtle.up()
    turtle.goto(50, 142.7)
    turtle.right(90)
    turtle.down()
    turtle.forward(60)
    for i in range(20):
        turtle.right(7.8)
        turtle.forward(0.3)
    turtle.forward(8)
    turtle.up()
    turtle.goto(100, -10)
    turtle.write(title)
    turtle.exitonclick()

def heart3():
    import turtle
    import time

    def draw_circle():
        for i in range(400):
            turtle.right(0.5)
            turtle.forward(1)

    def draw_love():
        #    turtle.color('red','darkred')
        #    turtle.pensize(1)
        turtle.pen(fillcolor="black", pencolor="red", pensize=8)
        turtle.speed(2000)
        turtle.goto(0, 0)
        turtle.begin_fill()
        turtle.left(140)
        turtle.forward(224)
        draw_circle()
        turtle.left(120)
        draw_circle()
        turtle.forward(224)
        turtle.end_fill()
        turtle.write("I Love you")
        time.sleep(2)
        turtle.up()
        turtle.goto(150, 20)
        turtle.color('black')
        turtle.write('相夕妄想 来日方长 很喜欢你 到此为止', font=("微软雅黑", 18, "normal"))
        time.sleep(2)

    def draw_abc():
        turtle.fillcolor("black")
        turtle.pencolor("red")
        turtle.pensize(10)
        turtle.speed(1)
        turtle.up()
        turtle.goto(0, -50)
        turtle.down()
        turtle.begin_fill()
        turtle.circle(45)
        turtle.end_fill()
        time.sleep(2)

    def word():
        turtle.up()
        turtle.goto(-100, 200)
        turtle.color("red")
        turtle.pensize(4)
        #   turtle.down()
        turtle.write('宝贝，你以为你是唯一吗？', font=("隶书", 18, "bold"))
        time.sleep(10)

    draw_love()
    draw_abc()
    word()
def heart4():
    import turtle
    import time

    # 画心形圆弧
    def hart_arc():
        for i in range(200):
            turtle.right(1)
            turtle.forward(2)

    def move_pen_position(x, y):
        turtle.hideturtle()  # 隐藏画笔（先）
        turtle.up()  # 提笔
        turtle.goto(x, y)  # 移动画笔到指定起始坐标（窗口中心为0,0）
        turtle.down()  # 下笔
        turtle.showturtle()  # 显示画笔

    love = input("请输入表白话语，默认为‘I Love You’：")
    signature = input("请签署你的大名，不填写默认不显示：")

    if love == '':
        love = 'I Love You'

    # 初始化
    turtle.setup(width=800, height=500)  # 窗口（画布）大小
    turtle.color('red', 'pink')  # 画笔颜色
    turtle.pensize(3)  # 画笔粗细
    turtle.speed(1)  # 描绘速度
    # 初始化画笔起始坐标
    move_pen_position(x=0, y=-180)  # 移动画笔位置
    turtle.left(140)  # 向左旋转140度

    turtle.begin_fill()  # 标记背景填充位置

    # 画心形直线（ 左下方 ）
    turtle.forward(224)  # 向前移动画笔，长度为224
    # 画爱心圆弧
    hart_arc()  # 左侧圆弧
    turtle.left(120)  # 调整画笔角度
    hart_arc()  # 右侧圆弧
    # 画心形直线（ 右下方 ）
    turtle.forward(224)

    turtle.end_fill()  # 标记背景填充结束位置

    # 在心形中写上表白话语
    move_pen_position(0, 0)  # 表白语位置
    turtle.hideturtle()  # 隐藏画笔
    turtle.color('#CD5C5C', 'pink')  # 字体颜色
    # font:设定字体、尺寸（电脑下存在的字体都可设置）  align:中心对齐
    turtle.write(love, font=('Arial', 30, 'bold'), align="center")

    # 签写署名
    if signature != '':
        turtle.color('red', 'pink')
        time.sleep(2)
        move_pen_position(180, -180)
        turtle.hideturtle()  # 隐藏画笔
        turtle.write(signature, font=('Arial', 20), align="center")

    # 点击窗口关闭程序
    window = turtle.Screen()
    window.exitonclick()
def tree1():
    import turtle as tl
    def draw_smalltree(tree_length, tree_angle):
        '''
        绘制分形树函数
        '''
        if tree_length >= 3:
            tl.forward(tree_length)  # 往前画
            tl.right(tree_angle)  # 往右转
            draw_smalltree(tree_length - 10, tree_angle)  # 画下一枝，直到画到树枝长小于3

            tl.left(2 * tree_angle)  # 转向画左
            draw_smalltree(tree_length - 10, tree_angle)  # 直到画到树枝长小于3

            tl.rt(tree_angle)  # 转到正向上的方向，然后回溯到上一层
            if tree_length <= 30:  # 树枝长小于30，可以当作树叶了，树叶部分为绿色
                tl.pencolor('green')
            if tree_length > 30:
                tl.pencolor('brown')  # 树干部分为棕色
            tl.backward(tree_length)  # 往回画，回溯到上一层

    tl.penup()
    # tl.pencolor('green')
    tl.left(90)  # 因为树是往上的，所以先把方向转左
    tl.backward(250)  # 把起点放到底部
    tl.pendown()
    tree_length = 100  # 我设置的最长树干为100
    tree_angle = 20  # 树枝分叉角度，我设为20
    draw_smalltree(tree_length, tree_angle)
    tl.exitonclick()  # 点击才关闭画画窗口

def tree2():
    import turtle

    def draw_brach(brach_length):

        if brach_length > 5:
            if brach_length < 40:
                turtle.color('green')

            else:
                turtle.color('red')

            # 绘制右侧的树枝
            turtle.forward(brach_length)
            print('向前', brach_length)
            turtle.right(25)
            print('右转20')
            draw_brach(brach_length - 15)
            # 绘制左侧的树枝
            turtle.left(50)
            print('左转40')
            draw_brach(brach_length - 15)

            if brach_length < 40:
                turtle.color('green')

            else:
                turtle.color('red')

            # 返回之前的树枝上
            turtle.right(25)
            print('右转20')
            turtle.backward(brach_length)
            print('返回', brach_length)

    def main():
        turtle.left(90)
        turtle.penup()
        turtle.backward(150)
        turtle.pendown()
        turtle.color('red')

        draw_brach(100)

        turtle.exitonclick()
    main()

def tree3():
    import turtle as tl

    def draw_smalltree(tree_length, tree_angle, tree_wide):
        '''
        绘制分形树函数
        '''
        if tree_length >= 5:
            tl.pensize(tree_wide)
            tl.forward(tree_length)  # 往前画
            tl.right(tree_angle)  # 往右转
            draw_smalltree(tree_length - 10, tree_angle, tree_wide * 2 / 3)  # 画下一枝，直到画到树枝长小于3

            tl.left(2 * tree_angle)  # 转向画左
            draw_smalltree(tree_length - 10, tree_angle, tree_wide * 2 / 3)  # 直到画到树枝长小于3

            tl.rt(tree_angle)  # 转到正向上的方向，然后回溯到上一层
            if tree_length <= 30:  # 树枝长小于30，可以当作树叶了，树叶部分为绿色
                tl.pencolor('green')
            if tree_length > 30:
                tl.pencolor('brown')  # 树干部分为棕色

            tl.pensize(tree_wide)
            tl.backward(tree_length)  # 往回画，回溯到上一层

    def main():
        tl.screensize(100, 100, "black")  # 画布大小
        tl.penup()
        tl.left(90)  # 因为树是往上的，所以先把方向转左
        tl.backward(250)  # 把起点放到底部
        tl.pendown()
        tl.pencolor('brown')
        tl.speed(10)
        tree_length = 80  # 我设置的最长树干为80
        tree_angle = 20  # 树枝分叉角度，我设为20
        tree_wide = 5  # 树枝粗度
        draw_smalltree(tree_length, tree_angle, tree_wide)
        tl.exitonclick()  # 点击才关闭画画窗口
    main()

def tree4():
    '''表白用'''

    import turtle
    import random
    def love(x, y):  # 在(x,y)处画爱心lalala
        lv = turtle.Turtle()
        lv.hideturtle()
        lv.up()
        lv.goto(x, y)  # 定位到(x,y)

        def curvemove():  # 画圆弧
            for i in range(20):
                lv.right(10)
                lv.forward(2)

        lv.color('red', 'pink')
        lv.speed(10000000)
        lv.pensize(1)
        # 开始画爱心lalala
        lv.down()
        lv.begin_fill()
        lv.left(140)
        lv.forward(22)
        curvemove()
        lv.left(120)
        curvemove()
        lv.forward(22)
        lv.write("GPA", font=("Arial", 12, "normal"), align="center")  # 写上表白的人的名字
        lv.left(140)  # 画完复位
        lv.end_fill()

    def tree(branchLen, t):
        if branchLen > 5:  # 剩余树枝太少要结束递归
            if branchLen < 20:  # 如果树枝剩余长度较短则变绿
                t.color("green")
                t.pensize(random.uniform((branchLen + 5) / 4 - 2, (branchLen + 6) / 4 + 5))
                t.down()
                t.forward(branchLen)
                love(t.xcor(), t.ycor())  # 传输现在turtle的坐标
                t.up()
                t.backward(branchLen)
                t.color("brown")
                return
            t.pensize(random.uniform((branchLen + 5) / 4 - 2, (branchLen + 6) / 4 + 5))
            t.down()
            t.forward(branchLen)
            # 以下递归
            ang = random.uniform(15, 45)
            t.right(ang)
            tree(branchLen - random.uniform(12, 16), t)  # 随机决定减小长度
            t.left(2 * ang)
            tree(branchLen - random.uniform(12, 16), t)  # 随机决定减小长度
            t.right(ang)
            t.up()
            t.backward(branchLen)

    myWin = turtle.Screen()
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(1000)
    t.left(90)
    t.up()
    t.backward(200)
    t.down()
    t.color("brown")
    t.pensize(32)
    t.forward(60)
    tree(100, t)
    myWin.exitonclick()

def rose1():
    from turtle import pensize,showturtle,penup,pendown,left,fd,right,fillcolor,begin_fill,circle,setheading,end_fill,done
    # 初始化一下，摆好姿势...
    pensize(2)
    showturtle()
    penup()
    left(90)
    fd(200)
    pendown()
    right(90)
    # 来一个火辣辣的花蕊，代表我对你深深的爱...
    fillcolor("red")
    begin_fill()
    circle(10, 180)
    circle(25, 110)
    left(50)
    circle(60, 45)
    circle(20, 170)
    right(24)
    fd(30)
    left(10)
    circle(30, 110)
    fd(20)
    left(40)
    circle(90, 70)
    circle(30, 150)
    right(30)
    fd(15)
    circle(80, 90)
    left(15)
    fd(45)
    right(165)
    fd(20)
    left(155)
    circle(150, 80)
    left(50)
    circle(150, 90)
    end_fill()
    # 来一些花瓣，让她爱上我
    left(150)
    circle(-90, 70)
    left(20)
    circle(75, 105)
    setheading(60)
    circle(80, 98)
    circle(-90, 40)
    # 再来一些花瓣，让她爱上我
    left(180)
    circle(90, 40)
    circle(-80, 98)
    setheading(-83)
    # 来一片绿油油的叶子...
    fd(30)
    left(90)
    fd(25)
    left(45)
    fillcolor("green")
    begin_fill()
    circle(-80, 90)
    right(90)
    circle(-80, 90)
    end_fill()
    right(135)
    fd(60)
    left(180)
    fd(85)
    left(90)
    fd(80)
    # 再来一片绿油油的叶子...
    right(90)
    right(45)
    fillcolor("green")
    begin_fill()
    circle(80, 90)
    left(90)
    circle(80, 90)
    end_fill()
    left(135)
    fd(60)
    left(180)
    fd(60)
    left(90)
    circle(200, -60)
    done()
def peppa():
    import turtle as t
    t.pensize(4)
    t.hideturtle()
    t.colormode(255)
    t.color((255, 155, 192), "pink")
    t.setup(840, 500)
    t.speed(10)

    # 鼻子
    t.pu()
    t.goto(-100, 100)
    t.pd()
    t.seth(-30)
    t.begin_fill()
    a = 0.4
    for i in range(120):
        if 0 <= i < 30 or 60 <= i < 90:
            a = a + 0.08
            t.lt(3)  # 向左转3度
            t.fd(a)  # 向前走a的步长
        else:
            a = a - 0.08
            t.lt(3)
            t.fd(a)
    t.end_fill()

    t.pu()
    t.seth(90)
    t.fd(25)
    t.seth(0)
    t.fd(10)
    t.pd()
    t.pencolor(255, 155, 192)
    t.seth(10)
    t.begin_fill()
    t.circle(5)
    t.color(160, 82, 45)
    t.end_fill()

    t.pu()
    t.seth(0)
    t.fd(20)
    t.pd()
    t.pencolor(255, 155, 192)
    t.seth(10)
    t.begin_fill()
    t.circle(5)
    t.color(160, 82, 45)
    t.end_fill()

    # 头
    t.color((255, 155, 192), "pink")
    t.pu()
    t.seth(90)
    t.fd(41)
    t.seth(0)
    t.fd(0)
    t.pd()
    t.begin_fill()
    t.seth(180)
    t.circle(300, -30)
    t.circle(100, -60)
    t.circle(80, -100)
    t.circle(150, -20)
    t.circle(60, -95)
    t.seth(161)
    t.circle(-300, 15)
    t.pu()
    t.goto(-100, 100)
    t.pd()
    t.seth(-30)
    a = 0.4
    for i in range(60):
        if 0 <= i < 30 or 60 <= i < 90:
            a = a + 0.08
            t.lt(3)  # 向左转3度
            t.fd(a)  # 向前走a的步长
        else:
            a = a - 0.08
            t.lt(3)
            t.fd(a)
    t.end_fill()

    # 耳朵
    t.color((255, 155, 192), "pink")
    t.pu()
    t.seth(90)
    t.fd(-7)
    t.seth(0)
    t.fd(70)
    t.pd()
    t.begin_fill()
    t.seth(100)
    t.circle(-50, 50)
    t.circle(-10, 120)
    t.circle(-50, 54)
    t.end_fill()

    t.pu()
    t.seth(90)
    t.fd(-12)
    t.seth(0)
    t.fd(30)
    t.pd()
    t.begin_fill()
    t.seth(100)
    t.circle(-50, 50)
    t.circle(-10, 120)
    t.circle(-50, 56)
    t.end_fill()

    # 眼睛
    t.color((255, 155, 192), "white")
    t.pu()
    t.seth(90)
    t.fd(-20)
    t.seth(0)
    t.fd(-95)
    t.pd()
    t.begin_fill()
    t.circle(15)
    t.end_fill()

    t.color("black")
    t.pu()
    t.seth(90)
    t.fd(12)
    t.seth(0)
    t.fd(-3)
    t.pd()
    t.begin_fill()
    t.circle(3)
    t.end_fill()

    t.color((255, 155, 192), "white")
    t.pu()
    t.seth(90)
    t.fd(-25)
    t.seth(0)
    t.fd(40)
    t.pd()
    t.begin_fill()
    t.circle(15)
    t.end_fill()

    t.color("black")
    t.pu()
    t.seth(90)
    t.fd(12)
    t.seth(0)
    t.fd(-3)
    t.pd()
    t.begin_fill()
    t.circle(3)
    t.end_fill()

    # 腮
    t.color((255, 155, 192))
    t.pu()
    t.seth(90)
    t.fd(-95)
    t.seth(0)
    t.fd(65)
    t.pd()
    t.begin_fill()
    t.circle(30)
    t.end_fill()

    # 嘴
    t.color(239, 69, 19)
    t.pu()
    t.seth(90)
    t.fd(15)
    t.seth(0)
    t.fd(-100)
    t.pd()
    t.seth(-80)
    t.circle(30, 40)
    t.circle(40, 80)

    # 身体
    t.color("red", (255, 99, 71))
    t.pu()
    t.seth(90)
    t.fd(-20)
    t.seth(0)
    t.fd(-78)
    t.pd()
    t.begin_fill()
    t.seth(-130)
    t.circle(100, 10)
    t.circle(300, 30)
    t.seth(0)
    t.fd(230)
    t.seth(90)
    t.circle(300, 30)
    t.circle(100, 3)
    t.color((255, 155, 192), (255, 100, 100))
    t.seth(-135)
    t.circle(-80, 63)
    t.circle(-150, 24)
    t.end_fill()

    # 手
    t.color((255, 155, 192))
    t.pu()
    t.seth(90)
    t.fd(-40)
    t.seth(0)
    t.fd(-27)
    t.pd()
    t.seth(-160)
    t.circle(300, 15)
    t.pu()
    t.seth(90)
    t.fd(15)
    t.seth(0)
    t.fd(0)
    t.pd()
    t.seth(-10)
    t.circle(-20, 90)

    t.pu()
    t.seth(90)
    t.fd(30)
    t.seth(0)
    t.fd(237)
    t.pd()
    t.seth(-20)
    t.circle(-300, 15)
    t.pu()
    t.seth(90)
    t.fd(20)
    t.seth(0)
    t.fd(0)
    t.pd()
    t.seth(-170)
    t.circle(20, 90)

    # 脚
    t.pensize(10)
    t.color((240, 128, 128))
    t.pu()
    t.seth(90)
    t.fd(-75)
    t.seth(0)
    t.fd(-180)
    t.pd()
    t.seth(-90)
    t.fd(40)
    t.seth(-180)
    t.color("black")
    t.pensize(15)
    t.fd(20)

    t.pensize(10)
    t.color((240, 128, 128))
    t.pu()
    t.seth(90)
    t.fd(40)
    t.seth(0)
    t.fd(90)
    t.pd()
    t.seth(-90)
    t.fd(40)
    t.seth(-180)
    t.color("black")
    t.pensize(15)
    t.fd(20)

    # 尾巴
    t.pensize(4)
    t.color((255, 155, 192))
    t.pu()
    t.seth(90)
    t.fd(70)
    t.seth(0)
    t.fd(95)
    t.pd()
    t.seth(0)
    t.circle(70, 20)
    t.circle(10, 330)
    t.circle(70, 30)

if __name__ == '__main__':
    import fire
    fire.Fire()