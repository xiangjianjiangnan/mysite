from django import template
from ..models import ArticleComment,LikeArticle,LikeComment,CollectArticle,FollowAuthor
from community.models import LikeTopic,LikeTopicComment,TopicComment
from article.models import Anthology,Article

register = template.Library()
# 生成每篇文章的评论数
@register.simple_tag
def get_article_comments_count(obj):
    article_comments_count = ArticleComment.objects.filter(article=obj).count()
    return article_comments_count

# 生成每篇文章的点赞数
@register.simple_tag
def get_article_likes_count(obj):
    article_likes_count = LikeArticle.objects.filter(article=obj).count()
    return article_likes_count

# 生成用户对某篇文章的点赞状态
@register.simple_tag(takes_context=True)
def get_user_likearticle_status(context,obj):
    user = context['user']
    # 如果用户未登录，返回空字符串
    if not user.is_authenticated:
        return ''
    user_like_status = LikeArticle.objects.filter(article=obj,user=user).exists()
    # 如果用户有点赞记录，则返回激活状态
    if user_like_status:
        return 'active'
    # 如果没有该用户的点赞记录，则返回空字符串
    else:
        return ''

# 生成每条评论的点赞数
@register.simple_tag
def get_comment_likes_count(obj):
    comment_likes_count = LikeComment.objects.filter(comment=obj).count()
    return comment_likes_count

# 生成用户对某篇文章的点赞状态
@register.simple_tag(takes_context=True)
def get_user_likecomment_status(context,obj):
    user = context['user']
    # 如果用户未登录，返回空字符串
    if not user.is_authenticated:
        return ''
    user_like_status = LikeComment.objects.filter(comment=obj,user=user).exists()
    # 如果用户有点赞记录，则返回激活状态
    if user_like_status:
        return 'active'
    # 如果没有该用户的点赞记录，则返回空字符串
    else:
        return ''

# 生成每篇文章的收藏数
@register.simple_tag
def get_article_collects_count(obj):
    article_collects_count = CollectArticle.objects.filter(article=obj).count()
    return article_collects_count

# 生成用户对某篇文章的点赞状态
@register.simple_tag(takes_context=True)
def get_user_collectarticle_status(context,obj):
    user = context['user']
    # 如果用户未登录，返回空字符串
    if not user.is_authenticated:
        return ''
    user_collect_status = CollectArticle.objects.filter(article=obj,user=user).exists()
    # 如果用户有点赞记录，则返回激活状态
    if user_collect_status:
        return 'active'
    # 如果没有该用户的点赞记录，则返回空字符串
    else:
        return ''

# 生成用户对某篇文章的点赞状态
@register.simple_tag(takes_context=True)
def get_user_follow_status(context,obj):
    user = context['user']
    # 如果用户未登录，返回空字符串
    if not user.is_authenticated:
        return '+ 关注'
    user_follow_status = FollowAuthor.objects.filter(author=obj,user=user).exists()
    # 如果用户有点赞记录，则返回激活状态
    if user_follow_status:
        return '已关注'
    # 如果没有该用户的点赞记录，则返回空字符串
    else:
        return '+ 关注'

# 生成该作者创做文选的篇数
@register.simple_tag
def get_author_anthologys_count(obj):
    author_anthologys_count = Anthology.objects.filter(author=obj).count()
    return author_anthologys_count

# 生成该作者创做文章的篇数
@register.simple_tag
def get_author_articles_count(obj):
    author_articles_count = Article.objects.filter(author=obj).count()
    return author_articles_count

# 生成该作者受到的关注人数
@register.simple_tag
def get_author_followers_count(obj):
    author_followers_count = FollowAuthor.objects.filter(author=obj).count()
    return author_followers_count

# 生成该作者关注的人数
@register.simple_tag
def get_author_follows_count(obj):
    author_follows_count = FollowAuthor.objects.filter(user=obj).count()
    return author_follows_count


# 生成每个话题的点赞数
@register.simple_tag
def get_topic_likes_count(obj):
    topic_likes_count = LikeTopic.objects.filter(topic=obj).count()
    return topic_likes_count

# 生成用户对某个话题的点赞状态
@register.simple_tag(takes_context=True)
def get_user_liketopic_status(context,obj):
    user = context['user']
    # 如果用户未登录，返回空字符串
    if not user.is_authenticated:
        return ''
    user_like_status = LikeTopic.objects.filter(topic=obj,user=user).exists()
    # 如果用户有点赞记录，则返回激活状态
    if user_like_status:
        return 'active'
    # 如果没有该用户的点赞记录，则返回空字符串
    else:
        return ''

# 生成每个话题的每个评论的点赞数
@register.simple_tag
def get_topiccomment_likes_count(obj):
    topiccomment_likes_count = LikeTopicComment.objects.filter(comment=obj).count()
    return topiccomment_likes_count

# 生成用户对某个话题的点赞状态
@register.simple_tag(takes_context=True)
def get_user_liketopiccomment_status(context,obj):
    user = context['user']
    # 如果用户未登录，返回空字符串
    if not user.is_authenticated:
        return ''
    user_like_status = LikeTopicComment.objects.filter(comment=obj,user=user).exists()
    # 如果用户有点赞记录，则返回激活状态
    if user_like_status:
        return 'active'
    # 如果没有该用户的点赞记录，则返回空字符串
    else:
        return ''

# 生成每个话题的评论数
@register.simple_tag
def get_topiccomments_count(obj):
    topiccomments_count = TopicComment.objects.filter(topic=obj).count()
    return topiccomments_count

# 生成某个评论的子评论个数
@register.simple_tag
def get_topiccomment_children_count(obj,root):
    topiccomment_children_count = TopicComment.objects.filter(topic=obj,root=root).count()
    return topiccomment_children_count

# 生成某个文选的文章数
@register.simple_tag
def get_anthology_articles_count(obj):
    articles_count = Article.objects.filter(anthology=obj).count()
    return articles_count

# 生成某个作者，最近发布的三篇文章
@register.simple_tag
def get_author_article_11(obj):
    article = Article.objects.filter(author=obj)[0]
    aricle_title = article.article_title
    return aricle_title
@register.simple_tag
def get_author_article_12(obj):
    article = Article.objects.filter(author=obj)[0]
    aricle_id = article.id
    return aricle_id

@register.simple_tag
def get_author_article_21(obj):
    article = Article.objects.filter(author=obj)[1]
    aricle_title = article.article_title
    return aricle_title
@register.simple_tag
def get_author_article_22(obj):
    article = Article.objects.filter(author=obj)[1]
    aricle_id = article.id
    return aricle_id

@register.simple_tag
def get_author_article_31(obj):
    article = Article.objects.filter(author=obj)[2]
    aricle_title = article.article_title
    return aricle_title
@register.simple_tag
def get_author_article_32(obj):
    article = Article.objects.filter(author=obj)[2]
    aricle_id = article.id
    return aricle_id


# 生成某个文选最近发布的四篇文章
@register.simple_tag
def get_anthology_article_11(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>0:
        article = articles[0]
        article_title = article.article_title
        return article_title
@register.simple_tag
def get_anthology_article_12(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>0:
        article = articles[0]
        article_id = article.id
        return article_id
@register.simple_tag
def get_anthology_article_13(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>0:
        article = articles[0]
        article_cover = article.article_cover
        return article_cover

@register.simple_tag
def get_anthology_article_21(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>1:
        article = articles[1]
        article_title = article.article_title
        return article_title
@register.simple_tag
def get_anthology_article_22(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>1:
        article = articles[1]
        article_id = article.id
        return article_id
@register.simple_tag
def get_anthology_article_23(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>1:
        article = articles[1]
        article_cover = article.article_cover
        return article_cover

@register.simple_tag
def get_anthology_article_31(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>2:
        article = articles[2]
        article_title = article.article_title
        return article_title
@register.simple_tag
def get_anthology_article_32(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>2:
        article = articles[2]
        article_id = article.id
        return article_id
@register.simple_tag
def get_anthology_article_33(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>2:
        article = articles[2]
        article_cover = article.article_cover
        return article_cover

@register.simple_tag
def get_anthology_article_41(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>3:
        article = articles[3]
        article_title = article.article_title
        return article_title
@register.simple_tag
def get_anthology_article_42(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>3:
        article = articles[3]
        article_id = article.id
        return article_id
@register.simple_tag
def get_anthology_article_43(obj):
    articles = Article.objects.filter(anthology=obj)
    if articles.count()>3:
        article = articles[3]
        article_cover = article.article_cover
        return article_cover