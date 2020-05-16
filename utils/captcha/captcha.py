from PIL import Image,ImageDraw,ImageFont
import random
import time
import os 
import string

class Captcha(object):
    # 字体位置
    font_path = os.path.join(os.path.dirname(__file__),'JOKERMAN.TTF')
    # 验证码数字个数
    number = 4
    # 验证码图片尺寸
    size = (80,40)
    # 设置背景为白色
    bgcolor = (0,0,0)
    # 随机字体颜色
    random.seed(int(time.time()))
    fontcolor = (random.randint(200,255),random.randint(100,255),random.randint(100,255))
    # 设置字体大小
    fontsize = 25
    # 随机然绕线颜色
    linecolor = (random.randint(0,250),random.randint(0,250),random.randint(0,250))
    # 是否加入干扰线
    draw_line = True
    # 是否加入干扰点
    draw_point = True
    # 加入干扰线条数
    line_number = 3

    SOURCE = list(string.ascii_letters)
    for index in range(0,10):
        SOURCE.append(str(index))

    # 定义类方法，私有，对象不能在外部使用
    # 随机从列表当中抽取4位，拼接成字符串
    @classmethod
    def gene_text(cls):
        return ''.join(random.sample(cls.SOURCE,cls.number))

    # 用来绘制干扰线
    @classmethod
    def __gene_line(cls,draw,width,height):
        begin = (random.randint(0,width),random.randint(0,height))
        end = (random.randint(0,width),random.randint(0,height))
        draw.line([begin,end],fill = cls.linecolor)
    # 用来绘制干扰点
    @classmethod
    def __gene_points(cls,draw,point_chance,width,height):
        chance = min(100,max(0,int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0,100)
                if tmp > 100 - chance:
                    draw.point((w,h),fill=(0,0,0))

    # 生成验证码
    @classmethod
    def gene_code(cls):
        # 宽和高
        width,height = cls.size
        # 创建画板
        image = Image.new('RGBA',(width,height),cls.bgcolor)
        # 设置验证码的字体
        font = ImageFont.truetype(cls.font_path,cls.fontsize)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 生成字符串
        text = cls.gene_text()
        font_width,font_height = font.getsize(text)
        draw.text(((width - font_width) / 2,(height - font_height) / 2),text,font=font,fill=cls.fontcolor)
        # 如果需要绘制干扰线
        if cls.draw_line:
            for x in range(0,cls.line_number):
                cls.__gene_line(draw,width,height)
        # 如果需要绘制干扰点
        if cls.draw_point:
            cls.__gene_points(draw,10,width,height)
        return (text,image)

