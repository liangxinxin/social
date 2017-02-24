
$('.say_word').hover(function() {
		$(this).addClass('say_word_border');
      },function(){
        $(this).removeClass('say_word_border');
      });
      function sayWrapFocus(replyid){
        var say_block = $('#say_block_'+replyid)
        say_block.find('div.say_wrap').addClass('say_word_border');
      }
      function sayWrapBlur(replyid){
        var say_block = $('#say_block_'+replyid)
        say_block.find('div.say_wrap').removeClass('say_word_border');
      }

    function huifu(replyid,commentid,userid){
       if(login){
          var say_block = $('#say_block_'+replyid)
          say_block.slideDown("fast",function(){
             var comment_wrap = $('.comment_wrap_'+commentid);
             var say_block = $('#say_block_'+replyid);
             var user = comment_wrap.find('div.comment-content').find('a.username');
             var username=user.html();
             // publish something to reply or comment.
             say_block.find('input.pubtype').val('comment');
             say_block.find('input.cuid').val(userid);
             var input_comm = '<input class="cid" type="hidden" value="'+commentid+'">';
             say_block.append(input_comm);
             say_block.find('.say_content').val('回复'+username+':');
             say_block.find('.say_content').focus();
             //$("div[id^='say_block']:not(div#say_block_"+replyid+")").slideUp("fast",function(){});
          });
        }else{
            alert('请登录后回复！')
        }


    }


      //日期格式化
      function getDate(convertDate) {
          var date = new Date(convertDate);
          Y = date.getFullYear() + '-';
          M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date
                  .getMonth() + 1)
                  + '-';
          D = date.getDate() <10 ? '0' + date.getDate()+' ' : date.getDate()+' ';
          h = date.getHours() < 10 ? '0' + date.getHours() + ':' : date
                  .getHours()
                  + ':';
          m = date.getMinutes() < 10 ? '0' + date.getMinutes() + ':' : date
                  .getMinutes()
                  + ':';
          s = date.getSeconds() < 10 ? '0' + date.getSeconds() : date
                  .getSeconds();
          return Y + M + D + h + m + s;
      }



      //click say
      function sayWord(replyid){

        if(login){
          var say_block = $('#say_block_'+replyid)
          say_block.slideToggle("fast",function(){
            //清除回复框中的内容
            var say_content = say_block.find('.say_content');
            say_content.val('');
            say_content.focus();
            var publishType = say_block.find('input.pub_type');
            publishType.val('reply');
           // $("div[id^='say_block']:not(div#say_block_"+replyid+")").slideUp("fast",function(){});
          });
        }else{
            alert('请登录后回复!');
        }
      }
      function joinHtml(comment,replyid){
          var create_time =getDate(comment.create_time)
          var user = comment.user;
          var touser = comment.user
          var content =comment.content;
          if(comment.parent_id>0){
            content='<span>回复<a href="#">'+touser.name+'</a></span>：'+comment.content;
          }
          var comment= ['<div class="comment_wrap comment_wrap_'+comment.id+' col-sm-12">',
              '<div class="comment-head-img">',
              '<a href="/user_info?user_id='+user.id+'"><img class="comm-img-ss" src="'+user.head_img_url+'"></a>',
              '</div>',
                '<div class="comment-content"><a class="username" href="/user_info?user_id='+user.id+'">'+user.name+'</a><span>&nbsp;:&nbsp;</span>',
                content,
                '</div>',
                '<div class="comment-foot"><span class="col-sm-11">'+create_time+'</span>',
                '<a href="javascript:void(0)" onclick="huifu('+replyid+','+comment.id+','+user.id+')">回复</a>',
                '</div></div>'
               ].join('');
          return comment;
      }
      //提交回复
       function  publishComment(replyid){
          if(!login){
            alert('请登录后回复!')
            return false;
          }
          var community_id = $('input#community_id').val();
          alert(community_id)
          var post_id = $('input#post_id').val();
          var say_block = $('#say_block_'+replyid)
          var content = say_block.find('.say_content').val().replace(/(^\s*)|(\s*$)/g, "");;
          var parentid = 0 ;
          var touid = 0;
          if(content==''|| content==null){
              alert('内容不能为空!');
              return false;
          }
          var indexOf = content.indexOf(':');
          if(indexOf!=-1){
            content = content.substring(indexOf+1,content.length);
            var publishType = say_block.find('input.pubtype').val();
            if(publishType=='comment'){
              parentid = say_block.find('input.cid').val(); //comment id
              touid = say_block.find('input.cuid').val();//to comment user id
            }
          }else{
            touid = say_block.find('input.ruid').val(); // to reply user id
          }
           var url='/publish_comment?replyid='+replyid+'&touid='+touid+'&content='+content+'&parentid='+parentid+'&communityid='+community_id+'&postid='+post_id;
            console.log('url'+url)
             $.ajax(url,{
                type: 'post',
                data: '',
                async:false,
                dataType: 'json',
                success:function (data) {
                  if(data.code==0){
                      comment = joinHtml(data.comment,replyid)
                      $('.comment_body_'+replyid).find('div.comment_container').append(comment);
                      $('.say_content').val('');
                      var num = parseInt($('#comment_num_'+replyid).text());
                      $('#comment_num_'+replyid).text((num+1));
                      $('.say_content').val('');
                  }else{
                      alert('回复失败')
                  }
                },
                error: function (data) {
                  alert('error')
                }
          });
      }
      //查询回复信息
      function getComment(replyid){
          var is_show = $('.comment_body_'+replyid).css('display');
          if(is_show=='block'){
              $('.comment_body_'+replyid).slideUp('500');
              return;
          }
          var page_no=1;
          $('.comment_body_'+replyid).find('.comment_container').html('');
         var length = sendAjax(replyid,page_no);
         if(!login){
            $("div[id^='say_block']").css('display','none');//未登录时不显示 输入框。
         }
         if(login || length>0){
           $('.comment_body_'+replyid).slideDown('fast');
         }

      }

      function more_comment(replyid,page_no){
           $('.comment_body_'+replyid).find('div.more_comment').remove();
           var page_no =page_no+1;
           sendAjax(replyid,page_no);

      }
      function sendAjax(replyid,page_no){
           var url='/get_comment?replyid='+replyid+'&page_no='+page_no;
           var datalen = 0;
           $.ajax(url,{
              type: 'get',
              data: '',
              async:false,
              dataType: 'json',
              success:function (data) {
                  var res =data.result;
                  if(res.length==0 ){
                      return ;
                  }
                  var comments = [];
                  for(var i=0;i<res.length;i++){
                      comment = joinHtml(res[i],replyid);
                      comments.push(comment);
                  }
                  $('.say_content').val('');
                  $('.comment_body_'+replyid).find('div.comment_container').append(comments);

                  if(data.has_next){
                      var more = $('.comment_body_'+replyid).find('div.more_comment')
                      if(typeof(more)!='undefined'){
                         more.remove();
                      }
                      var more ='<div class="more_comment col-sm-3"><a href="javascript:void(0)" onclick="more_comment('+replyid+','+page_no+')"><span id=more_'+replyid+'>查看更多</span></a></div>'
                      $('.comment_body_'+replyid).find('div.comment_container').after(more);
                  }
                  datalen = res.length;
                },
                error: function (data) {
                    alert('error')
                }
        });
        return datalen;
      }