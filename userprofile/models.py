from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from shortuuidfield import ShortUUIDField

class Profile(models.Model):
    # uuid，这个id是个中长的id，不是从0开始的
    uid = ShortUUIDField(primary_key=True)
    # 用户，这个字段关联着django自带的用户模型
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 电话
    telephone = models.CharField(max_length=11,blank=True)  
    #生日,默认为注册时间 
    birthday = models.DateField(auto_now_add=True)
    # 性别
    sex = models.CharField(max_length=5,blank=True)
    # 头像
    portrait = models.ImageField(upload_to='heads/',blank=True,default='/img/userhead.jpg')
    # 城市
    city = models.CharField(max_length=20,blank=True)
    # 个性签名
    autograph = models.CharField(max_length=100,blank=True,default='这个人很懒，什么也没有写')
    # 身份证号
    id_card = models.CharField(max_length=18,blank=True)
    # 经验值
    exp = models.IntegerField(default='0')
    #等级，这个等级是根据经验值计算出来的
    rank = models.IntegerField(default='0')
    #硬币，这个硬币可以是网站活动赠与，也可以是充钱转化
    coin = models.IntegerField(default='0')
    # 段位，是一种荣誉字段，他的判定
    level = models.CharField(max_length=10,default='无')#段位
    # 荣誉徽章
    badge = models.ImageField(upload_to='badges/',blank=True)#徽章
    money = models.IntegerField(default='0')#钱包
    is_vip = models.BooleanField(default=False)#是否是会员
    vip_rank = models.IntegerField(default='0')#VIP等级

    def __str__(self):
        return 'user {}'.format(self.user.email)

@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
