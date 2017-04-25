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

    this.$avatarView = $("a[href='#photo']") // click this to open upload page
    this.$avatar = this.$avatarView.find('img'); // the old shequ img
    this.$avatarModal = this.$container.find('.modal-body');
    this.$loading = this.$container.find('.loading');
    this.$avatarSave = this.$container.find('#save');
    this.$avatarCancel = this.$container.find('#cancel');
    this.$avatarClose = this.$container.find('a.close');

    this.$avatarForm = this.$avatarModal.find('.avatar-form');
    this.$avatarUpload = this.$avatarForm.find('.avatar-upload');
    this.$avatarSrc = this.$avatarForm.find('.avatar-src');
    this.$avatarData = this.$avatarForm.find('.avatar-data');
    this.$avatarInput = this.$avatarForm.find('.avatar-input');
    this.$avatarBtns = this.$avatarForm.find('.avatar-btns');
    this.$avatarUploadBtn = this.$avatarForm.find('#choose');
    this.$avatarCommendBtn =this.$avatarForm.find("a[href=#m2]");

    this.$avatarWrapper = this.$avatarModal.find('.avatar-wrapper');
    this.$avatarPreview = this.$avatarModal.find('.avatar-preview');
    this.$commendPreview = this.$avatarModal.find('.commend-preview');
    this.$avatarCommendwrapper =this.$avatarModal.find('.photo-list');


    this.$avatarLocalBtn =this.$container.find("a[href=#m1]");
    this.$avatarbody = this.$avatarModal.find('.avatar-body');
    this.isCommendBlock = false;
    this.type = $("input[name=type]").val();
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

      this.$avatarInput.val("")
      this.initTooltip();
      this.initModal();
      this.getDefaultImage();//初始化默认图片
      this.$avatarCommImg =this.$avatarModal.find("#m2>.photo-list>span");//系统推荐图片
      this.addListener();



    },
    uploadImage:function(){
        this.$avatarInput.click();
        this.isCommendBlock = false; //to record the submit is commend or upload
    },
    cleanUpSelected:function(){
        this.$commendPreview.empty().html('');
        this.$avatarCommendwrapper.find('span.active').removeClass('active');
    },
    cleanUploadData:function(){
        this.$avatarWrapper.html("");
        this.$avatarInput.val("");
        this.active = false;
    },
    selected:function(e){
         this.$avatarCommendwrapper.find('span').not($(e.target).parent()).attr("class","");
         $($(e.target).parent()).attr("class","active");
         this.isCommendBlock = true;
         this.cleanUploadData();

    },
    addListener: function () {
      this.$avatarView.on('click', $.proxy(this.click, this));
      this.$avatarInput.on('change', $.proxy(this.change, this));
      this.$avatarSave.on('click', $.proxy(this.submit, this));
      this.$avatarBtns.on('click', $.proxy(this.rotate, this));
      // add by lxx clear image data
       this.$avatarUploadBtn.on('click',$.proxy(this.uploadImage, this));
        this.$avatarCommImg.on('click',$.proxy(this.selected, this));
        this.$avatarCancel.on('click', $.proxy(this.close, this));
        this.$avatarClose.on('click', $.proxy(this.close, this));

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
      this.$avatarModal.find('ul.base-tab>li.active').removeClass('active');
      this.$avatarLocalBtn.click();
      // select the choosen img
      if (url.indexOf('upload') !=-1){
        this.$avatarPreview.empty().html('<img src="' + url + '">');
      }else{
        this.$avatarCommendwrapper.find('span').each(function(){
            if($.trim(url) ==$(this).find('img').attr('src')){
            $(this).addClass('active');
        }
      });
      }

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
     // this.$avatarModal.modal('show');
      this.initPreview();
      //alert('click')

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
        if(this.type=='shequ'){
            data.append('community_id',community_id);
        }
        data.append('type',this.type);//user提交，还是community
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
      if(data.code===0){
       $('#photo').find('.close').click();
       $("a[href='#photo']").find('img').attr('src',data['data']);
       return ;
      }else if(data.code===1){
            alert('上传失败！')
//          $("div.fail").fadeToggle(500);
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
           console.log(data.message);
        }
      } else {
        console.log('Failed to response');
      }
    },

    submitFail: function (msg) {
      console.log(msg);
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
               data.append('isDefault',false);//isDefault :true 使用系统默认的
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
                data.append('isDefault',false);//isDefault :true 使用系统默认的
                this.callback(data);  // 回调base64字符串
            }
        }

    },
    getBase64Image:function (data) {

       var  selectedImage = this.$avatarCommendwrapper.find('span.active>img');
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
               data.append('isDefault',true);//isDefault :true 使用系统默认的
               this.callback(data);	  // 回调base64字符串
        }else{
            img.onload = function() {
                ctx.drawImage(this, 0, 0, this.width, this.height);
                var base64 = canvas.toDataURL('image/jpg', 1);  // 这里的“1”是指的是处理图片的清晰度（0-1）之间，当然越小图片越模糊，处理后的图片大小也就越小
                img.onload = null;
                data.append('image',base64);
                data.append('isDefault',true);//isDefault :true 使用系统默认的
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
                var community_url = $("a[href='#photo']").find('img').attr('src')

                    this.recommendimage =$('.recommend-image');
                    var imgs = [];
                    var res =data.result;
                    for(var i=0;i<res.length;i++){
                        this.image= [
                             '<span >',
                             '<img src="'+res[i].imgsrc+'"/></span>'
                             ].join('');
                        imgs.push(this.image)
                    }

                    $('.photo-list').html(imgs)
                },
                error: function (data) {
                    alert('加载默认图片出错！')
                }
        });
    }
  };

  $(function () {
    return new CropAvatar($('#photo'));
  });

});
