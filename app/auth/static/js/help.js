$(function() {
          $('a#submit_res').bind('click', function() {
            $.getJSON('/SearchResult', {
              searchbar: $('input[name="searchbar"]').val()
            }, function(data) {
              $("#search_res").show();
              $("#search_res").html("");
              var stringRes = "";

              for(i=0; i<data.size; i++){
                    stringRes += '<div class="panel panel-default bootcards-media" style="width:80%; margin:0 auto;">'+ 
                    '<div class="panel-heading" id="trip_num" align="left">'+data.result1[i]+'</div>'+
                    '<div class="panel-body" id="trip_details">'+ data.result3[i]+'</div>' +
                    '<img src="http://www.linkofphoto.com/path"/>'+
                    '<div class="panel-footer" id="trip_em" align="left" style="display:inline-block;">'+data.result2[i]+'</div>'+
                    '<a href="#" class="btn btn-primary">View Trip</a>'+
                '</div>';  
              }
              $("#search_res").append(stringRes);
              console.log(stringRes);
            });
            return false;
          });
        });

$(document).ready(function() {
            $("#search_res").hide();
        });