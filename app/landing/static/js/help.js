//Search Bar
/*          $('a#submit_res').bind('click', function() {
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
                    '<a href="/view/'+data.result1[i]+'" class="btn btn-primary">View Trip</a>'+
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
        });*/
function return_Result(){
    var res = $('input[name="searchbar"]').val();
    window.location.replace("/main/trip-plans/"+res);
}


//Newest Trips and Most popular
var counter = 1;
var det = true;


function state(tripname, from, to, views){
      return   '<div class="col-sm-3 text-center">'+
                            '<div class="container" style="display:inline; width:100%;">'+
                                '<div class="panel panel-default bootcards-media" style="width:100%;">'+ 
                                    '<div class="panel-heading" align="left" style="width: 100%;">'+tripname+'</div>'+
                                    '<div class="panel-body" style="width: 100%; height: 100%;" align="center">'+
                                    '<img style="height: 100%; width: 100%; object-fit:contain;" src="http://static2.businessinsider.com/image/58d14474d349f92a008b5bee/the-25-most-popular-travel-destinations-in-the-us.jpg"/></div>'+
                                    '<div class="panel-footer" align="left" style="display: inline-block; width: 100%;">'+
                                      '<div class="row">'+
                                            '&nbsp; From:'+from+
                                            '<a href="/main/view/'+tripname+'" target="_blank" class="btn btn-primary" style="float: right;">View Trip</a>'+
                                        '</div>'+
                                        '<div class="row">'+
                                            '&nbsp; To:'+to+
                                            '&nbsp; '+views+' views'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'+ 
                        '</div>';

}

    function res(){
      if(det==true)
           counter++;
      if(counter==1)
          counter++;
        $.getJSON('/main/paginate/1', {
              page: counter
            }, function(data) {
            $("#res").html("");
              var stringRes = "";
              if(data.determiner==false)
                det = false;
              else if(data.determiner==true)
                det = true;

            for(i=0; i<data.size; i++){
                stringRes+=state(data.result1[i], JSON.stringify(data.result2[i]).slice(5,17), JSON.stringify(data.result3[i]).slice(5,17), data.result4[i]);
            }
            $("#res").append(stringRes);
            console.log(counter);
        });
        return false;
    }

    function res_1(){
        if(counter>1)
            counter--;
        $.getJSON('/main/paginate/1', {
              page: counter
            }, function(data) {
            $("#res").html("");
              var stringRes = "";

            if(data.determiner==false)
                det = false;
              else if(data.determiner==true)
                det = true;

            for(i=0; i<data.size; i++){
                stringRes+=state(data.result1[i], JSON.stringify(data.result2[i]).slice(5,17), JSON.stringify(data.result3[i]).slice(5,17), data.result4[i]);
            }
            $("#res").append(stringRes);
            console.log(counter);
            
        });
        return false;
    }


    var counter_1 = 1;
var det_1 = true;

    function res_m(){
      if(det_1==true)
           counter_1++;
      if(counter_1==1)
          counter_1++;
        $.getJSON('/main/paginate/2', {
              page_1: counter_1
            }, function(data) {
            $("#res_1").html("");
              var stringRes = "";
              if(data.determiner==false)
                det_1 = false;
              else if(data.determiner==true)
                det_1 = true;

            for(i=0; i<data.size; i++){
                stringRes+=state(data.result1[i], JSON.stringify(data.result2[i]).slice(5,17), JSON.stringify(data.result3[i]).slice(5,17), data.result4[i]);
            }
            $("#res_1").append(stringRes);
            console.log(counter_1);
        });
        return false;
    }

    function res_1_m(){
        if(counter_1>1)
            counter_1--;
        $.getJSON('/main/paginate/2', {
              page_1: counter_1
            }, function(data) {
            $("#res_1").html("");
              var stringRes = "";

            if(data.determiner==false)
                det_1 = false;
              else if(data.determiner==true)
                det_1 = true;

            for(i=0; i<data.size; i++){
                stringRes+=state(data.result1[i], JSON.stringify(data.result2[i]).slice(5,17), JSON.stringify(data.result3[i]).slice(5,17), data.result4[i]);
            }
            $("#res_1").append(stringRes);
            console.log(counter_1);
            
        });
        return false;
    }

function sendMail(){
      $.getJSON('/main/sendRepsonse', {
              name : $('input[name="resID"]').val(),
              email : $('input[name="resEMAIL"]').val(),
              body : $('textarea[name="resMSG"]').val()
            }, function(data) {
            $('input[name="resID"]').val('');
            $('input[name="resEMAIL"]').val('');
            $('textarea[name="resMSG"]').val('');
            if(data.sent==true){
              swal('Message Sent!');
            }
            else
              swal('An error occured!');
            
        });
        return false;
}