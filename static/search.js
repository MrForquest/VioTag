$(function() {
        let arr = [];
	$( "#search_tag" ).on("change paste keyup input",
	function () {
         arr.length = 0;
          var value = this.value;
                var jqxhr = $.getJSON( "http://127.0.0.1:5000/relevant_tags",{name_tag: value}, function(data) {
                    for (var i = 0; i < data.length; i++) {
                           arr.push(data[i].tag[0].name);
                            }
                            console.log(arr);
        });

    	if  ($('#search_tag').val().length > 2) {
                     $('.add_img').removeClass('disabled');
                   }
                   else {
                     $('.add_img').addClass('disabled');
                   }
        }
	);
});
$(function () {
      $('#search_tag').on('input', function () { $('.hidden_span').text($('#search_tag').val()+"brave");
            if  ($('#search_tag').val().length > 2) {
              $('.add_img').removeClass('disabled');
            }
            else {
              $('.add_img').addClass('disabled');
            }
      });
});
$(function () {
      $('.add_img').click(function () {
      if  ($('#search_tag').val().length > 2) {
       $('#flex_search').after('<div class="p-2 tag">' + $('#search_tag').val() + '</div>')
       $('#search_tag').val("");
       $('.add_img').addClass('disabled');
       console.log("click");
      }
      getTags();
      });
});

$(document).on("click", "#list .tag", function () {
      this.remove();
});

function resizeInput() {
    var input = document.querySelector('#search_tag');
     var container = document.querySelector('#searchcon');
  container.style.width = input.value.length + 3 + "ch";
}

function getTags() {
    var elements = document.querySelectorAll('#list .tag');
    let names = [];
     console.log(elements);
    for (var i = 0; i < elements.length; i++) {
        names.push(elements[i].innerHTML);
    }
    $('#tags').val(names.join(";"));
    console.log(names);
}

$(function() {
   var elements = document.querySelectorAll('.nav-item');
   for (var i = 0; i < elements.length; i++) {
        elements[i].classList.remove("active");
    }
   document.querySelector('#search_page').classList.add("active");
});
$(function() {
    $('div.wrapper').click(function(e) {
            e.preventDefault();
            $('#image-modal .modal-body img').attr('src', $(this).find('img').attr('src'));
            $("#image-modal").modal('show');
        });
        $('#image-modal .modal-body img').on('click', function() {
            $("#image-modal").modal('hide');
        });
});
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

$(window).scroll();