// 在页面加载后将首页的导航栏变成半透明
$(function(){
    $('.head').addClass('active');
    $('.nav_li').mouseenter(function(){
        $(this).css('background','rgba(245,245,245,0.4)');
    });

    $('.nav_li').mouseleave(function(){
        $(this).css('background','rgba(245,245,245,0)');
    });

})


$(function(){
    // 找到有几个新闻列表
    var NewListCount = $('.news_content').length;
    for(var n=0; n<NewListCount; n++){
        // 对每一个新闻列表进行遍历
        var NewList = $('.news_content').eq(n);
        // 找到新闻列表里面的每一个标签
        var NewTag = NewList.find('.new_tag');
        // 对标签机型计数
        var NewTagCount = NewTag.length;
        for(var m=0; m<NewTagCount; m++) {
            // 给每一个标签加上相应的数字
            NewTag.eq(m).text(m+1);
            // 给前三条加上active
            if(m<3){
                NewTag.eq(m).addClass('active');
            }
        }
    }
})



//鼠标滚动与悬浮事件
window.onscroll= function(){
    //变量t是滚动条滚动时，距离顶部的距离
    var t = document.documentElement.scrollTop||document.body.scrollTop;
    //当滚动到距离顶部小于170px时，导航条不透明且无阴影，按钮悬浮透明度为0.4，返回顶部按钮不出现
    if(t<120){
        $('#scrollup').css('display','none');
        $('.head').addClass('active');
        $('.head2').removeClass('active');
        $('.nav_li').mouseenter(function(){
            $(this).css('background','rgba(245,245,245,0.4)');
        });

        $('.nav_li').mouseleave(function(){
            $(this).css('background','rgba(245,245,245,0)');
        });

    // 滚动条下滑170px,返回顶部按钮出现，导航条背景为白色，阴影不出现，按钮悬浮透明度为1
    }else{
        $('#scrollup').css('display','block');
        $('.head').removeClass('active');
        $('.head2').addClass('active');
        $('.nav_li').mouseenter(function(){
            $(this).css('background','rgba(245,245,245,1)');
        });

        $('.nav_li').mouseleave(function(){
            $(this).css('background','rgba(245,245,245,0)');
        });
    }


}

// 文章的分类页面中，将处在哪个筛选条件下的条件名称激活
$(function(){
    var order = $('.order').text()
    $('.'+order).addClass('active');
    
})