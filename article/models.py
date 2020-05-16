from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import exceptions
from ckeditor_uploader.fields import RichTextUploadingField

# 关于是用User做关联还是Profile的思考：
# 1、关联的目的是为了找到用户信息，尤其是用户名，这一点上两个都能做到
# 2、首先用户登录肯定是用User中的账号密码登录，后端显示文章肯定也是根据传递的用户模型去搜索进行返回
# 3、无疑肯定是直接用User最直接，然后通过user.username找到用户名然后进行标注就可以了

# 模型之间的关系设定：
# 1、文章肯定是主题，所有功能都通过文章来设计
# 2、但是每篇文章必须要有一个单独的文章集合属性，这个属性可定设定多个，相当于文章集合与文章是一对多的关系
class Anthology(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    anthology_title = models.CharField(max_length=20,default='默认文选')
    anthology_cover = models.ImageField(upload_to='covers/',default='covers/anthology.jpg')
    anthology_describe = models.CharField(max_length=200,default='暂无描述')
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.anthology_title


# class Tag(models.Model):
#     tag = models.CharField(max_length=20)

    # class Meta:
    #     db_table = 'tag'



# class Category(models.Model):
#     category = models.CharField(max_length=20)

    
    # class Meta:
    #     db_table = 'category'


# 注意
# 1、其实在这个文章模型中最特殊的是文章集合，当用户点击文章集合的时候必须要按照一定的顺序显示
# 2、那么问题是，如果我的文章刚开始是随意写的，最后想要按照一定的顺序进行排序，怎么办，
#    这就需要搭配一个序列号字段，序列号字段是需要用户自主填写的
#  
class Article(models.Model):
    # 文章标题，必填
    article_title = models.CharField(max_length=50)
    # 引入文集的外键，一对多，这个字段可以由
    anthology = models.ForeignKey(Anthology,on_delete=models.CASCADE,null=True)
    # 自主标签
    # tags = models.ManyToManyField(Tag,related_name='articles')
    # 系统分类
    category = models.CharField(max_length=20,default='数据分析')
    # categorys = models.ManyToManyField(Category,related_name='articles')
    # 文章序列号，用来表明这是“文集”的第几个，默认为第一个
    serial = models.IntegerField(default='1')
    # 作者，这个作者是真是有账号的作者
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    # 作者，这个作者是假作者，用来备用，没有对应的用户，只是单纯的字符串
    author_copy = models.CharField(max_length=20,blank=True)
    # 文章摘要，用来简明扼要的阐述主题，可以为空
    summary = models.CharField(max_length=200,blank=True)
    # 文章内容，不能为空
    content = RichTextUploadingField()
    # 文章封面，不能为空，用来做推荐时候的封面
    article_cover = models.ImageField(upload_to='covers/')
    
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    # 文章排序功能，可排序的字段为：最近投稿、阅读次数最多、阅读人数最多、点赞最多、收藏最多、评论最多
    read_num = models.IntegerField(default='0')
    reader_num = models.IntegerField(default='0')
    like_num = models.IntegerField(default='0')
    collect_num = models.IntegerField(default='0')
    comment_num = models.IntegerField(default='0')
    # 公开状态，默认公开，关闭则只对自己可见
    # is_open = models.BooleanField(default=True,verbose_name='公开状态')
    # 激活状态，默认激活，不激活则显示被删除，这个是逻辑删除字段
    is_active = models.BooleanField(default=True)
    #是否需要付费，默认不需要
    is_pay = models.BooleanField(default=False)
    # 需要支付多少钱
    need_pay = models.IntegerField(default='0')

        

    def __str__(self):
        return "<Article: %s>" % self.article_title
    
    class Meta:
        ordering = ['-created_time',]

    # class Meta:
    #     db_table = 'article'
    

class ReaderNum(models.Model):
    reader = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    # 第一次阅读的时间
    once_read_time = models.DateTimeField(auto_now_add=True)
    # 重新阅读的时间
    more_read_time = models.DateTimeField(auto_now=True)
