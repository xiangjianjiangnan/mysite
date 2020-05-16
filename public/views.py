from django.shortcuts import render
from article.models import Article,Anthology
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from cms.models import Recommend
from community.models import Topic

def home(request):
    context = {}
    # 首页轮播图,取最近的一条轮播图设置，得到主体id的列表字段
    recommend_record11 = Recommend.objects.filter(recommend_type=11).first()
    if recommend_record11 is not None:
        id_list11 = recommend_record11.recommend_id.split()
        id_list11 = [ int(x) for x in id_list11 ]
        recommend11 = Article.objects.filter(id__in=id_list11)
        context['recommend11'] = recommend11
    else:
        print("找不到相关推荐")

    # 首页重点文章推荐，6篇
    recommend_record12 = Recommend.objects.filter(recommend_type=12).first()
    if recommend_record11 is not None:
        id_list12 = recommend_record12.recommend_id.split()
        id_list12 = [ int(x) for x in id_list12 ]
        recommend12 = Article.objects.filter(id__in=id_list12)
        context['recommend12'] = recommend12
    else:
        print("找不到相关推荐")

    # 首页文选推荐，4篇
    recommend_record13 = Recommend.objects.filter(recommend_type=13).first()
    if recommend_record13 is not None:
        id_list13 = recommend_record13.recommend_id.split()
        id_list13 = [ int(x) for x in id_list13 ]
        recommend13 = Anthology.objects.filter(id__in=id_list13)
        context['recommend13'] = recommend13
    else:
        print("找不到相关推荐")

    # 首页文章推荐，8篇
    recommend_record14 = Recommend.objects.filter(recommend_type=14).first()
    if recommend_record14 is not None:
        id_list14 = recommend_record14.recommend_id.split()
        id_list14 = [ int(x) for x in id_list14 ]
        recommend14 = Article.objects.filter(id__in=id_list14)
        context['recommend14'] = recommend14
    else:
        print("找不到相关推荐")

    # 首页作者推荐，5个
    recommend_record15 = Recommend.objects.filter(recommend_type=15).first()
    if recommend_record15 is not None:
        id_list15 = recommend_record15.recommend_id.split()
        id_list15 = [ int(x) for x in id_list15 ]
        recommend15 = User.objects.filter(id__in=id_list15)
        context['recommend15'] = recommend15
    else:
        print("找不到相关推荐")

    # 首页教程推荐，5个
    recommend_record16 = Recommend.objects.filter(recommend_type=16).first()
    if recommend_record16 is not None:
        id_list16 = recommend_record16.recommend_id.split()
        id_list16 = [ int(x) for x in id_list16 ]
        recommend16 = Anthology.objects.filter(id__in=id_list16)
        context['recommend16'] = recommend16
    else:
        print("找不到相关推荐")

    # 推荐的资讯,原则是首页展示十条最新的资讯
    news = Article.objects.filter(category='资讯')[0:10]
    # 文章更新列表，原则是提取不是资讯的最新15条文章
    articles_update_list = ['数据思维','数据获取','数据处理','数据分析','数据可视化','数据报告','人工智能','面试题'] 
    articles_update = Article.objects.filter(category__in=articles_update_list)[0:15]
    # 评论的更新列表
    topics_update = Topic.objects.all()[0:15]

    context['news'] = news
    context['articles_update'] = articles_update
    context['topics_update'] = topics_update
    return render(request, 'home.html',context)


def news(request,category):
    article = Article.objects.get(id=1)
    context = {}
    context['article'] = article
    context['category'] = category
    return render(request, 'news.html',context)

def category(request,category):

    if request.GET.get('order') == 'read_num': 
        articles = Article.objects.filter(category=category).order_by('-read_num')
        order = 'read_num'
    elif request.GET.get('order') == 'reader_num':
        articles = Article.objects.filter(category=category).order_by('-reader_num')
        order = 'reader_num'
    elif request.GET.get('order') == 'like_num':
        articles = Article.objects.filter(category=category).order_by('-like_num')
        order = 'like_num'
    elif request.GET.get('order') == 'collect_num':
        articles = Article.objects.filter(category=category).order_by('-collect_num')
        order = 'collect_num'
    elif request.GET.get('order') == 'comment_num':
        articles = Article.objects.filter(category=category).order_by('-comment_num')
        order = 'comment_num'
    else:
        articles = Article.objects.filter(category=category)
        order = 'created_time'
    
    # 对挑选出的分类文章进行分页
    paginator = Paginator(articles,20)
    page_num = request.GET.get('page',1)
    page_of_articles = paginator.get_page(page_num)
    #总页数
    num_pages = paginator.num_pages

    # 设定当前页左右显示页数
    around_count = 2
    # 获取当前页码、左侧页码、右侧页码
    current_page = page_of_articles.number

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

    hot_articles = Article.objects.filter(category=category).order_by('-read_num')[0:10]
    context = {}
    # 一共分了多少页
    context['page_of_articles'] = page_of_articles
    # context['page_range'] = paginator.page_range
    context['left_pages'] = left_pages
    context['current_page'] = current_page
    context['right_pages'] = right_pages
    context['left_has_more'] = left_has_more
    context['right_has_more'] = right_has_more
    context['num_pages'] = num_pages
    context['order'] = order
    context['category'] = category
    context['hot_articles'] = hot_articles
    return render(request,'class.html',context)

def service_government(request):
    return render(request,'service_government.html')

def service_media(request):
    return render(request,'service_media.html')

def service_intelligence(request):
    return render(request,'service_intelligence.html')

def service_company(request):
    return render(request,'service_company.html')