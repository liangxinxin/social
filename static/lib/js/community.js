//初始化页面
function initData(){
   getLoginInfo();
   loadCommunityPost(1);
   load_commend_community();
   var callback = function(page_no){
       loadCommunityPost(page_no)
   }
   $("#page").initPage(num_page,total,page_no,callback);
}
 $('#u-cancel').click(function(){
   var name = $('h4.hname').find('span').text();
   var desc = $('.content').find('p.pdesc').html();
   $('input[name=cname]').val(name)
   $('textarea[name=cdesc]').val(desc)

});
$('#update').click(function(){
   var name =  $('input[name=cname]').val()
   var desc = $('textarea[name=cdesc]').val()
   if ($.trim(name)==''){
       alert('请填写社区名')
   }
   var data ={}
   data['id']=community_id;
   data['name']=name;
   data['desc']=desc;
   data['type']='update'
   $.ajax({
        type:'POST',
        url:'/update_community',
        data:data,
        dataType:'json',
        timeout:5000,
        success:function(data){
               if(data.result==0){
                    $('h4.hname').find('span').text(name);
                    $('.content').find('p.pdesc').html(desc);
                    $('input[name=cname]').val(name)
                    $('textarea[name=cdesc]').val(desc)
                    $('#u-cancel').click();
               }else{
                    alert('修改失败!')
               }
        },
        error:function(xhr, type) {
            alert('修改失败!')
        }

   })


})
function remove_match(){
    $('#button_publish_post').removeAttr('disabled')
    <!--$('#div_publish_post_title').find('ul.dropdown-menu').remove();-->
    $('#submit').val('true');
 }
var flag;
$('#input_publish_post_title').keyup(function(){
     clearTimeout(flag);
       //延时500ms执行请求事件，如果感觉时间长了，就用合适的时间
       //只要有输入则不执行keyup事件
      flag = setTimeout(function(){
       //这里面就是调用的请求
          find_match_post();
        }, 500);

})
 function find_match_post(){
        var title = $('#input_publish_post_title').val();
        $('input#input_publish_post_title~ul').remove();
        if (title.trim()!=""){
            $.ajax({
              url:'/find_match_post',
              type:'get',
              dataType:'json',
              async:false,
              data:{
                title:title
              },
              timeout:5000,
              success:function(data){
                  posts = data.post_list
                  if (posts !=null && posts.length>0){
                      drop_menu='<ul class="dropdown-menu"><li><a style="color:#337ab7;" class="match_info" href="#">已有类似的帖子,不能再次发表,请点击查看</a></li>'
                      for(var i =0;i<posts.length;i++){
                        drop_menu =drop_menu +'<li><a href="/post?post_id='+posts[i].id+'">'+posts[i].title+'</a></li>'
                      }
                      drop_menu =drop_menu+'</ul>'
                      $('#submit').val('false');
                      $('#input_publish_post_title').after(drop_menu);
                      $('.post-input').addClass('open');
                      $('#button_publish_post').attr('disabled','disabled')
                  }else{
                    $('#button_publish_post').removeAttr('disabled')
                  }
              }

            })
        }
 }

 $('a#summit-post').click(function(){
     var is_submit =  $('#submit').val()
     if(is_submit=='true'){
     //get title
       var title=document.getElementById("input_publish_post_title").value;
       //get content
       var content=$('#editor').html();
       if (title==""){
          alert('标题不能为空');
          return;
       }
       if(content.trim()=="" || content==null || content.length==0){
          alert('内容不能为空');
          return;
       }
       //post request for save post
       if(user_id>0){
        postRequest("/post_publish",{"type":"publish","title":title,"content":content,"create_user_id":user_id,"community_id":community_id});
       }else{
        alert('您需要登录后才能发帖哦！');
       }
     }


 })

 function postRequest(URL, PARAMS) {

     var temp = document.createElement("form");
     temp.action = URL;
     temp.method = "post";
     temp.style.display = "none";
     for (var x in PARAMS) {
         var opt = document.createElement("textarea");
         opt.name = x;
         opt.value = PARAMS[x];
         temp.appendChild(opt);
     }
     document.body.appendChild(temp);
     temp.submit();
     return temp;
 }
function publish_post() {
    <!--find_match_post();-->
     var is_submit =  $('#submit').val()
     if(is_submit=='true'){
     //get title
       var title=document.getElementById("input_publish_post_title").value;
       //get content
       var content=$('#editor').html();
       if (title==""){
          alert('标题不能为空');
          return;
       }
       if(content.trim()=="" || content==null || content.length==0){
          alert('内容不能为空');
          return;
       }
       var id=document.getElementById("community_id").value;
       //post request for save post
       if(user_id>0){
        post("/post_publish",{"type":"publish","title":title,"content":content,"create_user_id":user_id,"community_id":community_id});
       }else{
        alert('您需要登录后才能发帖哦！');
       }
     }
 }


function load_commend_community(){
    var data = {}
    data['community_id'] = community_id;
    data['type'] = 'commend_community';
    $.ajax({
        type: 'get',
        url: '/get_commend_community',
        data: data,
        dataType: 'json',
        timeout: 5000,
        async:false,
        success: function(data) {
            //<div class="span"><a href="#" class="btn btn-default"><i>+</i>加入</a></div>
            commend_list = data.commend_list
            var commend_wrap ='';
            for(var i=0;i<commend_list.length;i++){
                community = commend_list[i]
                commend_wrap =commend_wrap+'<div class="community-block">\
                                       <div class="img"><img src="../images/img.png"></div>\
                                       <div class="content">\
                                           <h4><a href="#">'+community.name+'</a></h4>\
                                           <p>'+community.describe+'</p>\
                                       </div>\
                                       <div class="blk-1x"></div>\
                                       <div class="divider solid"></div>\
                                       <div class="block-bar">\
                                            <div class="span"><em>帖子</em><b>'+community.post_num+'</b></div>\
                                            <div class="span"><em>成员</em><b>'+community.user_num+'</b></div>\
                                       </div>\
                                   </div>';

            }
            $('.side-container').append(commend_wrap);
        },
        error: function(xhr, type) {
        }
    })



}


// load post
function loadCommunityPost(page_no){
    var data = {};
    data['type'] = 'getpost';
    data['community_id'] = community_id;
    data['page_no'] = page_no;
    data['num_perpage'] = num_page;
    $.ajax({
        type: 'get',
        url: '/get_community_post',
        data: data,
        dataType: 'json',
        timeout: 5000,
        async:false,
        success: function(data) {
            post_list = data.post_list
            var post_wrap ='';
            for(var i=0;i<post_list.length;i++){
                post=post_list[i];
                user=post_list[i].user
                post_wrap=post_wrap+ '<div class="item">\
                                        <div class="photo">\
                                            <a href="/user_info?user_id='+user.id+'">\
                                                <img src="'+user.head_img_url+'"></a>\
                                        </div>\
                                        <div class="content">\
                                            <h4><a href="/post?post_id='+post.id+'&community_id='+post.community_id+'">'+post.title+'</a>\
                                            </h4>\
                                            <p>'+post.content+'</p>\
                                            <div class="block-bar">\
                                                <span><a href="#">'+user.name+'</a></span>\
                                                <div class="control-right">\
                                                    <div class="row-1x">\
                                                        <div class="group-span-1x"><span>'+post.create_time+'</span>\
                                                        <span><a href="#"><em>评论</em></a><b>'+post.floor_num+'</b></span></div>\
                                                    </div>\
                                                </div>\
                                            </div>\
                                        </div>\
                                    </div>';
            }
            $('.post-list').html(post_wrap);
            total = data.total;
            page_no=page_no;

        },
        error: function(xhr, type) {
        }
    })

}
// click left
$('#left').click(function() {
    if (user_id > 0) {
        var data = {};
        data['type'] = 'left';
        data['user_id'] = user_id;
        data['community_id'] = community_id;
        $.ajax({
            type: 'POST',
            url: '/user_community',
            data: data,
            dataType: 'json',
            timeout: 5000,
            success: function(data) {
                alert('您已离开社区!');
                $('.comm_user_num').text(data['user_num']);
                $('#left').addClass('hide');
                $('#join').removeClass('hide');
            },
            error: function(xhr, type) {
                alert('离开社区失败!');
            }
        })
    } else {
        alert('登录后才能离开社区哦！');
    }

})
// click join
$('#join').click(function() {
    if (user_id > 0) {
        var data = {};
        data['type'] = 'join';
        data['user_id'] = user_id;
        data['community_id'] = community_id;
        $.ajax({
            type: 'POST',
            url: '/user_community',
            data: data,
            dataType: 'json',
            timeout: 5000,
            success: function(data) {
                alert('加入社区成功!');
                $('.comm_user_num').text(data['user_num']);
                $('#join').addClass('hide');
                $('#left').removeClass('hide');
            },
            error: function(xhr, type) {
                alert('加入社区失败!');
            }
        })
    } else {
        alert('登录后才能加入社区哦！');
    }
})