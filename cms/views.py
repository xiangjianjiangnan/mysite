from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .forms import RecommendForm
from .models import Recommend
from article.models import Article,Anthology

# 主页
# 判断是否为员工的权限的装饰器，只有是员工身份才能登陆这个界面
@staff_member_required(login_url='/')
def cms(request):
    context = {}
    # 首页轮播图,取最近的一条轮播图设置，得到主体id的列表字段
    recommend_record11 = Recommend.objects.filter(recommend_type=11).first()
    if recommend_record11 is not None:
        id_list11 = recommend_record11.recommend_id.split()
        id_list11 = [ int(x) for x in id_list11 ]
        recommend11 = Article.objects.filter(id__in=id_list11)
        context['recommend_record11'] = recommend_record11
        context['recommend11'] = recommend11
    else:
        print("找不到相关推荐")

    # 首页重点文章推荐，6篇
    recommend_record12 = Recommend.objects.filter(recommend_type=12).first()
    if recommend_record12 is not None:
        id_list12 = recommend_record12.recommend_id.split()
        id_list12 = [ int(x) for x in id_list12 ]
        recommend12 = Article.objects.filter(id__in=id_list12)
        context['recommend_record12'] = recommend_record12
        context['recommend12'] = recommend12
    else:
        print("找不到相关推荐")

    # 首页文选推荐，4篇
    recommend_record13 = Recommend.objects.filter(recommend_type=13).first()
    if recommend_record13 is not None:
        id_list13 = recommend_record13.recommend_id.split()
        id_list13 = [ int(x) for x in id_list13 ]
        recommend13 = Anthology.objects.filter(id__in=id_list13)
        context['recommend_record13'] = recommend_record13
        context['recommend13'] = recommend13
    else:
        print("找不到相关推荐")

    # 首页文章推荐，8篇
    recommend_record14 = Recommend.objects.filter(recommend_type=14).first()
    if recommend_record14 is not None:
        id_list14 = recommend_record14.recommend_id.split()
        id_list14 = [ int(x) for x in id_list14 ]
        recommend14 = Article.objects.filter(id__in=id_list14)
        context['recommend_record14'] = recommend_record14
        context['recommend14'] = recommend14
    else:
        print("找不到相关推荐")

    # 首页作者推荐，5个
    recommend_record15 = Recommend.objects.filter(recommend_type=15).first()
    if recommend_record15 is not None:
        id_list15 = recommend_record15.recommend_id.split()
        id_list15 = [ int(x) for x in id_list15 ]
        recommend15 = User.objects.filter(id__in=id_list15)
        context['recommend_record15'] = recommend_record15
        context['recommend15'] = recommend15
    else:
        print("找不到相关推荐")

    # 首页教程推荐，5个
    recommend_record16 = Recommend.objects.filter(recommend_type=16).first()
    if recommend_record16 is not None:
        id_list16 = recommend_record16.recommend_id.split()
        id_list16 = [ int(x) for x in id_list16 ]
        recommend16 = Anthology.objects.filter(id__in=id_list16)
        context['recommend_record16'] = recommend_record16
        context['recommend16'] = recommend16
    else:
        print("找不到相关推荐")

    return render(request, 'cms.html',context)
# 推荐页面展示
@staff_member_required(login_url='/')
def recommend(request):
    return render(request, 'cms_recommend.html')

# 推荐上传
@staff_member_required(login_url='/')
@require_POST
def recommend_post(request):
    # recommend_form = RecommendForm(request.POST)
    # context = {}
    # if recommend_form.is_valid():
    #     print("进来了")
    #     recommend_type = recommend_form.cleaned_data['recommend_type']
    #     recommend_id = recommend_form.cleaned_data['recommend_id']
    #     recommend_text = recommend_form.cleaned_data['recommend_text']
    context = {}
    recommend_type = request.POST.get('recommend_type')
    recommend_id = request.POST.get('recommend_id')
    recommend_text = request.POST.get('recommend_text')
    print(type(recommend_type))
    print(type(recommend_id))
    print(type(recommend_text))
    recommend = Recommend()
    # 接下来是判断设置的该推荐主体是否存在，如果不存在则返回这个推荐界面
    recommend_list1 = [11,12,14]#主体是文章
    recommend_list2 = [13,16,17]#主体是文选
    recommend_list3 = [15]#主体是作者

    # 将推荐列表有字符串变成列表
    id_list = recommend_id.split()
    # 将列表中的字符串转换为数字类型
    id_list = [ int(x) for x in id_list ]
    # 建立一个空的列表，用来存储验证不过的推荐主体
    not_list = []
    if int(recommend_type) in recommend_list1:
        # 如果推荐主体是文章，则要判断该文章是否存在
        
        for i in id_list:
            article = Article.objects.get(id=i)
            if article:
                pass
            else:
                not_list.append(i)
        if not_list:
            # 如果存储不存在文章的列表不为空，则说明有不存在的文章
            context['jump_to'] = "/cms/recommend/"
            context['operation'] = "下列推荐内容不存在：" + "、".join(not_list)
            return render(request,'cms_sucess.html',context)
        else:
            # 如果列表为空，则说明推荐的主体都存在
            recommend.recommend_type = int(recommend_type)
            recommend.recommend_id = recommend_id
            recommend.recommend_text = recommend_text
            recommend.save()
            # 设置完推荐后跳转到后台主页
            context['jump_to'] = "/cms/"
            context['operation'] = "设置推荐成功"
            return render(request,'cms_sucess.html',context)
    elif int(recommend_type) in recommend_list2:
        # 如果推荐主体是文选
        for i in id_list:
            anthology = Anthology.objects.get(id=i)
            if anthology:
                pass
            else:
                not_list.append(i)
        if not_list:
            # 如果存储列表不为空，则说明有不存在的文选
            context['jump_to'] = "/cms/recommend/"
            context['operation'] = "下列推荐内容不存在：" + "、".join(not_list)
            return render(request,'cms_sucess.html',context)
        else:
            # 如果列表为空，则说明推荐的主体都存在
            recommend.recommend_type = int(recommend_type)
            recommend.recommend_id = recommend_id
            recommend.recommend_text = recommend_text
            recommend.save()
            # 设置完推荐后跳转到后台主页
            context['jump_to'] = "/cms/"
            context['operation'] = "设置推荐成功"
            return render(request,'cms_sucess.html',context)
    elif int(recommend_type) in recommend_list3:
        # 如果推荐主体是用户
        for i in id_list:
            user = User.objects.get(id=i)
            if user:
                pass
            else:
                not_list.append(i)
        if not_list:
            # 如果存储列表不为空，则说明有不存在的用户
            context['jump_to'] = "/cms/recommend/"
            context['operation'] = "下列推荐内容不存在：" + "、".join(not_list)
            return render(request,'cms_sucess.html',context)
        else:
            # 如果列表为空，则说明推荐的主体都存在
            recommend.recommend_type = int(recommend_type)
            recommend.recommend_id = recommend_id
            recommend.recommend_text = recommend_text
            recommend.save()
            # 设置完推荐后跳转到后台主页
            context['jump_to'] = "/cms/"
            context['operation'] = "设置推荐成功"
            return render(request,'cms_sucess.html',context)


# 轮播图上传
# @staff_member_required(login_url='home')
# @require_POST
# def banner_create(request):
#     bannerform = BannerForm()
#     if bannerform.is_valid():
#         banner_title = bannerform.cleaned_data['banner_title']
#         banner_class = bannerform.cleaned_data['banner_class']
#         article_id = bannerform.cleaned_data['article_id']
#         banner_img1 = bannerform.cleaned_data['banner_img1']
#         banner_img2 = bannerform.cleaned_data['banner_img2']
#         article = Article.objects.filter(id=article_id)
#         if article:
#             banner, created = Banner.objects.get_or_create(
#             banner_title=banner_title,
#             banner_class=banner_class,
#             banner_img1=banner_img1,
#             banner_img2=banner_img2,
#             article=article
#         )
#             banner.save()
#             return render(request, 'banner_sucess.html')
#         else:
#             return render(request, 'banner_failed.html')



    # context = {}
    # context['banner'] = banner
    # return render(request, 'cms_banner.html', context)

# 文章发布
# @staff_member_required(login_url='home')
# def article_release(request):
#     articleform = ArticleReleaseForm()
#     user = request.user
#     articles = Article.objects.filter(author=user)
#     context = {}
#     context['articleform'] = articleform
#     context['articles'] = articles
#     return render(request, 'cms_article_release.html',context)


# 标签设置
# @staff_member_required(login_url='home')
# def tag_release(request):
#     user = request.user
#     articles = Article.objects.filter(author=user)
#     context = {}
#     context['articles'] = articles

#     return render(request, 'cms_tag.html',context)

# 文选设置
# @staff_member_required(login_url='home')
# def anthology_release(request): 
#     user = request.user
#     anthologys = Anthology.objects.filter(author=user)
#     context = {}
#     context['anthologys'] = anthologys
#     return render(request, 'cms_anthology.html',context)
    
# @require_POST
# def anthology_create(request):

#     anthology_form = AnthologyReleaseForm(request.POST, request.FILES)
#     print('表单接收成功')
#     if anthology_form.is_valid():
#         print('表单验证成功')
#         user = request.user
#         anthology_title = anthology_form.cleaned_data['anthology_title']
#         anthology_cover = anthology_form.cleaned_data['anthology_cover']
#         anthology_describe = anthology_form.cleaned_data['anthology_describe']
#         if anthology_title != '':
#             anthology, created = Anthology.objects.get_or_create(
#             author=user,
#             anthology_title=anthology_title,
#             anthology_cover=anthology_cover,
#             anthology_describe=anthology_describe
#         )
#         anthology.save()
#         anthologys = Anthology.objects.filter(author=user)
#         context = {}
#         context['anthologys'] = anthologys
#         return render(request, 'cms_anthology.html',context)
