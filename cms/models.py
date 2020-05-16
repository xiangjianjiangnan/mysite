from django.db import models

# 各个页面的推荐
# 目前就只有文章、文选、作者这三个主体
class Recommend(models.Model):
    # 推荐类型，每个对应的数字代表着不同的推荐位置
    recommend_type =  models.IntegerField()
    # 推荐主体的id,用来寻找推荐的主体
    recommend_id = models.CharField(max_length=50, verbose_name="推荐id")
    # 推荐语，如果不写默认为推荐主体的标题
    recommend_text = models.CharField(max_length=200, verbose_name="推荐语")
    recommend_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-recommend_time']
