function friend_attention(friendid,userid){
    $.ajax({
             type:'POST',
             url:'/add_relation',
             data:{
                 relation_user_id:userid,
                 is_relation:0
             },
             dataType:'json',
             success:function(data) {
                var a = '<a href="#">已关注</a>'
                $('#friend_wrap_'+friendid).find('.btn_attention').empty().html(a);
             },
             error:function(xhr,type){
                 alert('操作失败!');
             }
         })

}


// load post reply
function load_post_reply(post_id){

    var reply_wrap = $('#post_'+post_id).find('div.u_post_reply_wrap');
    if(reply_wrap.length!=0){
        reply_wrap.remove();
        return;
    }
    var size =5;
    $.ajax({
            type:'get',
            url:'/get_post_reply',
            data:{
                 post_id:post_id,
                 no:defaultPage,
                 size:size
            },
            async:false,
            dataType:'json',
            success:function(data) {
                reply_list = data.reply_list;
                total=data.totalsize;
                reply_html = '<div class="u_post_reply_wrap col-sm-12">\
                         <div  class="reply_in_div"><input class="communityId" type = "hidden" value = "' +post.community_id+ '" >\
                         <input type = "text" onfocus = "replyInFocus(this)" onblur = "replyInFocus(this)"  class ="reply_input"></div>\
                         <div class="sub_reply_div col-sm-12 ';
                if(total==0){
                    reply_html =reply_html+' no_bm';
                }

                    reply_html =reply_html+'"><a id="submit_reply" class="comm-btn" href="javascript:void(0)"\
                          onclick="publishReply(' + post_id+ ')">提交</a></div>';
                length =reply_list.length;
                for(var k=0;k<length;k++){
                    reply =reply_list[k];
                    is_like = reply.is_like;
                    console.log(is_like)
                    reply_html = reply_html+ '<div class="'
                    if ( length < size && k == length-1){
                        reply_html =reply_html + 'no_bm '
                    }else{
                        reply_html =reply_html + 'bb '
                    }
                    reply_html = reply_html + 'u_reply_wrap  col-sm-12" >\
                                 <div class="r_user_head no_m_p  left col-sm-1"><a href="#">\
                                 <img class="comm-img-ss" src="' + reply.user.head_img_url+ '"></a>\
                                 </div>\
                                 <div class="p_r_content col-sm-10">\
                                 <div class="nameAcontent">\
                                 <div class="r_user_name no_m_p"><a href="#">' +reply.user.name+ ':</a></div> \
                                 <div class="r_user_reply_content no_m_p ">&nbsp;' + reply.content+ '</div> \
                                 </div>\
                                 <div class="timeAlike">\
                                 <span class="r_time no_m_p col-sm-6">' + reply.create_time+ '</span> \
                                 <input type = "hidden" id = "isliked-' +reply.id+ '" value = "' +is_like+ '"/>\
                                 <span class="r_good no_m_p col-sm-6"><a id = "link-' + reply.id + '"';

                    if(!is_like){
                        reply_html =reply_html+ ' class ="reply-liked-no"';
                    }
                    reply_html = reply_html + ' href="javascript:likeReply(' +reply.id+ ');"> \
                                 <i class ="glyphicon glyphicon-thumbs-up" aria-hidden="true" ></i></a>\
                                 <span id="count-' +reply.id + '" class="rely_like_count">';
                    if(reply.like_num != 0){
                        reply_html = reply_html +reply.like_num;
                    }
                    reply_html = reply_html+ '</span></span></div></div></div>';

                }
                if(data.totalsize > size){
                    reply_html =reply_html+ '<div class="r_more col-sm-12 "><a href="/post?post_id='+post_id+ '">点击查看更多</a></div></div>';
                }
                $('#post_'+post_id).append(reply_html);

            }
    })
}

// load right content  friends
function load_friends(currPageNo){
    $.ajax({
            type:'get',
            url:'/good_friends',
            data:{
                 user_id:user_id,
                 no:currPageNo,
                 size:fPageSize
            },
            async:false,
            dataType:'json',
            success:function(data) {
                friends = data.friends;
                var friend_html ='<ul>';
                if(friends.length==0){
                    friend_html='主人还没有好友';
                    $('.friend_content').empty().html(friend_html);
                }
                for(var k=0;k<friends.length;k++){
                    friend=friends[k]
                    friend_html=friend_html+'<li class="friend_head left col-sm-4">\
                                                <div class="no_m_p">\
                                                <a href="user_info?user_id='+friend.user.id+'">\
                                                <img class="comm-img-md" src="'+friend.user.head_img_url+'"></a></div>\
                                                <div class="f_name"><a href="user_info?user_id='+friend.user.id+'">'+friend.user.name+'</a></div>\
                                                </li>';

                }
                if(data.totalsize>3){
                    friend_html=friend_html+'<div class="col-sm-12 f_more"><a onclick="load_more_friends(1)" href="javascript:void(0)">查看更多</a></div>';
                }
                friend_html=friend_html+'</ul>';
                $('.friend_content').empty().html(friend_html);

            }
    })
}


// init post info
function load_post(currPageNo){
           $.ajax({
                 type:'get',
                 url:'/user_info_post',
                 data:{
                     user_id:user_id,
                     size:pageSize,
                     no:currPageNo
                 },
                async:false,
                dataType:'json',
                success:function(data) {
                    pageNo = data.no;
                    pageSize = data.size;
                    totalPages = Math.ceil(data.totalsize/pageSize);
                    postList = data.post_list;
                    post_html_text='';
                    if(postList.length==0){
                        post_html_text='<div col-sm-12 class="p_no_content">主人还没有发过贴</div>'
                        $('.user_post').html(post_html_text);
                        return;
                    }
                    for (var j =0 ;j<postList.length;j++){
                        post = postList[j];
                        post_html_text=post_html_text+'<div id="post_'+post.id+'" class="each_post_wrap col-sm-12">\
                        <div class="p_user_head col-sm-2 "><a href="#"><img class="comm-img-sm" src="'+post.user.head_img_url+'"></a> \
                        <a href="#"><span class="p_user_name" >'+post.user.name+'</span></a></div>\
                        <div class="p_title col-sm-9"><a href="/post?post_id='+post.id+'">'+post.title+'</a></div>\
                        <div class="u_post_content col-sm-10"><a href="/post?post_id='+post.id+'">'+post.content+'</a></div>\
                        <div class="u_post_foot col-sm-8">\
                        <span class="col-sm-6">'+post.create_time+'</span>\
                        <a href="javascript:void(0)" onclick="load_post_reply('+post.id+')"><i class="glyphicon glyphicon-comment"></i><span class="u_post_comment">&nbsp;评论\
                        <i class="floor_num">'
                        if(post.floor_num>0)
                            post_html_text=post_html_text+post.floor_num
                        post_html_text = post_html_text+'</i></span></a>\
                        <a class="delete_p_btn" href="javascript:void(0)" onclick="deletePost('+post.id+')">删除\
                        </div>\
                        </div>\
                        </div>\
                        </div>'
                    }
                    $('.user_post').html(post_html_text)
                }
           });

}
/* delete post start*/
function deletePost(postid) {
    if (confirm('你确定删除帖子吗？帖子的评论也将会删除。')) {
        var data = {
            data: JSON.stringify({
                "post_id": postid
            })
        }
        $.ajax({
            url: '/delete_post',
            type: 'POST',
            data: data,
            success: function(data) {
                if (data.result== 0) {
                    window.location.reload();
                } else {
                    alert('删除失败')
                }
            },
            error: function(data) {
                alert('删除失败')
            }
        })
    }
}
/* delete post end*/



// get more friends
function load_more_friends(currPageNo){

    $('#post_container').remove();
    var data= {
              data:JSON.stringify({
                 user_id:user_id,
                 no:currPageNo,
                 size:fPageSize
             })
            }

    $.ajax({
            type:'get',
            url:'/good_friends',
            data:{
                 user_id:user_id,
                 no:currPageNo,
                 size:fPageSize
             },
            async:false,
            dataType:'json',
            success:function(data) {
                friend_html='';
                friends=data.friends;
                defaultParam='未知'
                var len = data.friends.length;
                var default_relation=''
                for(var i=0;i<len;i++){
                    user=friends[i].user;
                    if(friends[i].is_relation){
                      default_relation='<div class="btn_attention"><a href="#">已关注</a></div>'
                    }else{
                      default_relation='<div class="btn_attention"><a onclick="friend_attention('+friends[i].id+','+user.id+')" href="javascript:void(0)">+关注</a></div>'
                    }
                    if(user.location==null){
                        user.location= defaultParam
                    }
                    if(user.professional==null){
                        user.professional= defaultParam
                    }
                     friend_html =friend_html+'<div id="friend_wrap_'+friends[i].id+'" class="friend_wrap col-sm-11"'
                    if(i==(data.friends.length-1)){
                        friend_html =friend_html+' style="border:none;" ';
                    }
                   friend_html =friend_html+'>\
                                   <div class="f_w_user_head"><a href="#"><img class="comm-img-sm" src="'+user.head_img_url+'"></a></div>\
                                   <div class="f_w_user_info col-sm-6">\
                                     <div class="f_w_user_name col-sm-12">'+user.name+'</div>\
                                      <div class="f_w_user_desc col-sm-12">\
                                          <ul>\
                                              <li>关注<span>'+user.attention_num+'</span></li>\
                                              <li>粉丝<span>'+user.by_attention_num+'</span></li>\
                                             <li>发帖<span>'+user.post_num+'</span></li>\
                                          </ul>\
                                          <div class="f_w_user_address col-sm-12">地址 '+user.location+'</div>\
                                          <div class="f_w_user_professial col-sm-12">职业 '+user.professional+'</div>\
                                      </div>\
                                   </div>\
                                   <div class="f_w_btn_attention col-sm-2">';
                   friend_html =friend_html+default_relation+'</div></div>';
                }
                fPageNo = data.no;
                fPageSize = data.size;
                fTotalPages = Math.ceil(data.totalsize/fPageSize);
                $('.friend_content').empty().html(friend_html)
                $('#friend_container').css('display','block');

            }
     })

}

//more friends end


//publish reply start
function publishReply(post_id){
    if(login_userid==0){
        alert("登录后再来回复吧！");
    }
   var input =$('#post_'+post_id).find('input.reply_input')
   var content = input.val();
   var communityId = $('#post_'+post_id).find('input.communityId').val();
   if(content ==""){
        alert('内容不能为空！')
        return false;
   }

   var data= {
          data:JSON.stringify({
             content:content,
             create_user_id:login_userid,
             post_id:post_id,
             community_id:communityId
         })
            }
   $.ajax({
         type:'POST',
         url:'/user_info_publish_reply',
         data:data,
         dataType:'json',
         success:function(data) {
             reply = data.reply;
             is_like = 'False';
             reply_html = '<div class="u_reply_wrap bb col-sm-12"> \
             <div class="r_user_head no_m_p  left col-sm-1"><a href="#">\
             <img class="comm-img-ss" src="' + reply.user.head_img_url + '"></a>\
             </div>\
             <div class="p_r_content col-sm-10">\
             <div class="nameAcontent">\
             <div class="r_user_name no_m_p left"><a href="#">' + reply.user.name + ':</a></div>\
             <div class="r_user_reply_content no_m_p">&nbsp;'  + reply.content+ '</div> \
             </div>\
             <div class="timeAlike">\
             <span class="r_time no_m_p col-sm-6">' + reply.create_time + '</span>\
             <input type = "hidden" id = "isliked-' + reply.id + '" value = "' +is_like + '"/>\
             <span class="r_good no_m_p col-sm-6"><a id = "link-' +reply.id+ '"\
              class ="reply-liked-no"\
              href="javascript:likeReply(' +reply.id + ');">\
             <i class ="glyphicon glyphicon-thumbs-up" aria-hidden="true" ></i></a>\
             <span id="count-' +reply.id + '" class="rely_like_count">\
              </span></span>\
             </div>\
             </div>\
             </div>';
             var count = $('#post_'+post_id).find('i.floor_num').text();
             if (count==""){
                count=0;
             }
             var reply_wrap =$('#post_'+post_id).find('div.u_reply_wrap');
             $('#post_'+post_id).find('i.floor_num').text(parseInt(count)+1);
             input.val('');
             $('#post_'+post_id).find('.sub_reply_div').removeClass('no_bm')
             $('#post_'+post_id).find('.sub_reply_div').after(reply_html);
             if(reply_wrap.length==0){
                $('#post_'+post_id).find('.u_reply_wrap').removeClass('bb');
                $('#post_'+post_id).find('.u_reply_wrap').addClass('no_bm');
             }
         }
   });

}
//publish reply end
function replyInFocus(object){
   $(object).parent().addClass('onfoucs_border');

}
function onblur(object){
   $(object).parent().removeClass('onfoucs_border');
}

