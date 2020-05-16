from django.shortcuts import get_object_or_404,render,redirect,render_to_response
from .models import Topic,TopicComment,LikeTopic,LikeTopicComment
from .forms import TopicCreateForm,TopicCommentForm
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def community(request):
    topicform = TopicCreateForm()
    topics = Topic.objects.all()[:20]
    # 筛选出评论最多的十个话题
    # 首先根据TopicComment表中计算出每个话题的评论数,然后根据评论数进行排序，并取前十个
    hot_topics = Topic.objects.annotate(comment_count=Count("topiccomment__topic")).order_by('-comment_count')[0:10]
    
    context = {}
    context['hot_topics'] = hot_topics
    context['topicform'] = topicform
    context['topics'] = topics
    return render(request,'community_home.html',context)


def topic_create(request):
    user = request.user
    topicform = TopicCreateForm()
    # print(user.username)
    topic_form = TopicCreateForm(request.POST, request.FILES)
    if topic_form.is_valid():       
        topic_title = topic_form.cleaned_data['topic_title']
        content = topic_form.cleaned_data['content']
        category = topic_form.cleaned_data['category']
        # 创建或者获取这条话题，并保存
        topic, created = Topic.objects.get_or_create(author=user, topic_title=topic_title, content=content, category=category)
        topic.save()
        # 首先根据TopicComment表中计算出每个话题的评论数,然后根据评论数进行排序，并取前十个
        hot_topics = Topic.objects.annotate(comment_count=Count("topiccomment__topic")).order_by('-comment_count')[0:10]
        context = {}
        context['topic'] = topic
        context['topicform'] = topicform
        context['hot_topics'] = hot_topics
        return render(request, 'topic.html',context)


def topic_detail(request,id):
    topic = get_object_or_404(Topic,id=id)
    # 打开话题一次，就计算一个阅读数
    topic.read_num += 1
    topic.save()
    topicform = TopicCommentForm()
    topic_comments = TopicComment.objects.filter(topic=topic, parent=None)
    # 筛选出评论最多的十个话题
    # 首先根据TopicComment表中计算出每个话题的评论数,然后根据评论数进行排序，并取前十个
    hot_topics = Topic.objects.annotate(comment_count=Count("topiccomment__topic")).order_by('-comment_count')[0:10]

    context = {}
    context['topic'] = topic
    context['topicform'] = topicform
    context['topic_comments'] = topic_comments
    context['hot_topics'] = hot_topics
    return render(request,'topic.html',context)

def topic_comment(request):
    user = request.user
    topiccomment_form = TopicCommentForm(request.POST, request.FILES)
    topicform = TopicCommentForm()
    context = {}
    if topiccomment_form.is_valid():
        topic_id = topiccomment_form.cleaned_data['topic_id']
        reply_comment_id = topiccomment_form.cleaned_data['reply_comment_id']
        content = topiccomment_form.cleaned_data['content']

        topic = Topic.objects.get(pk=topic_id)
        topiccomment = TopicComment()
        # 现在判断传入的这个数值是不是0，若是0，那它就是最顶级的评论，它的父级评论、根评论、回复人都是空的
        if reply_comment_id == 0:
            topiccomment.parent = None
            topiccomment.root = None
            topiccomment.reply_to = None
        # 如果现在传入的评论id不是0，那就看看根据这个id是不是能找到相应的评论
        #如果评论存在的话，那这个评论就是当前评论的父级评论，它的user就是被回复人，这条评论的根评论也是当前评论的根评论
        elif TopicComment.objects.filter(pk=reply_comment_id).exists():
            topiccomment.parent = TopicComment.objects.get(pk=reply_comment_id)
            # 如果根评论存在就是根评论，如果根评论不存在，那么父级评论就是他的根评论
            if topiccomment.parent.root:
                topiccomment.root = topiccomment.parent.root
            else:
                topiccomment.root = topiccomment.parent
            topiccomment.reply_to = topiccomment.parent.user
        topiccomment.user = user
        topiccomment.comment = content
        topiccomment.topic = topic
        if topiccomment.comment != '':
            topiccomment.save()
        # 保存之后跳转到话题的详情页
        return redirect("community:topic_detail", id=topic_id)


def topic_comment_like(request):
    user = request.user
    topiccomment_id = request.GET.get('topiccomment_id')
    is_active = request.GET.get('is_active')
    topic_id = request.GET.get('topic_id')
    print(topiccomment_id)
    print(is_active)
    print(topic_id)
    
    data = {}
    # 如果返回的评论id为0，说明这是对原帖子的点赞
    if topiccomment_id == '0':
        topic = Topic.objects.get(pk=topic_id)
        if is_active == 'false':
            like_topic, created = LikeTopic.objects.get_or_create(topic=topic, user=user, like_status='1')
            data['status'] = 'SUCESS'
        else:
            like_topic = LikeTopic.objects.filter(topic=topic, user=user, like_status='1')
            if like_topic.exists():
                like_topic.delete()
                data['status'] = 'SUCESS'
            else:
                data['status'] = 'ERROR'
    # 如果返回的评论id不为0，那么就是对评论进行的点赞
    else:
        topiccomment = TopicComment.objects.get(pk=topiccomment_id)
        # 处理数据,如果点赞图标处于未点赞状态，那么就创造一条点赞记录
        if is_active == 'false':
            # 正在执行点赞动作，从数据库中获取或者创造一条点赞记录
            like_topiccomment, created = LikeTopicComment.objects.get_or_create(comment=topiccomment, user=user, like_status='1')
            data['status'] = 'SUCESS'
        
        else:
            # 点赞图标处于点赞状态，正在执行取消点赞动作,先获取这条点赞的记录
            like_topiccomment = LikeTopicComment.objects.filter(comment=topiccomment, user=user, like_status='1')
            # 如果这条点赞记录存在，那么删除这条记录
            if like_topiccomment.exists():
                like_topiccomment.delete()
                data['status'] = 'SUCESS'
            else:
                data['status'] = 'ERROR'
        # data['articlecomment_id'] = articlecomment_id
    return JsonResponse(data)

       
# 对每个类型的话题进行分类展示，排序方法有按照你时间逆序、按照点击最多、按照评论最多
def topic_categry(request,category):
    topicform = TopicCreateForm()
    topics = Topic.objects.filter(category=category)

    if request.GET.get('order') == 'read_num': 
        topics = Topic.objects.filter(category=category).order_by('-read_num')
        order = 'read_num'
    elif request.GET.get('order') == 'comment_num':
        topics = Topic.objects.filter(category=category).annotate(comment_count=Count("topiccomment__topic")).order_by('-comment_count')
        order = 'comment_num'
    else:
        topics = Topic.objects.filter(category=category)
        order = 'created_time'

    # 对挑选出的分类文章进行分页
    paginator = Paginator(topics,10)
    page_num = request.GET.get('page',1)
    page_of_topics = paginator.get_page(page_num)
    #总页数
    num_pages = paginator.num_pages

    # 设定当前页左右显示页数
    around_count = 2
    # 获取当前页码、左侧页码、右侧页码
    current_page = page_of_topics.number

    left_has_more = False
    right_has_more = False
    if current_page <= around_count+2:
        left_pages = range(1,current_page)
    else:
        left_has_more = True
        left_pages = range(current_page-around_count,current_page)
    if current_page >= num_pages-around_count-1:
        right_pages = range(current_page+1,num_pages+1)
    else:
        right_has_more = True
        right_pages = range(current_page+1,current_page+around_count+1)

    hot_topics = Topic.objects.annotate(comment_count=Count("topiccomment__topic")).order_by('-comment_count')[0:10]
    context = {}
    # 一共分了多少页
    context['page_of_topics'] = page_of_topics
    # context['page_range'] = paginator.page_range
    context['left_pages'] = left_pages
    context['current_page'] = current_page
    context['right_pages'] = right_pages
    context['left_has_more'] = left_has_more
    context['right_has_more'] = right_has_more
    context['num_pages'] = num_pages
    context['order'] = order
    context['hot_topics'] = hot_topics
    context['category'] = category
    context['topicform'] = topicform

    return render(request,'community_category.html',context)

def topic_search(request):
    topicform = TopicCreateForm()
    # 获取搜索关键词，并去除首尾空格
    search_words = request.GET.get('topic_search','').strip()
    # 如果有程序直接绕过前端输入了空字符串，那么就直接返回首页
    if len(search_words) == 0:
        return render(request,'community_home.html')
    else:
        condition = None
        for word in search_words.split(' '):
            if condition is None:
                condition = Q(topic_title__icontains=word) | Q(content__icontains=word)
            else:
                condition = condition | Q (topic_title__icontains=word) | Q(content__icontains=word)#  ~:非  $:并  |：或        
        search_topics = Topic.objects.filter(condition).order_by('-created_time')
        # search_articles = Article.objects.filter(article_title__icontains=search_word)
        # 对搜索结果分页
        paginator = Paginator(search_topics,20)
        page_num = request.GET.get('page',1)
        page_of_topics = paginator.get_page(page_num)
        #总页数
        num_pages = paginator.num_pages

        # 设定当前页左右显示页数
        around_count = 2
        # 获取当前页码、左侧页码、右侧页码
        current_page = page_of_topics.number

        left_has_more = False
        right_has_more = False
        if current_page <= around_count+2:
            left_pages = range(1,current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count,current_page)
        if current_page >= num_pages-around_count-1:
            right_pages = range(current_page+1,num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1,current_page+around_count+1)

        hot_topics = Topic.objects.annotate(comment_count=Count("topiccomment__topic")).order_by('-comment_count')[0:10]

        context = {}
        context['search_words'] = search_words
        context['search_topics_count'] = search_topics.count()
        context['page_of_topics'] = page_of_topics
        # context['page_range'] = paginator.page_range
        context['left_pages'] = left_pages
        context['current_page'] = current_page
        context['right_pages'] = right_pages
        context['left_has_more'] = left_has_more
        context['right_has_more'] = right_has_more
        context['num_pages'] = num_pages
        context['hot_topics'] = hot_topics
        context['topicform'] = topicform
        return render(request,'community_search.html',context)






