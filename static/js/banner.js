
//对总的类进行参数的设置，相当于python中的__init__
function Banner(){
	this.bannerGroup = $("#banner_group");
	this.index = 1;
	this.bannerWidth = this.bannerGroup.outerWidth();
	this.pageControl = $("#page_control");
	this.leftArrow = $(".left_arrow");
	this.rightArrow = $(".right_arrow");
	this.bannerUL = $("#banner_ul");
	this.liList = this.bannerUL.children("li");
	this.bannerCount = this.liList.length;
	

}


//这个是鼠标进入轮播框轮播就停止，移出轮播框继续执行自动轮播
Banner.prototype.listenBannerHover = function(){
	var self =this;
	this.bannerGroup.hover(function(){
		//第一个函数是把鼠标移动到banner上会执行的函数
		clearInterval(self.timer);
	},function(){
		//第二个函数是把鼠标移出banner时会执行的函数
		self.loop();
	});
}; 



//轮播图切换的速度是1秒钟
Banner.prototype.animate = function(){
	var self =this;
	self.bannerUL.animate({"left":-self.bannerWidth*self.index},1000);
	if(self.index === 0){
		index = self.bannerCount-1;
	}else if(self.index === self.bannerCount+1){
		index = 0;
	}else{
		index = self.index-1;
	}
	self.pageControl.children("li").eq(index).addClass("active").siblings().removeClass("active");
};


//这个函数是轮播图的自动轮播功能，每4秒执行一次
Banner.prototype.loop = function(){
	var self = this;
	this.timer = setInterval(function(){
		if(self.index >= self.bannerCount+1){
			self.bannerUL.css({"left":-self.bannerWidth});
			self.index = 2;
		}else{
			self.index++;
		}		
		self.animate();
	},4000);
};

//这个函数是点击箭头进行轮播图的切换功能
Banner.prototype.listenArrowClick = function(){
	var self = this;
	self.leftArrow.click(function(){
		if(self.index === 0){
			self.bannerUL.css({"left":-self.bannerCount*self.bannerWidth});
			self.index = self.bannerCount - 1;
		}else{
			self.index--;
		}
		self.animate();
	});

	self.rightArrow.click(function(){
		if(self.index === self.bannerCount + 1){
			self.bannerUL.css({"left":-self.bannerWidth});
			self.index = 2;
		}else{
			self.index++;
		}
		self.animate();
	});
};

//动态创建轮播图的小原点
Banner.prototype.initPageControl = function(){
	var self = this;
	for(var i=0; i<self.bannerCount; i++){
		if(i === 0){
			self.pageControl.children("li:first-child").addClass("active");
		}
	}
};

//小圆点的点击事件
Banner.prototype.lsitenPageControl = function(){
	var self = this;
	self.pageControl.children("li").each(function(index,obj){
		$(obj).click(function(){
			self.index = index+1;
			self.animate();

		});
	});
};

////动态改变轮播图中.banner_ul .liList的宽度
Banner.prototype.bannerULwidth = function(){
	var self =this;
	self.liList.css({"width":self.bannerWidth});
	var firstBanner = self.liList.eq(0).clone();
	var lastBanner = self.liList.eq(self.bannerCount-1).clone();
	self.bannerUL.append(firstBanner);
	self.bannerUL.prepend(lastBanner);	
	self.bannerUL.css({"width":self.bannerWidth*(self.bannerCount+2),"left":-self.bannerWidth});
};


//这个是所有功能的集成函数，将所有的小功能运行
Banner.prototype.run = function(){
	//轮播内容宽度设置函数
	this.bannerULwidth();
	//自动轮播设置函数
	this.loop();
	//动态添加小圆点的函数
	this.initPageControl();
	//小圆点点击切换效果函数
	this.lsitenPageControl();
	//鼠标悬浮时的箭头效果函数
	this.listenBannerHover();
	//箭头点击效果函数
	this.listenArrowClick();
	
};
	

// 创建行函数并运行
$(function(){
	var banner = new Banner();
	banner.run();
});

