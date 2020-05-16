


// 文章和文选封面上传
function articlecover() {
    var article_cover = document.getElementById('cover_input');
    var cover_img = document.getElementById('cover_img');
    var reads = new FileReader();
    reads.readAsDataURL(article_cover.files[0]);
    reads.onload = function(e) {
        cover_img.src = this.result;
        $("#cover_img").css("display", "block");
        $(".img_show").css("border","none");
        $(".img_tip").css("display","none");
    };
}

function articlecover2() {
    var article_cover2 = document.getElementById('cover_input2');
    var cover_img = document.getElementById('cover_img2');
    var reads = new FileReader();
    reads.readAsDataURL(article_cover2.files[0]);
    reads.onload = function(e) {
        cover_img.src = this.result;
        $("#cover_img2").css("display", "block");
        $(".img_show2").css("border","none");
        $(".img_tip2").css("display","none");
    };
}


$('#article_create_bar').click(function(){
    $('.article_release_box').css('display','block');
    $('.anthology_create_box').css('display','block');
    $('.banner_create_box').css('display','block');
    $('#putaway').css('display','block');
    $('#article_create_bar').css('display','none');
})

$('#putaway').click(function(){
    $('.article_release_box').css('display','none');
    $('.anthology_create_box').css('display','none');
    $('.banner_create_box').css('display','none');
    $('#putaway').css('display','none');
    $('#article_create_bar').css('display','block');
})