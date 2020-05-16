from django.shortcuts import get_object_or_404,render,redirect,render_to_response
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q
from .models import Article,ReaderNum
from functions.models import ArticleComment

# def home(request):
# 	return render(request, 'home.html')

def article_detail(request,id):
	# 获取文章
	article = get_object_or_404(Article,id=id)
	# 每次打开文章的时候，如果用户处于登录状态，那么就获取或者创建一条阅读记录
	if request.user.is_authenticated:
		reader = request.user
		reader_num, created = ReaderNum.objects.get_or_create(article=article, reader=reader)
		# 这里有两种技术方法，一个是判断是否是新建的，但是这种很容易在后台出错的时候遗漏，这里采用第二种方法，直接对该文章的阅读记录进行一个计数，然后赋值
		reader_num = ReaderNum.objects.filter(article=article).count()
		# 对该文章的阅读记录进行计数，如果数据库中的阅读人数少于计数量，则更新
		if article.reader_num != reader_num:
			article.reader_num = reader_num
		
	# 无论用户是否登录，只要改文章打开，那么阅读数+1
	article.read_num += 1
	article.save(update_fields=['read_num','reader_num'])
	# 该作者最新发布的5篇文章
	latest_articles = Article.objects.filter(author=article.author)[0:5]
	# 获取文章的评论
	article_comments = ArticleComment.objects.filter(article=article, parent=None).order_by('-comment_time')
	# 对搜索结果分页
	paginator = Paginator(article_comments,20)
	page_num = request.GET.get('page',1)
	page_of_comments = paginator.get_page(page_num)
	#总页数
	num_pages = paginator.num_pages

	# 设定当前页左右显示页数
	around_count = 2
	# 获取当前页码、左侧页码、右侧页码
	current_page = page_of_comments.number

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
	hot_articles = Article.objects.all().order_by('-read_num')[0:10]
	context = {}
	# context['search_words'] = search_words
	# context['search_atticles_count'] = search_articles.count()
	context['page_of_comments'] = page_of_comments
	# context['page_range'] = paginator.page_range
	context['left_pages'] = left_pages
	context['current_page'] = current_page
	context['right_pages'] = right_pages
	context['left_has_more'] = left_has_more
	context['right_has_more'] = right_has_more
	context['num_pages'] = num_pages

	
	# context = {}
	context['article'] = article
	# context['article_comments'] = article_comments.order_by('-comment_time')
	context['latest_articles'] = latest_articles
	return render(request,'article.html',context)


def article(request):
	article = get_object_or_404(Article,id=1)
	context = {}
	context['article'] = article
	return render(request,'article.html',context)



def article_serach(request):
	# 获取搜索关键词，并去除首尾空格
	search_words = request.GET.get('search','').strip()
	# 如果有程序直接绕过前端输入了空字符串，那么就直接返回首页
	if len(search_words) == 0:
		return render(request,'home.html')
	else:
		condition = None
		for word in search_words.split(' '):
			if condition is None:
				condition = Q(article_title__icontains=word) | Q(content__icontains=word)
			else:
				condition = condition | Q (article_title__icontains=word) | Q(content__icontains=word)#  ~:非  $:并  |：或        
		search_articles = Article.objects.filter(condition).order_by('-created_time')
		# search_articles = Article.objects.filter(article_title__icontains=search_word)
		# 对搜索结果分页
		paginator = Paginator(search_articles,10)
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
		hot_articles = Article.objects.all().order_by('-read_num')[0:10]
		context = {}
		context['search_words'] = search_words
		context['search_atticles_count'] = search_articles.count()
		context['page_of_articles'] = page_of_articles
		# context['page_range'] = paginator.page_range
		context['left_pages'] = left_pages
		context['current_page'] = current_page
		context['right_pages'] = right_pages
		context['left_has_more'] = left_has_more
		context['right_has_more'] = right_has_more
		context['num_pages'] = num_pages
		context['hot_articles'] = hot_articles
		return render(request,'search.html',context)