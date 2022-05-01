function isClick(btn_id) {
       console.log(btn_id);
        var elem = document.getElementById(btn_id);
        elem.classList.toggle("act")
      // Инициализировать новый запрос
          const request = new XMLHttpRequest();
        //document.querySelector('#currency').value;
          request.open('POST', '/btn_like_click');
          // Функция обратного вызова, когда запрос завершен
          request.onload = () => {
              // Извлечение данных JSON из запроса
              const data = JSON.parse(request.responseText);
              if (data["like"]) {
              console.log(data["like"]);
              elem.classList.add('act');
              }
              else {
              elem.classList.remove('act');
              }
          }
          // Добавить данные для отправки с запросом
          const data = new FormData();
          data.append('like_btn_id', btn_id);
          // Послать запрос
          request.send(data);
         return false;
};

$(function() {
    $('div.wrapper').click(function(e) {
        e.preventDefault();
        $('#image-modal .modal-body img').attr('src', $(this).find('img').attr('src'));
        $("#image-modal").modal('show');
    });
    $('#image-modal .modal-body img').on('click', function() {
        $("#image-modal").modal('hide');
    });
   var elements = document.querySelectorAll('.nav-item');
   for (var i = 0; i < elements.length; i++) {
        elements[i].classList.remove("active");
    }
    document.querySelector('#profile').classList.add("active");
});
$(document).ready(function() {
    $('#file').on('input', function() {
        var file = this.files[0];
        var fReader = new FileReader();
        var path = "";
        fReader.readAsDataURL(file);
        fReader.onloadend = function(event){
            path = event.target.result;
        }
        var formData = new FormData();
        formData.append("avatar_upload", file);

        $("#progressbar")[0].innerHTML = '<div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width: 75%"></div></div>';
        document.getElementById("modal_img_id").style.visibility = "hidden";
        $("#image-modal").modal('show');
        $.ajax({
               url : '/avatar_upload',
               type : 'POST',
               data : formData,
               processData: false,  // tell jQuery not to process the data
               contentType: false,  // tell jQuery not to set contentType
               success : function(data) {
                   console.log(data["success"]);
                   $("#progressbar")[0].innerHTML = "";
                   document.getElementById("modal_img_id").style.visibility = "visible";
                    $("#image-modal").modal('hide');
                   if (data["success"]){
                        var img = document.getElementById("avatar");
                        img.src = path;
                   }
                   else {
                   alert("Ошибка загрузки");
                   }

               }
        });

    });
});
$(document).ready(function(){
    $(this).scrollTop(0);
});
function subscribeFunc(user_id) {
       var elem = document.getElementById("subbtn");
       if (elem.classList.contains("subscribe")) {
       elem.innerHTML = "Подписаться";
       const request = new XMLHttpRequest();
       request.open('POST', '/subscribe_user');
       request.onload = () => {
           const data = JSON.parse(request.responseText);
       }
       const data = new FormData();
       data.append('user_id', user_id);
       request.send(data);
       }
       else {
       elem.innerHTML = "Отменить подписку";
       const request = new XMLHttpRequest();
       request.open('POST', '/subscribe_user');
       request.onload = () => {
           const data = JSON.parse(request.responseText);
       }
       const data = new FormData();
       data.append('user_id', user_id);
       request.send(data);
       }
       elem.classList.toggle("subscribe");
       elem.classList.toggle("btnvio");
       return false;
};