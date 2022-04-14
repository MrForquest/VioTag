 function isClick(btn_id) {

       console.log(btn_id);
        var elem = document.getElementById(btn_id);
        elem.classList.toggle("act");

      // Инициализировать новый запрос
          const request = new XMLHttpRequest();
        //document.querySelector('#currency').value;
          request.open('POST', '/btn_click_register');
          // Функция обратного вызова, когда запрос завершен
          request.onload = () => {
              // Извлечение данных JSON из запроса

              const data = JSON.parse(request.responseText);
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
        fReader.readAsDataURL(file);
        fReader.onloadend = function(event){
        var img = document.getElementById("avatar");
        img.src = event.target.result;
        }
        var formData = new FormData();
        formData.append("avatar_upload", file);
        $.ajax({
               url : '/avatar_upload',
               type : 'POST',
               data : formData,
               processData: false,  // tell jQuery not to process the data
               contentType: false,  // tell jQuery not to set contentType
               success : function(data) {
                   console.log(data);
               }
        });
    });
});
$(document).ready(function(){
    $(this).scrollTop(0);
});