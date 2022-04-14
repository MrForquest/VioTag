$(function() {
        let arr = [];

	$( "#search_tag" ).autocomplete({
		source: arr,
		minLength: 1
		}
	);
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

$(document).on("click", ".tag", function () {
      this.remove();
});

function resizeInput() {
    var input = document.querySelector('#search_tag');
     var container = document.querySelector('#searchcon');
  container.style.width = input.value.length + 3 + "ch";
}

function getTags() {
    var elements = document.querySelectorAll('.tag');
    let names = [];
     console.log(elements);
    for (var i = 0; i < elements.length; i++) {
        names.push(elements[i].innerHTML);
    }
    $('#tags').val(names.join(";"));
    console.log(names);
}

$(document).ready(function() {
    var $element = $('#pic');
    $('#img').on('input', function() {
        var fReader = new FileReader();
        fReader.readAsDataURL(this.files[0]);
        fReader.onloadend = function(event){
        var img = document.getElementById("pic");
        img.src = event.target.result;
        }
    });
});
