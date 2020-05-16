// 弹窗JS

//导航栏点击事件
// $('.nav_li').click(function(){
//     $('.nav_li').css('border-bottom','5px solid #fff');
//     $(this).css('border-bottom','5px solid #FF7F00');
// })

// 点击事件下的下拉菜单
$('.c_main_menu').click(function(event){

    var display = $(this).next().css('display')
    if(display == 'none'){
		$('.minor_menu').css('display','none');
        $(this).next().css('display','block');
    }else{
        $(this).next().css('display','none');
    }
    event.stopPropagation();
})
$(document).click(function(){
    $('.minor_menu').css('display','none');
})

// 悬浮事件下的下拉菜单
$('.h_main_menu').mouseenter(function(){
	$(this).children('.minor_menu').css('display','block');
})

$('.h_main_menu').mouseleave(function(){
	$(this).children('.minor_menu').css('display','none');
})




//点击搜索按钮展开搜索框，展开按钮隐藏，关闭按钮出现
// $('.search_show').click(function(){
//     $(this).css('display','none')
//     $('.search_close').css('display','block');
    
//     $('#search').animate({width:'300px',paddingLeft:'17px'});
//     $('#search_button').css('opacity','1');
// })
//点击关闭按钮，搜索框隐藏，关闭按钮隐藏，展开按钮出现
// $('.search_close').click(function(){
//     $(this).css('display','none')
//     $('.search_show').css('display','block');
    
//     $('#search').animate({width:'0px',paddingLeft:'0px'});
//     $('#search_button').css('opacity','0');
// })


// ------------------------------------以下是登录界面的JS设置-----------------------------------

// 点击登录按钮跳出弹出框
// $('.user_login').click(function(){
//     $('.log_right_banner').css('left','0')
//     $('.pop').css('display','block');
// });
// 点击注册按钮跳出弹出框
// $('.user_register').click(function(){
//     $('.log_right_banner').css('left','-420px')
//     $('.pop').css('display','block');
// });

//点击文章删除按钮跳出弹出框
// $('.article_delete').click(function(){
//     $('.pop').css('display','block');
// });

// 点击灰色背景或者关闭按钮关闭弹出框
$('.pop_back, .close_pop').click(function(){
    $('.pop').css('display','none');
})

// .collect_bar标签添加点击事件
// $(document).on('click','.collect_bar',function(){
//     alert(0);
// })


// 对登录界面的参数进行设置
// function Log(){
//     this.loginButton = $(".login_button");
//     this.logoutButton = $(".register_button");
//     this.logBanner = $(".log_right_banner");
//     this.logRight = $(".login_box");
//     this.logWidth = this.logRight.outerWidth();
//     this.index = 0
// }


// 切换登录界面的速度是1秒
// Log.prototype.animate = function(){
//     var self =this;
//     self.logBanner.animate({"left":self.logWidth*self.index},1000);
// };

//登录按钮的点击事件
// Log.prototype.logClick = function(){
//     var self = this;
//     self.loginButton.click(function(){  
//         self.index = 0;     
//         self.animate();
//     });

//     self.logoutButton.click(function(){
//         self.index = -1;
//         self.animate();
//     });
// };

// Log.prototype.run = function(){
//     this.logClick();   
// };

// $(function(){
//     var log = new Log();
//     log.run();
// });

//点击输入框的时候底部线条颜色变化
// $(".input_set").click(function(){
//     $(".input_set").css('border-bottom','1px solid #D3D3D3');
//     $(this).css('border-bottom','1px solid #FFA54F');
// });

//点击切换验证码
$(".img_captcha").click(function(){
    $(this).attr("src","/user/captcha/"+"?random="+Math.random())
});





// 回到顶部按钮动画设置
window.onscroll= function(){
    //变量t是滚动条滚动时，距离顶部的距离
    var roll = document.documentElement.scrollTop||document.body.scrollTop;
    //当滚动到距离顶部200px时，返回顶部的按钮显示
    if(roll>=200){
        $('#scrollup').css('display','block');
    }else{          //恢复正常
        $('#scrollup').css('display','none');
    }
}

// 悬浮在删除按钮上是提示语出现
$('.anthology_delete').mouseenter(function(){
    $(this).parent('.detail_3').next().css('display','block');
})

$('.anthology_delete').mouseleave(function(){
    $(this).parent('.detail_3').next().css('display','none');
})
