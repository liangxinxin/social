function initData(){
    $('.friend-listli:first').addClass('active');
    getLoginInfo();
    getHistoryMessage(to_user_id);

}

function makeMineHtml(message){
    var user = message.user;
    var user_html = '<li class="chat-mine">\
                        <div class="chat-user"><img src="'+user.head_img_url+'" /></div>\
                        <div class="chat-content">'+message.content+'\
                        </div>\
                    </li>';
    return user_html;
}
function makeChaterhtml(message){
    var chat_html ='<li>\
                        <div class="chat-user"><img src="'+message.user.head_img_url+'"/></div>\
                        <div class="chat-content">'+message.content+'\
                        </div>\
                    </li>';
    return chat_html;

}
$('#send').click(function(){
    var content =$('#smile-editor').html(); //$('#editor').html();
    if(content==''){
        alert('发送内容不能为空！')
        return;
    }
    to_user_id = $('#chatWith').val()
    var data= {}
    data['type'] ='send';
    data['to_user_id'] = to_user_id;
    data['content'] = content;
    $.ajax({
        url:'/save_message',
        type:'POST',
        data:data,
        dataType: 'json',
        timeout: 5000,
        success:function(data){
            if(data.result.code==0){
                message=data.result.data;
                $('div.chat>div.container-scroll>ul').append(makeMineHtml(message));
                $("div.container-scroll").scrollTop($("div.container-scroll")[0].scrollHeight);
                $('#smile-editor').empty();
            }else{
                alert('发送失败')
            }

        },
        error:function(data){
                alert('发送失败')
        }
    })
})

function getHistoryMessage(to_user_id){
    $(".friend-list>li").removeClass('active');
    $('.friend-list>li#u_'+to_user_id).addClass('active');
    $('#chatWith').val(to_user_id);
    $('.friend-list>li#u_'+to_user_id).find('span.circle_sm').remove();
    var data = {}
    data['type']='history_message';
    data['to_user_id'] = to_user_id;
    $.ajax({
        url:'/get_history_message',
        type:'get',
        data:data,
        dataType: 'json',
        timeout: 5000,
        success:function(data){
            var new_message='';
            var mess_list= data.result;
            if(mess_list.length>0){
                for(var i =0;i<mess_list.length;i++){
                        if(mess_list[i].create_user_id==user_id){
                            new_message+=makeMineHtml(mess_list[i])
                        }else{
                            new_message+=makeChaterhtml(mess_list[i])
                        }
                }
            new_message+='<li style="width:100%; text-align:center;">历史消息</li>';
            }
            $('div.chat>div.container-scroll>ul').empty().html(new_message);
            $("div.container-scroll").scrollTop($("div.container-scroll")[0].scrollHeight+20);
        }
    })
}
(function longPolling() {
   to_user_id = $('#chatWith').val();
   var data= {}
   data['type'] = 'new_message'
   data['create_user_id'] = to_user_id
    $.ajax({
        url: "/get_new_message",
        data: data,
        dataType: "json",
        timeout: 5000,
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if (textStatus == "timeout") { // 请求超时
                    console.log('请求超时')
                }
            },
        success: function (data) {
             message_list=data.result;
             var len = message_list.length
             if(len>0){
                var new_message='';
                for(var i =0;i<message_list.length;i++){
                    new_message+=makeChaterhtml(message_list[i])
                }
                console.log(new_message)
                $('div.chat>div.container-scroll>ul').append(new_message);
               $("div.container-scroll").scrollTop($("div.container-scroll")[0].scrollHeight);
             }
            setTimeout(longPolling, 5000);//5000毫秒，自己定义延迟时间
        }
    });
})();