(function (factory) {
  if (typeof define === 'function' && define.amd) {
    define(['jquery'], factory);
  } else if (typeof exports === 'object') {
    // Node / CommonJS
    factory(require('jquery'));
  } else {
    factory(jQuery);
  }
})(function ($) {

  'use strict';

  var console = window.console || { log: function () {} };

  function CropAvatar($element) {
    this.$container = $element;

    this.$avatarView = this.$container.find('.avatar-view');
    this.$avatar = this.$avatarView.find('img');
    this.$avatarModal = this.$container.find('#avatar-modal');
    this.$loading = this.$container.find('.loading');

    this.$avatarForm = this.$avatarModal.find('.avatar-form');
    this.$avatarUpload = this.$avatarForm.find('.avatar-upload');
    this.$avatarSrc = this.$avatarForm.find('.avatar-src');
    this.$avatarData = this.$avatarForm.find('.avatar-data');
    this.$avatarInput = this.$avatarForm.find('.avatar-input');
    this.$avatarSave = this.$avatarForm.find('.avatar-save');
    this.$avatarBtns = this.$avatarForm.find('.avatar-btns');

    this.$avatarWrapper = this.$avatarModal.find('.avatar-wrapper');
    this.$avatarPreview = this.$avatarModal.find('.avatar-preview');
    this.$commendPreview = this.$avatarModal.find('.commend-preview');


    this.$avatarCloseBtns = this.$avatarForm.find('.avatar-close');
    this.$avatarUploadBtn = this.$avatarForm.find('#choose');
    this.$avatarCommendBtn =this.$avatarForm.find('#avatar-commend-title');
    this.$avatarLocalBtn =this.$avatarForm.find('#avatar-local-up');
    this.$avatarCommendwrapper =this.$avatarForm.find('.avatar-wrapper-commend');
    this.$avatarbody = this.$avatarModal.find('.avatar-body');
    this.isCommendBlock = false;
    this.type = $("input#type").val();

    this.init();

  }


  CropAvatar.prototype = {
    constructor: CropAvatar,

    support: {
      fileList: !!$('<input type="file">').prop('files'),
      blobURLs: !!window.URL && URL.createObjectURL,
      formData: !!window.FormData
    },

    close:function(){
       this.cleanUploadData();
       this.cleanUpSelected();
    } ,
    init: function () {
      this.support.datauri = this.support.fileList && this.support.blobURLs;
      if (!this.support.formData) {
        this.initIframe();
      }
      this.$avatarLocalBtn.click();
      this.$avatarInput.val("")
      this.initTooltip();
      this.initModal();
      this.getDefaultImage();//初始化默认图片
      this.$avatarCommImg =this.$avatarModal.find(".image-li>a>img");//系统推荐图片
      this.$avatarCommendBtn.css("color","#666");
      this.$avatarLocalBtn.css("color","#317ef3");
      this.addListener();


    },
    uploadImage:function(){

        this.$avatarInput.click();

    },
    getCommend:function(){
        this.$avatarbody.css("display","none");
        this.$avatarCommendwrapper.css("display","block");
        this.$avatarCommendBtn.css("color","#317ef3");
        this.$avatarLocalBtn.css("color","#666");
        this.isCommendBlock = true;
    },
    getLocal:function(){
        this.$avatarbody.css("display","block");
        this.$avatarCommendwrapper.css("display","none");
        this.$avatarCommendBtn.css("color","#666");
        this.$avatarLocalBtn.css("color","#317ef3");
        this.isCommendBlock = false;

    },
    cleanUpSelected:function(){
        this.$commendPreview.empty().html('');
        $("li.image-li *").removeClass("select")
        $("li.image-li *").removeClass("selected-img")
    },
    cleanUploadData:function(){
        this.$avatarWrapper.html("");
        this.$avatarInput.val("");
        this.initPreview();
        this.active = false;
    },
    selected:function(e){
         $("li.image-li *").not(e.target).attr("class","");
         $(e.target).next("span").attr("class","select");
         $(e.target).addClass("selected-img");
         var url = $(e.target).attr("src");
         this.$commendPreview.empty().html('<img src="' + url + '">');
         // 如果有上传图片数据  清除
         this.cleanUploadData();

    },
    addListener: function () {
      this.$avatarView.on('click', $.proxy(this.click, this));
      this.$avatarInput.on('change', $.proxy(this.change, this));
      this.$avatarForm.on('submit', $.proxy(this.submit, this));
      this.$avatarBtns.on('click', $.proxy(this.rotate, this));
      // add by lxx clear image data
       this.$avatarCloseBtns.on('click', $.proxy(this.close, this));
       this.$avatarUploadBtn.on('click',$.proxy(this.uploadImage, this));
       this.$avatarCommendBtn.on('click', $.proxy(this.getCommend, this));
       this.$avatarLocalBtn.on('click', $.proxy(this.getLocal, this));
       this.$avatarCommImg.on('click',$.proxy(this.selected, this));

    },

    initTooltip: function () {
      this.$avatarView.tooltip({
        placement: 'bottom'
      });
    },

    initModal: function () {
      this.$avatarModal.modal({
        show: false
      });
    },

    initPreview: function () {
      var url = this.$avatar.attr('src');
      this.$avatarPreview.empty().html('<img src="' + url + '">');
    },

    initIframe: function () {
      var target = 'upload-iframe-' + (new Date()).getTime(),
          $iframe = $('<iframe>').attr({
            name: target,
            src: ''
          }),
          _this = this;

      // Ready ifrmae
      $iframe.one('load', function () {

        // respond response
        $iframe.on('load', function () {
          var data;

          try {
            data = $(this).contents().find('body').text();
          } catch (e) {
            console.log(e.message);
          }

          if (data) {
            try {
              data = $.parseJSON(data);
            } catch (e) {
              console.log(e.message);
            }

            _this.submitDone(data);
          } else {
            _this.submitFail('Image upload failed!');
          }

          _this.submitEnd();

        });
      });

      this.$iframe = $iframe;
      this.$avatarForm.attr('target', target).after($iframe.hide());
    },

    click: function () {
      this.$avatarModal.modal('show');
      this.initPreview();
      //this.init();
    },

    change: function () {
        this.cleanUpSelected();//清除 选中数据
      var files,
          file;
      if (this.support.datauri) {
        files = this.$avatarInput.prop('files');
        if (files.length > 0) {
          file = files[0];

          if (this.isImageFile(file)) {
            if (this.url) {
                URL.revokeObjectURL(this.url); // Revoke the old one
            }
            this.url = URL.createObjectURL(file);
            this.startCropper();
          }else{
            alert('上传失败！上传图片文件只支持JPG、PNG、GIF')
          }
        }
      } else {
        file = this.$avatarInput.val();

        if (this.isImageFile(file)) {
          this.syncUpload();
        }
      }

    },

    submit: function () {
      if(this.isCommendBlock){
        this.ajaxUpload();
        return false;
      }

      if (!this.$avatarSrc.val() && !this.$avatarInput.val()) {
         alert('请先选择图片')
        return false;
      }

      if (this.support.formData) {
        this.ajaxUpload();
        return false;
      }
    },

    rotate: function (e) {
      var data;

      if (this.active) {
        data = $(e.target).data();

        if (data.method) {
          this.$img.cropper(data.method, data.option);
        }
      }
    },

    isImageFile: function (file) {
      if (file.type) {
        return /^image\/\w+$/.test(file.type);
      } else {
        return /\.(jpg|jpeg|png|gif)$/.test(file);
      }
    },

    startCropper: function () {
      var _this = this;

      if (this.active) {
        this.$img.cropper('replace', this.url);
      } else {
        this.$img = $('<img src="' + this.url + '">');
        this.$avatarWrapper.empty().html(this.$img);
        this.$img.cropper({
          aspectRatio: 1,
          preview: this.$avatarPreview.selector,
          strict: false,
          crop: function (data) {
            var json = [
                  '{"x":' + data.x,
                  '"y":' + data.y,
                  '"height":' + data.height,
                  '"width":' + data.width,
                  '"rotate":' + data.rotate + '}'
                ].join();

            _this.$avatarData.val(json);
          }
        });

        this.active = true;

      }
    },

    stopCropper: function () {
      if (this.active) {
        this.$img.cropper('destroy');
        this.$img.remove();
        this.active = false;
      }
    },
    callback: function(data) {

        var url = this.$avatarForm.attr('action'),
        _this = this;
        if(this.type=='community'){
            data.append('community_id',$("input#type").attr('name'));
        }
        data.append('type',this.type);//user提交，还是community
        console.log(data)
		// 回调后的函数处理
		    $.ajax(url, {
                type: 'post',
                data: data,
                dataType: 'json',
                processData: false,
                contentType: false,
                beforeSend: function () {
                  _this.submitStart();
                },

                success: function (data) {
                  _this.submitDone(data);
                },

                error: function (XMLHttpRequest, textStatus, errorThrown) {
                  _this.submitFail(textStatus || errorThrown);
                },

                complete: function () {
                  _this.submitEnd();
                }
            });
	},
    ajaxUpload:function(){
       var data = new FormData(this.$avatarForm[0]);

        if(this.isCommendBlock){
            this.getBase64Image(data);
      }else{
            data.append('filename',this.$avatarInput.val());
	        var canvasdata = this.$img.cropper("getCanvasData");
	        var cropBoxData = this.$img.cropper('getCropBoxData');
	        this.convertToData(this.url, canvasdata, cropBoxData, data);
      }




    },

    syncUpload: function () {
      this.$avatarSave.click();
    },

    submitStart: function () {
      this.$loading.fadeIn();
    },

    submitDone: function (data) {
      console.log(data);
      if(data.code===0){
        $("div.success").fadeToggle(500,function(){
            $('.avatar-close').click();
            window.location.reload();

        })
        return ;
      }else if(data.code===1){
          $("div.fail").fadeToggle(500);
          return;
      }
      if ($.isPlainObject(data) && data.code === 0) {
        if (data.result) {
          this.url = data.result;

          if (this.support.datauri || this.uploaded) {
            this.uploaded = false;
            this.cropDone();
          } else {
            this.uploaded = true;
            this.$avatarSrc.val(this.url);
            this.startCropper();
          }

          //this.$avatarInput.val('');
        } else if (data.message) {
           alert(data.message);
        }
      } else {
        alert('Failed to response');
      }
    },

    submitFail: function (msg) {
      alert(msg);
    },

    submitEnd: function () {
      this.$loading.fadeOut();
    },

    cropDone: function () {
      this.$avatarForm.get(0).reset();
      this.$avatar.attr('src', this.url);
      this.stopCropper();
      this.$avatarModal.modal('hide');
    },

    alert: function (msg) {
      var $alert = [
            '<div class="alert alert-danger avater-alert">',
              '<button type="button" class="close" data-dismiss="alert">&times;</button>',
              msg,
            '</div>'
          ].join('');

      this.$avatarUpload.after($alert);
    },
    convertToData:function(url, canvasdata, cropdata,data) {
        var cropw = cropdata.width; // 剪切的宽
        var croph = cropdata.height; // 剪切的宽
        var imgw = canvasdata.width; // 图片缩放或则放大后的高
        var imgh = canvasdata.height; // 图片缩放或则放大后的高
        var poleft = canvasdata.left - cropdata.left; // canvas定位图片的左边位置
        var potop = canvasdata.top - cropdata.top; // canvas定位图片的上边位置
        var canvas = document.createElement("canvas");
        var ctx = canvas.getContext('2d');
        canvas.width = cropw;
        canvas.height = croph;
        var img = new Image();
        img.src = url;
        if(img.complete){
                this.width = imgw;
                this.height = imgh;
                    // 这里主要是懂得canvas与图片的裁剪之间的关系位置
                ctx.drawImage(img, poleft, potop, this.width, this.height);
                var base64 = canvas.toDataURL('image/jpg', 1);  // 这里的“1”是指的是处理图片的清晰度（0-1）之间，当然越小图片越模糊，处理后的图片大小也就越小

               data.append('image',base64);
               data.append('isDefault',0);//isDefault :true 使用系统默认的
               this.callback(data)	  // 回调base64字符串
        }else{
            img.onload = function() {
                this.width = imgw;
                this.height = imgh;
                // 这里主要是懂得canvas与图片的裁剪之间的关系位置
                ctx.drawImage(this, poleft, potop, this.width, this.height);
                var base64 = canvas.toDataURL('image/jpg', 1);  // 这里的“1”是指的是处理图片的清晰度（0-1）之间，当然越小图片越模糊，处理后的图片大小也就越小
                img.onload = null;
                data.append('image',base64);
                data.append('isDefault',0);//isDefault :true 使用系统默认的
                this.callback(data);  // 回调base64字符串
            }
        }

    },
    getBase64Image:function (data) {
       var  selectedImage = this.$avatarModal.find('.selected-img');
       if(typeof(selectedImage)=="undefined"){
           alert('请先选择图片');
           return false;
       }
       var imagePath = selectedImage.attr("src");
       var filename = imagePath;
       if(imagePath.indexOf("/")>0)//如果包含有"/"号 从最后一个"/"号+1的位置开始截取字符串
       {
         filename=imagePath.substring(imagePath.lastIndexOf("/")+1,imagePath.length);
       }
        var data = new FormData(this.$avatarForm[0]);
        data.append('filename',filename);
        var canvas = document.createElement("canvas");
        canvas.width = selectedImage.width;
        canvas.height = selectedImage.height;
        var ctx = canvas.getContext("2d");
        //ctx.drawImage(this, 0, 0, selectedImageage.width, selectedImage.height);
        var img = new Image();
        img.src = selectedImage.attr('src');
        if(img.complete){
                ctx.drawImage(img, 0, 0, selectedImage.width, selectedImage.height);
                var base64 = canvas.toDataURL('image/jpg', 1);  // 这里的“1”是指的是处理图片的清晰度（0-1）之间，当然越小图片越模糊，处理后的图片大小也就越小

               data.append('image',base64);
               data.append('isDefault',1);//isDefault :true 使用系统默认的
               this.callback(data);	  // 回调base64字符串
        }else{
            img.onload = function() {
                ctx.drawImage(this, 0, 0, this.width, this.height);
                var base64 = canvas.toDataURL('image/jpg', 1);  // 这里的“1”是指的是处理图片的清晰度（0-1）之间，当然越小图片越模糊，处理后的图片大小也就越小
                img.onload = null;
                data.append('image',base64);
                data.append('isDefault',1);//isDefault :true 使用系统默认的
                this.callback(data);	  // 回调base64字符串
            }
        }

        //callback && callback(data)
        // return dataURL.replace("data:image/png;base64,", "");
    },
    getDefaultImage:function () { //type:user获取人的默认头像，community：社区默认头像
        var url = '/get_default_image?type='+this.type;
        $.ajax(url, {
                type: 'get',
                data: "",
                dataType: 'json',
                async:false,
                processData: false,
                contentType: false,
                success: function (data) {
                    this.recommendimage =$('.recommend-image');
                    var imgs = [];
                    var res =data.result;
                    for(var i=0;i<res.length;i++){
                        this.image= [
                            '<li class="image-li" >',
                              '<a><img src="'+res[i].imgsrc+'"/>',
                              '<span class="no-select"></span>',
                             '</a>',
                             '</li>'
                             ].join('');
                             console.log(this.image)
                        imgs.push(this.image)
                    }
                    $('.recommend-image>ul').empty().html(imgs);
                },
                error: function (data) {
                    alert('加载默认图片出错！')
                }
        });
    }
  };

  $(function () {


return new CropAvatar($('#crop-avatar'));
  });

});
