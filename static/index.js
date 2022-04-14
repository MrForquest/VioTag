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

$(document).ready(function(){
    $(this).scrollTop(0);
});

$(function() {
   var elements = document.querySelectorAll('.nav-item');
   for (var i = 0; i < elements.length; i++) {
        elements[i].classList.remove("active");
    }
   document.querySelector('#main').classList.add("active");
});