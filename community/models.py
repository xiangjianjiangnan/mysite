from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import exceptions
from ckeditor_uploader.fields import RichTextUploadingField

# 话题的发布，首先话题得有标题，正文，作者，发布时间，分类
class Topic(models.Model):
    # 话题标题，必填
    topic_title = models.CharField(max_length=50)
    # 话题内容，不能为空
    content = RichTextUploadingField()
    # 系统分类
    category = models.CharField(max_length=20)
    # 作者，这个作者是真是有账号的作者
    author = models.ForeignKey(User,on_delete=models.CASCADE) 
    read_num = models.IntegerField(default='0')
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Topic: %s>" % self.topic_title
    
    class Meta:
        ordering = ['-created_time',]


# 针对话题的评论
class TopicComment(models.Model):
    # 评论的话题
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    # 评论内容
    comment = RichTextUploadingField()
    #评论人
    user = models.ForeignKey(User, related_name="topic_user", on_delete=models.CASCADE)
    #评论时间
    comment_time = models.DateTimeField(auto_now_add=True)
    # 根评论
    root = models.ForeignKey('self', related_name="topic_root_comment", null=True, on_delete=models.CASCADE)
    # 上级评论
    parent = models.ForeignKey('self',related_name="topic_parent_comment",null=True, on_delete=models.CASCADE)
    # 被回复人
    reply_to = models.ForeignKey(User, related_name="topic_parent_user", null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-comment_time']

# 对话题的点赞
class LikeTopic(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    # 点赞状态，1表示支持，0表示反对
    like_status = models.IntegerField()
    like_time = models.DateTimeField(auto_now_add=True)



# 对话题评论的点赞
class LikeTopicComment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(TopicComment,on_delete=models.CASCADE)
    # 点赞状态，1表示支持，0表示反对
    like_status = models.IntegerField()
    like_time = models.DateTimeField(auto_now_add=True)