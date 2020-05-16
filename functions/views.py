from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import ArticleCommentForm
from .models import ArticleComment,LikeArticle,LikeComment,CollectArticle,FollowAuthor
from article.models import Article






# 处理文章评论
@login_required(login_url="home")
def article_comment(request):
    user = request.user
    articlecomment_form = ArticleCommentForm(request.POST)
    data = {}
    if articlecomment_form.is_valid():
        article_id = articlecomment_form.cleaned_data['article_id']
        article = Article.objects.get(pk=article_id)
        reply_comment_id = articlecomment_form.cleaned_data['reply_comment_id']
        articlecomment = ArticleComment()
        # 现在判断传入的这个数值是不是0，若是0，那它就是最顶级的评论，它的父级评论、根评论、回复人都是空的
        if reply_comment_id == 0:
            articlecomment.parent = None
            articlecomment.root = None
            articlecomment.reply_to = None
        # 如果现在传入的评论id不是0，那就看看根据这个id是不是能找到相应的评论
        #如果评论存在的话，那这个评论就是当前评论的父级评论，它的user就是被回复人，这条评论的根评论也是当前评论的根评论
        elif ArticleComment.objects.filter(pk=reply_comment_id).exists():
            articlecomment.parent = ArticleComment.objects.get(pk=reply_comment_id)
            # 如果根评论存在就是根评论，如果根评论不存在，那么父级评论就是他的根评论
            if articlecomment.parent.root:
                articlecomment.root = articlecomment.parent.root
            else:
                articlecomment.root = articlecomment.parent
            articlecomment.reply_to = articlecomment.parent.user
        
        articlecomment.user = user
        articlecomment.text = articlecomment_form.cleaned_data['text']

        articlecomment.article = article
        if articlecomment.text != '':
            articlecomment.save()

            # 如果这条评论被保留后，要对该文章的所有评论进行计数，如果计数多余数据库中的数据，则更新时数据库
            comment_num = ArticleComment.objects.filter(article=article).count()
            if article.comment_num < comment_num:
                article.comment_num = comment_num
                article.save(update_fields=['comment_num'])
            


        data['status'] = 'SUCCESS'
        data['username'] = articlecomment.user.username
        data['portrait'] = str(articlecomment.user.profile.portrait)
        data['text'] = articlecomment.text
        data['comment_time'] = articlecomment.comment_time.strftime('%Y/%m/%d %H:%M:%S')
        data['reply_to'] = articlecomment.reply_to.username if not articlecomment.parent is None else ''
        data['pk'] = articlecomment.pk
        data['root_pk'] = articlecomment.root.pk if not articlecomment.root is None else ''
        data['message'] = '评论成功！'
    else:
        data['status'] = 'ERROR'
        data['message'] = '评论失败！'

    return JsonResponse(data)

# 点赞的逻辑：点赞本身就是创造一个点赞的记录
def article_like(request):
    user = request.user
    article_id = request.GET.get('article_id')
    is_active = request.GET.get('is_active')
    article = Article.objects.get(pk=article_id)
    data = {}
    # 处理数据,如果点赞图标处于未点赞状态，那么就创造一条点赞记录
    if is_active == 'false':
        # 正在执行点赞动作，从数据库中获取或者创造一条点赞记录
        like_article, created = LikeArticle.objects.get_or_create(article=article, user=user)
        data['status'] = 'SUCESS'
    
    else:
        # 点赞图标处于点赞状态，正在执行取消点赞动作,先获取这条点赞的记录
        like_article = LikeArticle.objects.filter(article=article, user=user)
        # 如果这条点赞记录存在，那么删除这条记录
        if like_article.exists():
            like_article.delete()
            data['status'] = 'SUCESS'
        else:
            data['status'] = 'ERROR'
    like_num = LikeArticle.objects.filter(article=article).count()
    if article.like_num != like_num:
        article.like_num = like_num
        article.save(update_fields=['like_num'])
    return JsonResponse(data)


# 对文章评论进行点赞
def articlecomment_like(request):
    user = request.user
    articlecomment_id = request.GET.get('articlecomment_id')
    is_active = request.GET.get('is_active')
    comment = ArticleComment.objects.get(pk=articlecomment_id)
    data = {}
    # 处理数据,如果点赞图标处于未点赞状态，那么就创造一条点赞记录
    if is_active == 'false':
        # 正在执行点赞动作，从数据库中获取或者创造一条点赞记录
        like_comment, created = LikeComment.objects.get_or_create(comment=comment, user=user)
        data['status'] = 'SUCESS'
    
    else:
        # 点赞图标处于点赞状态，正在执行取消点赞动作,先获取这条点赞的记录
        like_comment = LikeComment.objects.filter(comment=comment, user=user)
        # 如果这条点赞记录存在，那么删除这条记录
        if like_comment.exists():
            like_comment.delete()
            data['status'] = 'SUCESS'
        else:
            data['status'] = 'ERROR'
    data['articlecomment_id'] = articlecomment_id
    return JsonResponse(data)

# 对文章进行收藏
def article_collect(request):
    user = request.user
    article_id = request.GET.get('article_id')
    is_active = request.GET.get('is_active')
    article = Article.objects.get(pk=article_id)
    data = {}
    # 处理数据,如果点收藏标处于未收藏状态，那么就创造一条收藏记录
    if is_active == 'false':
        # 正在执行收藏动作，从数据库中获取或者创造一条收藏记录
        collect_article, created = CollectArticle.objects.get_or_create(article=article, user=user)
        data['status'] = 'SUCESS'
    
    else:
        # 收藏图标处于收藏状态，正在执行取消收藏动作,先获取这条收藏的记录
        collect_article = CollectArticle.objects.filter(article=article, user=user)
        # 如果这条收藏记录存在，那么删除这条记录
        if collect_article.exists():
            collect_article.delete()
            data['status'] = 'SUCESS'
        else:
            data['status'] = 'ERROR'
    collect_num = CollectArticle.objects.filter(article=article).count()
    if article.collect_num != collect_num:
        article.collect_num = collect_num
        article.save(update_fields=['collect_num'])
    return JsonResponse(data)

# 对作者进行关注:ajax方法
def author_follow(request):
    user = request.user
    author_id = request.GET.get('author_id')
    is_follow = request.GET.get('is_follow')
    author = User.objects.get(pk=author_id)
    data = {}
    # 处理数据,如果关注图标处于未关注状态，那么就创造一条关注记录
    if is_follow == '+ 关注':
        # 正在执行关注动作，从数据库中获取或者创造一条关注记录
        follow_author, created = FollowAuthor.objects.get_or_create(author=author, user=user)
        data['status'] = 'SUCESS'
    
    elif is_follow == '已关注':
        # 关注图标处于关注状态，正在执行取消关注动作,先获取这条关注的记录
        follow_author = FollowAuthor.objects.filter(author=author, user=user)
        # 如果这条点赞记录存在，那么删除这条记录
        if follow_author.exists():
            follow_author.delete()
            data['status'] = 'SUCESS'
        else:
            data['status'] = 'ERROR'
    return JsonResponse(data)




