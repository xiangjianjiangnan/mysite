from django.db import models
from article.models import Article
from django.contrib.auth.models import User
# 这个app是用来执行各种功能的，每个模块单独分开，不掺杂在一起

# 文章的评论
class ArticleComment(models.Model):
    # 评论的文章
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    # 评论内容
    text = models.TextField() 
    #评论人
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    #评论时间
    comment_time = models.DateTimeField(auto_now_add=True)
    # 根评论
    root = models.ForeignKey('self', related_name="root_comment", null=True, on_delete=models.CASCADE)
    # 上级评论
    parent = models.ForeignKey('self',related_name="parent_comment",null=True, on_delete=models.CASCADE)
    # 被回复人
    reply_to = models.ForeignKey(User, related_name="parent_user", null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']


# 对文章的点赞
class LikeArticle(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    like_time = models.DateTimeField(auto_now_add=True)


# 对评论的点赞
class LikeComment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(ArticleComment,on_delete=models.CASCADE)
    like_time = models.DateTimeField(auto_now_add=True)

# 对文章的收藏
class CollectArticle(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    collect_time = models.DateTimeField(auto_now_add=True)

# 对作者的关注
class FollowAuthor(models.Model):
    user = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="author",on_delete=models.CASCADE)
    follow_time = models.DateTimeField(auto_now_add=True)


# 发送邮件时的验证码保存，将来发送邮件的时候取出来作对比
# 一般验证邮箱、忘记密码、修改密码都会用到
class EmailVerify(models.Model):
    code = models.CharField(max_length=20, verbose_name="邮箱验证码")
    email = models.EmailField(max_length=200, verbose_name="发送邮箱")
    send_type = models.IntegerField(choices=((1,'register'),(2,'forget'),(3,'change')), verbose_name="验证码类型")
    post_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '邮箱验证码信息'
        verbose_name_plural = verbose_name 
        ordering = ['-post_time']


