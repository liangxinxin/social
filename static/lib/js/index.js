//初始化页面
var callback = function(page_no){
   loadHotPost(page_no)
}
function initData(){
    getLoginInfo();
    $("#page").initPage(num_perpage,total,page_no,callback);
    loadHotCommunity();
}
function loadHotPost(page_no){
    var data = {};
    data['type'] = 'hot';
    data['page_no'] = page_no;
    data['num_perpage'] = num_perpage;
    $.ajax({
        type: 'GET',
        url: '/get_hot_post',
        data: data,
        dataType: 'json',
        timeout: 5000,
        success: function(data) {
            var post_list = data.post_list;
            total = data.total;
            if(post_list.length>0){
                var hot_post_wrap ='';
                for(var i =0 ; i<post_list.length;i++){
                    var user = post_list[i].user
                    var community = post_list[i].community
                    hot_post_wrap+='<div class="item">\
                            <div class="photo">\
                                <a href="/user_info_post?type=1&user_id='+user.id+'"><img src="'+user.head_img_url+'"></a>\
                            </div>\
                            <div class="content">\
                                <h4><a href="post?id='+post_list[i].id+'&type=postInfo">'+post_list[i].title+'</a></h4>\
                                <p>'+post_list[i].content+'</p>\
                                <div class="block-bar">\
                                    <span><a href="/user_info_post?type=1&user_id='+user.id+'">'+user.name+'</a></span>\
                                    <div class="control-right">\
                                        <div class="row-1x">\
                                            <div class="group-span-1x">\
                                            <span>'+post_list[i].create_time+'</span><span>来自：<a href="/community?id='+community.id+'&type=query">'+community.name+'</a></span><span><a href="#"><em>评论</em></a><b>'+post_list[i].floor_num+'</b></span>\
                                            </div>\
                                        </div>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>';

                }
                $('.post-list').html(hot_post_wrap);
            }
        },
        error: function(xhr, type) {
            alert('加载失败!');
        }
    })
}

function loadHotCommunity(){
    var data = {}
    data['type'] = 'commend_community';
    $.ajax({
        type: 'get',
        url: '/get_hot_community',
        data: data,
        dataType: 'json',
        timeout: 5000,
        async:false,
        success: function(data) {
            commend_list = data.commend_list
            var commend_wrap ='';
            for(var i=0;i<commend_list.length;i++){
                community = commend_list[i]
                commend_wrap =commend_wrap+'<div class="community-block">\
                                       <div class="img"><img src="'+community.head_img_url+'"></div>\
                                       <div class="content">\
                                           <h4><a href="community?id='+community.id+'&type=query">'+community.name+'</a></h4>\
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