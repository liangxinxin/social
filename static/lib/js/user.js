function initPageData(pageNo,pageSize,totalCount,totalPages){
        if (totalCount>0){
            $('.pagination').twbsPagination({
                startPage: pageNo,
                totalPages: totalPages,
                first: '首页',
                prev: '前一页',
                next: '下一页',
                last: '末页',
                onPageClick: function (evt, page) {

                    if (page == pageNo) {
                        console.debug("current page number clicked, do nothing.");
                        return;
                    }
                    var url = "/user_info_community_join?user_id=" + view_user_id + "&no=" + page + "&size=" + pageSize+"&type=joined";
                    console.debug("pageurl:", url);
                    window.location.href = url;
                }
            });
        }
    }
    function leftCommunity(community_id){
        var data = {};
        data['type'] = 'left';
        data['user_id'] = view_user_id;
        data['community_id'] = community_id;
        $.ajax({
            type: 'POST',
            url: '/user_community',
            data: data,
            dataType: 'json',
            timeout: 5000,
            success: function(data) {
                $('.community').find('#c_'+community_id).remove();
                if( $('.community').html()=='' && pageNo>1){
                    pageNo -=1;
                    var url = "/user_info_community_join?user_id=" + user_id + "&no=" + pageNo + "&size=" + pageSize+"&type=joined";
                    console.debug("pageurl:", url);
                    window.location.href = url;

                }else if($('.community').html()=='' && pageNo==1){
                    $('ul.pagination').empty();
                }
            },
            error: function(xhr, type) {
                alert('离开社区失败!');
            }
        })

    }
    function loadJoinedCommunity(pageno){
        var data = {};
        data['type'] = 'joined';
        data['user_id'] = view_user_id;
        $.ajax({
            type: 'get',
            url: '/community_joined',
            data: data,
            dataType: 'json',
            timeout: 5000,
            success: function(data) {
                var community_list = data.community_list;
                var community_html = '';

                var flag = view_user_id==login_user_id && login_user_id>0;
                for(var i=0;i<community_list.length;i++){
                    community = community_list[i];
                    var left_html =''
                    if(flag){
                        left_html = '<div class="right-control"><a href="javascript:void(0)" onclick="leftCommunity('+community.id+')" class="btn btn-default ">取消加入</a></div>';
                    }

                    community_html += '<div id="c_'+community.id+'" class="item">\
                                <div class="img">\
                                    <a href="#"><img src="'+community.head_img_url+'"></a>\
                               </div>\
                                <div class="content">\
                                    <h4><a href="community?id='+community.id+'&type=query">'+community.name+'岛</a></h4>\
                                    <p>'+community.describe+'</p>\
                                    <div class="block-bar action">\
                                        <div class="row-1x">\
                                            <div class="group-span-1x">\
                                                <span><em>帖子</em><b>'+community.post_num+'</b></span>\
                                                <span><em>成员</em><b>'+community.user_num+'</b></span>\
                                            </div>\
                                        </div>\
                                        '+left_html+'\
                                    </div>\
                                </div>\
                            </div>';
                }
                $('.community').html(community_html)
                pageNo = data['no'];
                pageSize = data['size']
                totalCount  = data['totalCount']
                totalPages = data['totalPages']
                initPageData(pageNo,pageSize,totalCount,totalPages)
            },
            error: function(xhr, type) {
                alert('社区加载失败!');
            }
        })


    }
