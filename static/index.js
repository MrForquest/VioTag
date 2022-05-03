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
var isViewed = new Map();
var viewCounter = new Map();
$(document).ready(function(){
    $(this).scrollTop(0);
    sec = 0;
    last_post = 0;
    setInterval(tick, 100);
});
$.fn.isInViewport = function() {
    var elementTop = $(this).offset().top;
    var elementBottom = elementTop + $(this).outerHeight();

    var viewportTop = $(window).scrollTop();
    var viewportBottom = viewportTop + $(window).height();

    return elementBottom > viewportTop && elementTop < viewportBottom;
};

function tick() {
sec += 100;
elements = document.querySelectorAll('.card');
for (var i = 0; i < elements.length; i++) {
    var el = $(elements[i]);
    if (isVisible(el)) {
        if (viewCounter.has(el.attr("id"))) {
            viewCounter.set(el.attr("id"), viewCounter.get(el.attr("id")) + 100);
            if (viewCounter.get(el.attr("id")) > 2700) {
                if (isViewed.has(el.attr("id"))) {

                } else {
                 console.log(el.attr("id"));
                 const request = new XMLHttpRequest();
                 request.open('POST', '/view_post');
                 request.onload = () => {
                     const data = JSON.parse(request.responseText);
                 }
                 const data = new FormData();
                 data.append('post_id_viewed', el.attr("id"));
                 request.send(data);
                 isViewed.set(el.attr("id"), true);
                }
            }
        }
        else {
            viewCounter.set(el.attr("id"), 100);
            }
        }
    }

};

$(function() {
   var elements = document.querySelectorAll('.nav-item');
   for (var i = 0; i < elements.length; i++) {
        elements[i].classList.remove("active");
    }
   document.querySelector('#main').classList.add("active");
});

function isVisible(elem) {
    var top_of_element = elem.offset().top;
    var bottom_of_element = elem.offset().top + elem.outerHeight();
    var bottom_of_screen = $(window).scrollTop() + $(window).innerHeight();
    var top_of_screen = $(window).scrollTop();
     //console.log(top_of_element, bottom_of_element, top_of_screen,bottom_of_screen);
    if ((top_of_element > (top_of_screen - 20)) && (bottom_of_element < (bottom_of_screen +  10))){
       return true;
    } else {
       return false;
    }
}
$(window).scroll();
