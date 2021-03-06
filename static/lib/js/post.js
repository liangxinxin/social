//初始化页面
var callbackPage = function(page_no){
       loadReply(page_no)
   }
function initData(){
   $("#page").initPage(num_perpage,total,page_no,callbackPage);
}
function post(URL, PARAMS) {
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
$('#post_del').click(function(){
    if(confirm('你确定删除这条帖子吗?其下的评论也将被删除')){
         var data ={}
         data['type'] = 'delete';
         data['post_id'] = post_id;
        $.ajax({
            url:'delete_post',
            type:'POST',
            dataType:'json',
            data:data,
            timeout:5000,
            success:function(data){
                if(data.result==0){
                    alert('帖子已被删除')
                    window.location.href ='/index'
                }else{
                    alert('删除失败')
                }
            }
        })

    }

})
$('#submmit-btn').click(function(){
       var content=$('#editor').html();
       var best = $('div.best-like').length==1;  //判断页面是否有最佳回帖
       if(login_user_id>0){
            var data = {};
            data['type'] = 'publish';
            data['post_id'] = post_id;
            data['content'] = content;
            data['community_id'] = community_id;
            data['num_perpage'] = num_perpage;
            data['has_best'] = best;
            if($.trim(content)=="" || content==null || content.length==0){
                  alert('内容不能为空');
                  return;
            }
            $.ajax({
                type: 'POST',
                url: '/reply_publish',
                data: data,
                dataType: 'json',
                timeout: 5000,
                success: function(data) {
                    if (data.reply !=null && data.total_page!=null){
                        total_page = data.total_page;
                        page_no = total_page;
                        $("#page").initPage(num_perpage,data.replycount,page_no,callbackPage);
                        $('#editor').empty();
                    }else{
                        alert('回复失败!');
                    }
                },
                error: function(xhr, type) {
                    alert('回复失败!');
                }
            })
    } else {
        alert('登录后才能回复哦！');
    }
})
//when click huifu
function getHuifuHtml(reply_id,comment_id){
    var huifu = '<div class="huifu">\
                    <button id="huifu-btn" class="btn huifu-btn" onClick="summitHuifu()" href="javascript:void(0)">提交</button>\
                    <div class="input-huifu">\
                                <input type="hidden" class="rid" value="'+reply_id+'">\
                                <input type="hidden" class="cid" value="'+comment_id+'">\
                                <div id="input-content" class="input-content" contenteditable="true"></div>\
                    </div>\
                 </div>';
    return huifu;
}
function summitHuifu(){

    var reply_id = $('div.huifu').find('input.rid').val();
    var comment_id = $('div.huifu').find('input.cid').val();
    var content = $('div.huifu').find('div.input-content').html();
    var index_huifi = content.indexOf('回复');
    var index = content.indexOf(':');
    if(index_huifi!=-1 && index!=-1){
        content = content.substring(index+1,content.length)
    }
    if($.trim(content)==''){
        alert('您还没有填写回复内容')
        return;
    }
    if (reply_id!=''){
        var data = {};
        data['type'] = 'publish';
        data['reply_id'] = reply_id;
        data['comment_id'] = comment_id;
        data['community_id'] = community_id;
        data['content'] = content;
        $.ajax({
            type: 'POST',
            url: '/publish_comment',
            data: data,
            dataType: 'json',
            success: function(data) {
                if(data.code==0){
                    comment = data.comment;
                    var comment_html = getCommentHtml(comment);
                    $('#item_'+reply_id).find('div.comment-wrap').append(comment_html);
                    var old_reply_num = $('#item_'+reply_id).find('input.hide-reply-num').val();
                    var reply_num =parseInt(old_reply_num)+1;
                    if(old_reply_num==0){
                        var reply_num_html='<span class="drop-toggle"><a class="reply-num" onClick="showComments('+reply_id+')" href="javascript:void(0)"><span>'+reply_num+'</span>条回复 <i class="icon-arrow-up"></i></a></span>';
                        $('#item_'+reply_id).find('span.reply-btn-span').after(reply_num_html)
                    }else{
                        $('#item_'+reply_id).find('a.reply-num>span').text(reply_num);
                    }
                    $('#item_'+reply_id).find('input.hide-reply-num').val(reply_num);
                    //showComments(reply_id);
                    $('#item_'+reply_id).find('div.comment-wrap').removeClass('hide');
                    $('#item_'+reply_id).find('div.huifu').remove();

                }else{
                    alert('回复失败!')
                }
            },
            error: function(xhr, type) {
                alert('回复失败!');
            }
        })

    }

}

function set_focus(){
    el=document.getElementById('input-content');
    //el=el[0];  //jquery 对象转dom对象
    el.focus();
    if($.support.msie){
        var range = document.selection.createRange();
        this.last = range;
        range.moveToElementText(el);
        range.select();
        document.selection.empty(); //取消选中
    }else{
        var range = document.createRange();
        range.selectNodeContents(el);
        range.collapse(false);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    }
}

function doHuifu(reply_id,comment_id){
    if(login_user_id>0){
        var huifu_input = getHuifuHtml(reply_id,comment_id);
        $('div.huifu').remove();
        $('#item_'+reply_id).append(huifu_input);
        var name = '';
        if(comment_id !=undefined && comment_id!=''){
           name=$('#comment_'+comment_id).find('div.content').find('a.name').text();
           $('#item_'+reply_id).find('div.input-content').html('回复'+name+':');
           set_focus();
        }
    }else{
        alert('登录后才能回复哦！')
    }
}
function doHuifuReply(reply_id){

    if(login_user_id>0){
        var huifu_input = getHuifuHtml(reply_id,0);
        $('div.huifu').remove();
        $('#item_'+reply_id).append(huifu_input);
        $('#item_'+reply_id).find('div.input-content').focus();
    }else{
        alert('登录后才能回复哦！')
    }
}
function showComments(reply_id){
    $('#item_'+reply_id).find('div.comment-wrap').toggleClass('hide');
    if($('#item_'+reply_id).find('div.comment-wrap').hasClass('hide')){
        $('#item_'+reply_id).find('a.reply-num').find('i').removeClass('icon-arrow-down').addClass('icon-arrow-up');
    }else{
        $('#item_'+reply_id).find('a.reply-num').find('i').removeClass('icon-arrow-up').addClass('icon-arrow-down');
    }

}
function getCommentHtml(comment){
    var comment_wrap='';
    var user = comment.user;
    var is_delete ='';
    if(comment.parent_id>0){
        content='<span>回复<a href="user_info_post?type=1&user_id='+comment.touser.id+'">'+comment.touser.name+'</a></span>：'+comment.content;
    }else{
        content = comment.content;
    }
    if(login_user_id==comment.create_user_id){
        is_delete ='<span><a onClick="deleteComment('+comment.reply_id+','+comment.id+')" href="javascript:void(0)">删除</a></span>';

    }
    comment_wrap='<div id="comment_'+comment.id+'" class="item">\
                    <div class="photo">\
                        <a href="user_info_post?type=1&user_id='+user.id+'"><img src="'+user.head_img_url+'"></a>\
                    </div>\
                    <div class="content">\
                        <div class="block-bar">\
                            <span><a class="name"  href="user_info_post?type=1&user_id='+user.id+'">'+user.name+'</a></span>\
                            <span>'+comment.create_time+'</span>\
                        </div>\
                        <p>'+content+'</p>\
                        <div class="block-bar action">\
                            <span><a onClick="doHuifu('+comment.reply_id+','+comment.id+')" href="javascript:void(0)">回复</a></span>\
                            '+is_delete+'\
                        </div>\
                    </div>\
                </div>';
    return comment_wrap;
}

function moreComment(replyId){
    var comment_page_no = $('#item_'+replyId).find('input.comment_page_no').val();
    var next_page_no = parseInt(comment_page_no)+1;
    var data = {};
    data['type'] = 'query';
    data['reply_id'] = replyId;
    data['page_no'] = next_page_no;
    data['num_perpage'] = num_perpage;
    $.ajax({
        type: 'GET',
        url: '/get_comment',
        data: data,
        dataType: 'json',
        timeout: 5000,
        success: function(data) {
           var comment_list = data.comment_list;
           var has_next = data.has_next;
           if(comment_list.length>0){
               var more_comment ='';
               for(var i=0;i<comment_list.length;i++){
                   more_comment+=getCommentHtml(comment_list[i]);
               }
           }
           $('#item_'+replyId).find('div.comment-wrap').append(more_comment)
           if(has_next){
                $('#item_'+replyId).find('input.comment_page_no').val(next_page_no);
           }else{
                $('#item_'+replyId).find('span.more-comment').remove();
           }
        },
        error: function(xhr, type) {
            alert('加载失败!');
        }
    })

}

function getReplyHtml(reply,comment_wrap,isBest){
    var like_num ='';
    var reply_wrap='';
    var comment_num='';
    var more_comment='';
    var user = reply.user;
    var comment_page_no =1;
    var is_delete ='';
    var is_update =''
    var is_best='';
    if (reply.like_num > 0){
      like_num = reply.like_num.toString();
    }
    var is_like = '<input type="hidden" id="like-'+reply.id+'" value="true">\
                <a onClick="doGood('+reply.id+')" href="javascript:void(0)"><i class="icon-like"></i></a>\
                <span class="like-num">'+like_num+'</span>';
    if(reply.floor_num>0){
        comment_num='<span class="drop-toggle"><a class="reply-num" onClick="showComments('+reply.id+')" href="javascript:void(0)"><span>'+reply.floor_num+'</span>条回复 <i class="icon-arrow-up"></i></a></span>';
    }
    if(reply.floor_num>num_perpage){
        more_comment ='<span class="more-comment"><a href="javascript:void(0)" onClick="moreComment('+reply.id+')">查看更多</a>\
        <input class="comment_page_no" type="hidden" value ="'+comment_page_no+'"></span>';
    }
    if(reply.islike){
        is_like = '<input type="hidden" id="like-'+reply.id+'" value="false">\
                <a class="like" onClick="doGood('+reply.id+')" href="javascript:void(0)"><i class="icon-like"></i></a>\
                <span class="like-num">'+like_num+'</span>';
    }else{
        is_like = '<input type="hidden" id="like-'+reply.id+'" value="true">\
                <a class="like" onClick="doGood('+reply.id+')" href="javascript:void(0)"><i class="icon-like-o"></i></a>\
                <span class="like-num">'+like_num+'</span>';
    }
    if(login_user_id==reply.create_user_id){
        is_delete ='<span><a onClick="deleteReply('+reply.id+')" href="javascript:void(0)">删除</a></span>';
        is_update ='<span><a onClick="toUpdate('+reply.id+')" href="javascript:void(0)">修改</a></span>';

    }
    if(isBest){
        is_best = '<div class="best-like"></div>';
        is_update ='';
    }
    reply_wrap = reply_wrap+'<div id="item_'+reply.id+'" class="item" >\
            <input class="hide-reply-num" type="hidden" value ="'+reply.floor_num+'">\
            <div class="photo">\
                <a href="user_info_post?type=1&user_id='+user.id+'"><img src="'+user.head_img_url+'"></a>\
            </div>\
            <div class="content">\
                '+is_best+'\
                <div class="block-bar">\
                    <span><a href="user_info_post?type=1&user_id='+user.id+'">'+reply.user.name+'</a></span>\
                    <span>'+reply.last_update_time+'</span>\
                </div>\
                <div class="cp"><p>'+reply.content+'</p></div>\
                <div class="block-bar action">\
                    <span class="reply-btn-span"><a onClick="doHuifuReply('+reply.id+')" href="javascript:void(0)">回复</a></span>'+comment_num+'\
                    '+is_delete+'\
                    '+is_update+'\
                    <div class="right-control">\
                        '+is_like+'\
                        </span>\
                    </div>\
                </div>\
                <div class="comment-wrap hide">\
                '+comment_wrap+'\
                '+more_comment+'\
                </div>\
            </div>\
        </div>';
    return reply_wrap;
}
function toUpdate(reply_id){
    var content = $('#item_'+reply_id).find('div.content').find('p');
    content.addClass('hide');
    $('.update-reply').removeClass('hide')

    $('#item_'+reply_id).find('div.cp').append($('.update-reply'));
    $('.update-reply').find('input#param').val(String(reply_id));
    $('div.update-reply').find('div#update').focus();
    $('div.update-reply').find('div#update').html($(content).html());

}
function cancelUpdate(){
    $('.post-list').before($('.update-reply').addClass('hide'));
    var reply_id = $('.update-reply').find('input#param').val();
    $('#item_'+reply_id).find('div.content').find('p').removeClass('hide');
    $('div.update-reply').find('input#param').val(0);
}
function doUpdate(){
    var content = $('div.update-reply').find('div#update').html();
    if($.trim(content)==''){
        alert('内容不能为空！');
        return;
    }
    var reply_id = $('.update-reply').find('input#param').val();
    var data = {}
    data['type']='update';
    data['reply_id']=reply_id;
    data['content']=content;
    $.ajax({
        url: '/update_reply',
        type: 'POST',
        data: data,
        timeout:5000,
        success: function(data) {
            if (data.result== 0) {
                $('.post-list').before($('.update-reply').addClass('hide'));
                $('#item_'+reply_id).find('.update-reply').remove();
                $('#item_'+reply_id).find('div.content').find('p').html(content);
                cancelUpdate();
            } else {
                alert('修改失败')
            }
        },
        error: function(data) {
            alert('修改失败')
        }
    })

}
function deleteReply(reply_id){
    if (confirm('你确定删除这条回帖吗？其下的回复也将会被删除')) {
        var data ={}
        data['type']='delete';
        data['reply_id'] = reply_id;
        $.ajax({
            url:'delete_reply',
            type:'POST',
            dataType:'json',
            data:data,
            timeout:5000,
            success:function(data){
                if(data.code==0){
                    $('.post-list').find('#item_'+reply_id).remove();
                    var length = $('.post-list').find('.item').length;
                    if(length==0 && page_no>1){
                        page_no = page_no -1;
                        $("#page").initPage(num_perpage,data.replycount,page_no,callbackPage);
                    }
                }else{
                    alert('删除失败')
                }
            }
        })

    }
}

function deleteComment(reply_id,comment_id){
     if (confirm('你确定删除这条回复吗?')) {
        var data={}
        data['type']='delete';
        data['comment_id'] = comment_id;
        $.ajax({
            url:'delete_comment',
            type:'POST',
            dataType:'json',
            data:data,
            timeout:5000,
            success:function(data){
                if(data.result==0){
                    var reply_num =  $('#item_'+reply_id).find('input.hide-reply-num').val();
                    reply_num =  parseInt(reply_num)-1;
                    if(reply_num==0){
                         $('#item_'+reply_id).find('span.drop-toggle').remove();
                    }
                    $('#item_'+reply_id).find('input.hide-reply-num').val(reply_num);
                    $('#item_'+reply_id).find('a.reply-num>span').text(reply_num);
                    $('#item_'+reply_id).find('#comment_'+comment_id).remove();

                }else{
                    alert('删除失败！')
                }

            }
        })
     }
 }

function doGood(reply_id){
    if (login_user_id > 0) {
        var mod_type = ''
        var is_like = $('#like-'+reply_id).val();
        if (is_like=='true'){
            mod_type = 'add';
        }else{
            mod_type = 'remove';
        }
        var data = {};
        data['type'] = 'like';
        data['reply_id'] = reply_id;
        data['mod_type'] = mod_type;
        $.ajax({
            type: 'POST',
            url: '/reply_like_status_change',
            data: data,
            dataType: 'json',
            //timeout: 5000,
            success: function(data){
                if(data.code==0){
                    var like_num = data.like_num;
                    if(mod_type == 'add'){
                         $('#like-'+reply_id).val("false");
                         $('#item_'+reply_id).find('a.like>i').removeClass('icon-like-o').addClass('icon-like');
                    }else{
                         $('#like-'+reply_id).val("true");
                         $('#item_'+reply_id).find('a.like>i').removeClass('icon-like').addClass('icon-like-o');
                    }
                    if(like_num>0){
                        $('#item_'+reply_id).find('span.like-num').text(like_num);

                    }else{
                        $('#item_'+reply_id).find('span.like-num').text('');

                    }
                    // something todo
                }else{
                    alert(' 操作失败！')
                }
            },
            error: function(xhr, type) {
                alert('操作失败!');
            }
        })
    } else {
        alert('登录后才能点赞哦！');
    }

}
function loadReply(page_no){
    var data = {};
    data['type'] = 'query';
    data['post_id'] = post_id;
    data['page_no'] = page_no;
    data['num_perpage'] = num_perpage;
    data['comment_num_perpage'] = num_perpage;
    $.ajax({
        type: 'get',
        url: '/get_reply',
        data: data,
        dataType: 'json',
        timeout: 5000,
        async:false,
        success: function(data) {
            var reply_list = data.reply_list;
            var best_reply = data.best_reply;
            var best_reply_like ='';
            var best_reply_wrap ='';
            var best_reply_comment='';
            var reply_wrap ='';
            var isBest= false;
            if(best_reply!=null && page_no == 1){
                var best_reply_comments = best_reply.comments;
                if(best_reply_comments!=null){
                    for(var i=0;i< best_reply_comments.length ;i++){
                        best_reply_comment+=getCommentHtml(best_reply_comments[i]);
                    }
                }
                isBest= true;
                best_reply_wrap+= getReplyHtml(best_reply,best_reply_comment,isBest);
            }
            isBest= false;
            for(var i=0;i<reply_list.length;i++){
                var reply = reply_list[i];
                var user = reply_list[i].user;
                var reply_comments = reply_list[i].comments;
                var reply_comment='';
                if(reply_comments.length>0){
                   for(var j=0;j<reply_comments.length;j++){
                    reply_comment +=getCommentHtml(reply_comments[j]);
                   }
                }
               reply_wrap += getReplyHtml(reply,reply_comment,isBest)
            }

            if (page_no==1){
                $('.post-list').html(best_reply_wrap+reply_wrap);
            }else{
                $('.post-list').html(reply_wrap);
            }
            total = data.total;
            page_no=data.page_no;
            total_page = data.total_page;

        },
        error: function(xhr, type) {
        }
    })
}
// click left
$('#left').click(function() {
    if (login_user_id > 0) {
        var data = {};
        data['type'] = 'left';
        data['user_id'] = login_user_id;
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
    if (login_user_id > 0) {
        var data = {};
        data['type'] = 'join';
        data['user_id'] = login_user_id;
        data['community_id'] = community_id;
        $.ajax({
            type: 'POST',
            url: '/user_community',
            data: data,
            dataType: 'json',
            timeout: 5000,
            success: function(data) {
                alert('成功加入社区!');
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
