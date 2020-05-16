from django.shortcuts import get_object_or_404,render,redirect,render_to_response
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
# from django.urls import reverse
from django.core.paginator import Paginator# 分页功能
from .forms import ArticleReleaseForm,AnthologyReleaseForm,InformationForm,PortraitForm,AhthologyChangeForm,ArticleChangeForm
from article.models import Article,Anthology
from functions.models import FollowAuthor
from functions.models import CollectArticle,LikeArticle
from userprofile.models import Profile
from community.models import Topic

# 主页
# 判断是否为员工的权限的装饰器，只有是员工身份才能登陆这个界面
@login_required(login_url="/")
def personal_center_home(request):
    # 个人页面首页，显示最近发布的一篇文章、各个文选下的前四篇文章
    context = {}
    user = request.user
    # 找到这个人发布的最新的一篇文章
    # new_article = Article.objects.filter(author=user).first()
    # if new_article is not None:
    #     context['new_article'] = new_article
    # else:
    #     print("还未发布文章")
    # 先取出个人所有的文选
    anthologys = Anthology.objects.filter(author=user)
    
    context['anthologys'] = anthologys
    return render(request, 'pc_home.html',context)

# 文章发布
@login_required(login_url="/")
def article_release(request):
    articleform = ArticleReleaseForm()
    user = request.user
    articles = Article.objects.filter(author=user)
    anthologys = Anthology.objects.filter(author=user)
    context = {}
    context['articleform'] = articleform
    context['articles'] = articles
    context['anthologys'] = anthologys
    return render(request, 'pc_article_release.html',context)

# 文章删除
@login_required(login_url="/")
def article_delete(request):
    article_id = request.GET.get('article_id')
    article = Article.objects.get(id=article_id)
    anthology_id = article.anthology.id
    article.delete()
    context = {}
    
    # 删除文章后应该跳转到该文章所在文选的详情页面
    context['jump_to'] = "/personal/anthology/" + str(anthology_id) + "/"
    context['operation'] = "文章删除成功"
    return render(request,'pc_sucess.html',context)

# 进入文章修改界面
@login_required(login_url="/")
def article_change(request):
    user = request.user
    article_id2 = request.GET.get('article_id2')
    article = Article.objects.get(id=article_id2)
    anthologys = Anthology.objects.filter(author=user)
    articleform = ArticleReleaseForm()
    context = {}
    context['article'] = article
    context['anthologys'] = anthologys
    context['articleform'] = articleform
    return render(request,'pc_article_change.html',context)

# 文章内容修改的处理函数
@login_required(login_url="/")
def article_change_handle(request):
    user = request.user
    articlechange_form = ArticleChangeForm(request.POST, request.FILES)
    if articlechange_form.is_valid():
        article_id = articlechange_form.cleaned_data['article_id']
        article_cover = articlechange_form.cleaned_data['article_cover']
        anthology_title = articlechange_form.cleaned_data['anthology']
        article_title = articlechange_form.cleaned_data['article_title']
        summary = articlechange_form.cleaned_data['summary']
        content = articlechange_form.cleaned_data['content']
        category = articlechange_form.cleaned_data['category']

        article = Article.objects.get(id=article_id)
        anthology = Anthology.objects.get(author=user,anthology_title=anthology_title)
        # 在更改页面，如果封面不选，就是一个none
        if article_cover is not None:
            article.article_cover = article_cover
        # 摘要部分有可能为空，为空就不填写了
        if summary != '':
            article.summary = summary
        article.anthology = anthology
        article.article_title = article_title
        article.content = content
        article.category = category
        article.save()
        context = {}
        context['jump_to'] = "/personal/anthology/" + str(anthology.id) + "/"
        context['operation'] = "文章修改成功"
        return render(request,'pc_sucess.html',context)

# 标签设置
@login_required(login_url="/")
def tag_release(request):
    user = request.user
    articles = Article.objects.filter(author=user)
    context = {}
    context['articles'] = articles
    return render(request, 'pc_tag.html',context)

# 文章创建
@require_POST
@login_required(login_url="/")
def article_create(request):
    user = request.user
    article_form = ArticleReleaseForm(request.POST, request.FILES)
    if article_form.is_valid():       
        article_title = article_form.cleaned_data['article_title']
        article_cover = article_form.cleaned_data['article_cover']
        content = article_form.cleaned_data['content']
        anthology_title = article_form.cleaned_data['anthology']
        summary = article_form.cleaned_data['summary']
        category = article_form.cleaned_data['category']

        # 这里有一个隐患，就是如果同一个作者，创建了两个相同名字的文选，那么这里的筛选就会出问题
        # 所以要在创建文选的那一个环节确认该作者创建的文选不能同名
        anthology = Anthology.objects.get(author=user,anthology_title=anthology_title)
        if anthology:
            article, created = Article.objects.get_or_create(
            author=user,
            article_title=article_title,
            article_cover=article_cover,
            content = content,
            anthology = anthology,
            summary = summary,
            category = category,
        )
        article.save()

        # 文章创建成功后应该跳转到所属文选的详情页面
        context = {}
        context['jump_to'] = "/personal/anthology/" + str(anthology.pk) + "/"
        context['operation'] = "文章创建成功"
        return render(request,'pc_sucess.html',context)


# 文选列表展示
@login_required(login_url="/")
def anthology_release(request): 
    user = request.user
    anthologys = Anthology.objects.filter(author=user).order_by('-created_time')
    context = {}
    # 对搜索结果分页
    paginator = Paginator(anthologys,12)
    page_num = request.GET.get('page',1)
    page_of_anthologys = paginator.get_page(page_num)
    #总页数
    num_pages = paginator.num_pages

    # 设定当前页左右显示页数
    around_count = 2
    # 获取当前页码、左侧页码、右侧页码
    current_page = page_of_anthologys.number

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


    context['page_of_anthologys'] = page_of_anthologys
    context['left_pages'] = left_pages
    context['current_page'] = current_page
    context['right_pages'] = right_pages
    context['left_has_more'] = left_has_more
    context['right_has_more'] = right_has_more
    context['num_pages'] = num_pages
    return render(request, 'pc_anthology.html',context)

# 文选创建 
@require_POST
@login_required(login_url="/")
def anthology_create(request):
    user = request.user
    anthology_form = AnthologyReleaseForm(request.POST, request.FILES)
    context = {}
    if anthology_form.is_valid():       
        anthology_title = anthology_form.cleaned_data['anthology_title']
        anthology_cover = anthology_form.cleaned_data['anthology_cover']
        anthology_describe = anthology_form.cleaned_data['anthology_describe']
        if anthology_title != '':
            # 这里为了避免同一个作者创建两个拥有相同名字的文选，必须做一个判断
            anthology_test = Anthology.objects.filter(author=user,anthology_title=anthology_title)
            if anthology_test.exists():
                context['jump_to'] = "/personal/anthology_release/"
                context['operation'] = "文选《" + anthology_title + "》已存在"
                return render(request,'pc_sucess.html',context)
            else:

                anthology, created = Anthology.objects.get_or_create(
                author=user,
                anthology_title=anthology_title,
                anthology_cover=anthology_cover,
                anthology_describe=anthology_describe
            )
                anthology.save()
                # 文选创建成功后，应该是跳转到文选的集合列表页面
                
                context['jump_to'] = "/personal/anthology_release/"
                context['operation'] = "文选创建成功"
                return render(request,'pc_sucess.html',context)

# 文选详情页
@login_required(login_url="/")
def anthology_article(request,id):
    user = request.user
    # anthologys = Anthology.objects.filter(author=user)
    anthology = Anthology.objects.get(id=id)
    articles = Article.objects.filter(author=user,anthology=anthology)
    # articleform = ArticleReleaseForm()

    # 分页
    paginator = Paginator(articles,10)
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

    context = {}
    context['page_of_articles'] = page_of_articles
    context['left_pages'] = left_pages
    context['current_page'] = current_page
    context['right_pages'] = right_pages
    context['left_has_more'] = left_has_more
    context['right_has_more'] = right_has_more
    context['num_pages'] = num_pages

    
    # context['articles'] = articles
    context['count'] = articles.count()
    context['anthology'] = anthology
    # context['articleform'] = articleform
    # context['anthologys'] = anthologys
    return render(request,'pc_anthology_article.html',context)

# 文选删除,删除文选的同时也要把他关联的文章删除，文章关联的所有内容都删除
@login_required(login_url="/")
def anthology_delete(request):
    anthology_id = request.GET.get('anthology_id')
    anthology = Anthology.objects.get(id=anthology_id)
    anthology.delete()
    context = {}
    context['jump_to'] = "/personal/anthology_release/"
    context['operation'] = "文选删除成功"
    return render(request,'pc_sucess.html',context)

# 文选的修改展示
@login_required(login_url="/")
def anthology_change(request):
    anthology_id2 = request.GET.get('anthology_id2')
    anthology = Anthology.objects.get(id=anthology_id2)
    context = {}
    context['anthology'] = anthology
    return render(request,'pc_anthology_change.html',context)

# 文选内容修改的处理函数
@login_required(login_url="/")
def anthology_change_handle(request):
    anthologychange_form = AhthologyChangeForm(request.POST, request.FILES)
    if anthologychange_form.is_valid():
        anthology_id = anthologychange_form.cleaned_data['anthology_id']
        anthology = get_object_or_404(Anthology,id=anthology_id)

        anthology_cover = anthologychange_form.cleaned_data['anthology_cover']
        if anthology_cover is not None:
            anthology.anthology_cover = anthology_cover

        anthology_title = anthologychange_form.cleaned_data['anthology_title']
        anthology_describe = anthologychange_form.cleaned_data['anthology_describe']
        anthology.anthology_title = anthology_title
        anthology.anthology_describe = anthology_describe
        anthology.save()

        context = {}
        context['jump_to'] = "/personal/anthology_release/"
        context['operation'] = "文选修改成功"
        return render(request,'pc_sucess.html',context)


# 用户信息的公开展示
# 首先能公开的信息有：文选、文章、关注、粉丝
def public_author_message(request,id):
    context = {}
    # 根据传进来的作者id找到这个人
    author =  User.objects.get(id=id)
    # 然后根据这个作者找到他创作了多少文选
    anthologys = Anthology.objects.filter(author=author)
    #根据作者找到他有多少文章
    articles = Article.objects.filter(author=author)
    # 根据这个作者找到谁关注了他，就是粉丝列表
    fans = FollowAuthor.objects.filter(author=author)
    # 根据这个作者找到他关注了谁,就是关注列表
    follows = FollowAuthor.objects.filter(user=author)

    collect_count = 0
    for article in articles:
        collect_count += CollectArticle.objects.filter(article=article).count()

    like_count = 0
    for article in articles:
        like_count += LikeArticle.objects.filter(article=article).count() 

    context['collect_count'] = collect_count
    context['like_count'] = like_count
    context['author'] = author
    context['anthologys'] = anthologys
    context['articles'] = articles
    context['fans'] = fans
    context['follows'] = follows

    return render(request,'pc_p_author.html',context)


# 关于对个人信息公开页的展示，要展示的有文选、关注、粉丝，点击文选之后才回出现各个文选下方的文章
# 对于个人头像点击之后，进来看到的是文选的页面
def public_author_anthologys(request,id):
    context = {}
    # 根据传进来的作者id找到这个人
    author =  User.objects.get(id=id)
    # 然后根据这个作者找到他创作了多少文选
    anthologys = Anthology.objects.filter(author=author)
    #根据作者找到他有多少文章
    articles = Article.objects.filter(author=author)
    collect_count = 0
    for article in articles:
        collect_count += CollectArticle.objects.filter(article=article).count()

    like_count = 0
    for article in articles:
        like_count += LikeArticle.objects.filter(article=article).count() 

    # 对挑选出的分类文章进行分页
    paginator = Paginator(anthologys,40)
    page_num = request.GET.get('page',1)
    page_of_anthologys = paginator.get_page(page_num)
    #总页数
    num_pages = paginator.num_pages

    # 设定当前页左右显示页数
    around_count = 2
    # 获取当前页码、左侧页码、右侧页码
    current_page = page_of_anthologys.number

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


    # 一共分了多少页
    context['page_of_anthologys'] = page_of_anthologys
    # context['page_range'] = paginator.page_range
    context['left_pages'] = left_pages
    context['current_page'] = current_page
    context['right_pages'] = right_pages
    context['left_has_more'] = left_has_more
    context['right_has_more'] = right_has_more
    context['num_pages'] = num_pages


    context['collect_count'] = collect_count
    context['like_count'] = like_count
    context['author'] = author

 

    return render(request,'pc_p_anthology.html',context)

# 点击文选之后进入文选的详细页面
def public_author_articles(request,id):
    context = {}
    # 根据传进来的文选id找到相应的文选
    anthology = Anthology.objects.get(id=id)
    # 根据文选，找到相对应的作者
    author = anthology.author
    # 根据文选，找到到下面所属的所有文章
    articles = Article.objects.filter(anthology=anthology)
    collect_count = 0
    for article in articles:
        collect_count += CollectArticle.objects.filter(article=article).count()

    like_count = 0
    for article in articles:
        like_count += LikeArticle.objects.filter(article=article).count() 


    # 对挑选出的分类文章进行分页
    paginator = Paginator(articles,40)
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


    # 一共分了多少页
    context['page_of_articles'] = page_of_articles
    # context['page_range'] = paginator.page_range
    context['left_pages'] = left_pages
    context['current_page'] = current_page
    context['right_pages'] = right_pages
    context['left_has_more'] = left_has_more
    context['right_has_more'] = right_has_more
    context['num_pages'] = num_pages
    context['anthology'] = anthology
    context['author'] = author
    # 这里的点赞数和收藏数，就是这个文选包含文章的点赞和收藏数量综合
    context['collect_count'] = collect_count
    context['like_count'] = like_count
    return render(request,'pc_p_article.html',context)


# 点击关注按钮后显示关注的人
def public_author_follows(request,id):
    context = {}
    # 根据传进来的作者id找到这个人
    author =  User.objects.get(id=id)

    #根据作者找到他有多少文章
    articles = Article.objects.filter(author=author)
    # 根据这个作者找到谁关注了他，就是粉丝列表
    # fans = FollowAuthor.objects.filter(author=author)
    # 根据这个作者找到他关注了谁,就是关注列表
    follows = FollowAuthor.objects.filter(user=author)

    collect_count = 0
    for article in articles:
        collect_count += CollectArticle.objects.filter(article=article).count()

    like_count = 0
    for article in articles:
        like_count += LikeArticle.objects.filter(article=article).count() 

    # 对挑选出的分类文章进行分页
    paginator = Paginator(follows,20)
    page_num = request.GET.get('page',1)
    page_of_follows = paginator.get_page(page_num)
    #总页数
    num_pages = paginator.num_pages

    # 设定当前页左右显示页数
    around_count = 2
    # 获取当前页码、左侧页码、右侧页码
    current_page = page_of_follows.number

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

    # 一共分了多少页
    context['page_of_follows'] = page_of_follows
    # context['page_range'] = paginator.page_range
    context['left_pages'] = left_pages
    context['current_page'] = current_page
    context['right_pages'] = right_pages
    context['left_has_more'] = left_has_more
    context['right_has_more'] = right_has_more
    context['num_pages'] = num_pages
    context['collect_count'] = collect_count
    context['like_count'] = like_count
    
    context['author'] = author
    context['articles'] = articles
    context['follow_fan'] = 'follow'

    return render(request,'pc_p_author.html',context)

# 点击粉丝按钮后显示粉丝
def public_author_fans(request,id):
    context = {}
    # 根据传进来的作者id找到这个人
    author =  User.objects.get(id=id)

    #根据作者找到他有多少文章
    articles = Article.objects.filter(author=author)
    # 根据这个作者找到谁关注了他，就是粉丝列表
    # fans = FollowAuthor.objects.filter(author=author)
    # 根据这个作者找到他关注了谁,就是关注列表
    follows = FollowAuthor.objects.filter(author=author)

    collect_count = 0
    for article in articles:
        collect_count += CollectArticle.objects.filter(article=article).count()

    like_count = 0
    for article in articles:
        like_count += LikeArticle.objects.filter(article=article).count() 

    # 对挑选出的分类文章进行分页
    paginator = Paginator(follows,20)
    page_num = request.GET.get('page',1)
    page_of_follows = paginator.get_page(page_num)
    #总页数
    num_pages = paginator.num_pages

    # 设定当前页左右显示页数
    around_count = 2
    # 获取当前页码、左侧页码、右侧页码
    current_page = page_of_follows.number

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

    # 一共分了多少页
    context['page_of_follows'] = page_of_follows
    # context['page_range'] = paginator.page_range
    context['left_pages'] = left_pages
    context['current_page'] = current_page
    context['right_pages'] = right_pages
    context['left_has_more'] = left_has_more
    context['right_has_more'] = right_has_more
    context['num_pages'] = num_pages
    context['collect_count'] = collect_count
    context['like_count'] = like_count
    
    context['author'] = author
    context['articles'] = articles
    context['follow_fan'] = 'fan'

    return render(request,'pc_p_author.html',context)

@login_required(login_url="/")
def author_follow(request):
    user = request.user
    author_id = request.POST.get('author_id')
    author = User.objects.get(pk=author_id)

    # 在表中查找该用户是否关注了这个作者
    follow_author = FollowAuthor.objects.filter(author=author, user=user)
    # 如果记录存在，说明关注了，现在执行的是取消关注的操作
    if follow_author.exists():
        follow_author.delete()
    #如果不存在这条记录，说明还没有关注，现在执行的是关注操作
    else:
        follow_author, created = FollowAuthor.objects.get_or_create(author=author, user=user)

    return redirect("personal_center:public_author_message", id=author_id)


#信息中心的界面
@login_required(login_url="/")
def message_center(request):
    user = request.user
    context = {}
    context['user'] = user
    return render(request,'pc_chat.html',context)

#个人资料的展示与修改
@login_required(login_url="/")
def information(request):
    user = request.user
    context = {}
    context['user'] = user
    return render(request,'pc_information.html',context)

# 只能在登陆状态下修改个人资料
@login_required(login_url="/")
def information_change(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    # context = {}
    information_form = InformationForm(request.POST, request.FILES)
    # print(information_form)
    if information_form.is_valid():
        # print("表单合格了")
        
        # portrait = information_form.cleaned_data['portrait']
        email = information_form.cleaned_data['email']
        autograph = information_form.cleaned_data['autograph']
        birthday = information_form.cleaned_data['birthday']
        sex = information_form.cleaned_data['sex']
        telephone = information_form.cleaned_data['telephone']
        city = information_form.cleaned_data['city']

        # 因为邮箱在注册的时候就填好了，如果用户修改邮箱的时候为空，不能更改邮箱
        if email != '':
            # print("邮箱验证合格了")
            user.email = email
            user.save()
        if autograph != '':
            # print("签名验证合格了")
            profile.autograph = autograph
        profile.sex = sex
        profile.telephone = telephone
        profile.city = city
        profile.birthday = birthday

        profile.save()


        return redirect("personal_center:information")

# 个人资料的头像修改
@login_required(login_url="/")
def portrait_change(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    portrait = request.FILES['portrait']
    if portrait != '':
    # portrait_form = PortraitForm(request.POST, request.FILES)
    # print(portrait_form)
    # if portrait_form.is_valid():
    #     print("验证通过")
    #     portrait = portrait_form.cleaned_data['portrait']
        profile.portrait = portrait
        profile.save()
        return redirect("personal_center:information")

# 用户发布的帖子展示,帖子是公共区域，暂时不允许删除
@login_required(login_url="/")
def topic_show(request):
    user = request.user
    topics = Topic.objects.filter(author=user)
    context = {}
    

    # 对搜索结果分页
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


    context['page_of_topics'] = page_of_topics
    # context['page_range'] = paginator.page_range
    context['left_pages'] = left_pages
    context['current_page'] = current_page
    context['right_pages'] = right_pages
    context['left_has_more'] = left_has_more
    context['right_has_more'] = right_has_more
    context['num_pages'] = num_pages

    # context['topics'] = topics
    return render(request,'pc_topic.html',context)


# 该用户关注的人
@login_required(login_url="/")
def follow_show(request):
    user = request.user
    follows = FollowAuthor.objects.filter(user=user)
    context = {}

    # 对搜索结果分页
    paginator = Paginator(follows,10)
    page_num = request.GET.get('page',1)
    page_of_follows = paginator.get_page(page_num)
    #总页数
    num_pages = paginator.num_pages

    # 设定当前页左右显示页数
    around_count = 2
    # 获取当前页码、左侧页码、右侧页码
    current_page = page_of_follows.number

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


    context['page_of_follows'] = page_of_follows
    # context['page_range'] = paginator.page_range
    context['left_pages'] = left_pages
    context['current_page'] = current_page
    context['right_pages'] = right_pages
    context['left_has_more'] = left_has_more
    context['right_has_more'] = right_has_more
    context['num_pages'] = num_pages
    context['fans_follow'] = 'follow'
    # context['topics'] = topics
    return render(request,'pc_follow.html',context)

# 该用户的粉丝
@login_required(login_url="/")
def fans_show(request):
    user = request.user
    follows = FollowAuthor.objects.filter(author=user)
    context = {}

    # 对搜索结果分页
    paginator = Paginator(follows,10)
    page_num = request.GET.get('page',1)
    page_of_follows = paginator.get_page(page_num)
    #总页数
    num_pages = paginator.num_pages

    # 设定当前页左右显示页数
    around_count = 2
    # 获取当前页码、左侧页码、右侧页码
    current_page = page_of_follows.number

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


    context['page_of_follows'] = page_of_follows
    # context['page_range'] = paginator.page_range
    context['left_pages'] = left_pages
    context['current_page'] = current_page
    context['right_pages'] = right_pages
    context['left_has_more'] = left_has_more
    context['right_has_more'] = right_has_more
    context['num_pages'] = num_pages
    context['fans_follow'] = 'fans'

    # context['topics'] = topics
    return render(request,'pc_follow.html',context)