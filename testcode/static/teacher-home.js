$(document).ready(function(){
 /*$(function(){ $("#create-lecture").hide() }); */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
  var csrftoken = getCookie('csrftoken');
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
   });


      
$("#homelink" )
      .button()
      .click(function() {
        $.post('/api/userhome'
               );
      });



/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$ CREATE CLASS $$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */

  $(function() {
    var name = $( "#classname" ),
        shortname = $( "#shortclassname" ),
        studentpassword = $( "#studentpassword" ),
        teacherpassword = $( "#teacherpassword" ),
        
        allFields = $( [] ).add( name ).add( shortname ).add( studentpassword ).add( teacherpassword ),
        tips = $( ".validateTips" );
 
    
    
 
    $( "#dialog-formclass" ).dialog({
      autoOpen: false,
      height: 400,
      width: 450,
      modal: true,
      buttons: {
          "Create a class": function() {         
          allFields.removeClass( "ui-state-error" );        
           
                 
          $.post('/api/createcourse',
                      {
                      name:name.val(),
                      short_name:shortname.val(),
                      admin_password:teacherpassword.val(),
                      student_password:studentpassword.val()
                      },
           function(data){                    
                     var result = jQuery.parseJSON(JSON.stringify(data))
                     var isOkay = result.isOkay
                     var error = result.error
                     var name= result.name

                     var id= result.course_id
                     if (isOkay==false)
                        {
                        color = "red";
                                 
                        }
                    else
                       { color = "green"
                        
                        setTimeout(function(){$("#dialog-formclass").dialog( "close" )
                        $("#shit").remove();
                        $("#classlist").prepend("<li id="+id+" class='classlinks'><a href='#''>"+name+"</a></li>");
                        $("#problemstable").prepend("<tr><td> 0 lectures</td><td >0 problems</td><td >0 students</td></tr>")}, 600);
                            
                        }
                   $("#create_message_box").html("<span style='color:"+color+"'>"+error+"</span>")
           },
           "json"
           
          )
                 
        },
        Cancel: function() {
          $( this ).dialog( "close" );
                           }
        },
      close: function() {
        allFields.val( "" ).removeClass( "ui-state-error" );
      }
    });
 
    $( "#create-class" )
      .button()
      .click(function() {
        $( "#dialog-formclass" ).dialog( "open" );
      });

  
    });

var courseid;
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
 $(function() 

     {
     $(document).on("click",".classlinks",function(){
            courseid=$(this).attr('id');         
            $.post('/api/getlectures',
                 {
                  course_id:courseid
                 },
                 function(data){
                   var result = jQuery.parseJSON(JSON.stringify(data))
                   var number= result.num_lectures;
                   var lecture_name= result.lecture_name;
                   var lecture_id=result.lecture_id;    
                   $("#latest").hide("slide", { direction: "up" }, 500);
                    setTimeout(
                      function(){
                        $("#latest").html(' <div class="classe"><div class="margins"> Lectures </div> <div class="btn-group in rightm"> <button class="btn " type="button" id="create-lecture"> <i class="icon-pencil"></i> Create a lecture</button> </div> </div> <div id="forerror"> </div> </ul><span style="-webkit-column-count:3"><ul class="nav nav-tabs nav-stacked" id="lecturelist"></ul></span>')
                          if (number==0) 
                            {
                                  $("#forerror").html("<p class='empty'> This class has no lectures. You can create one</p>");
                            }  
                   else
                   {                  

                   for (var i = 0; i < number; i++) 
                    {

                      $("#lecturelist").append("<li ><a href='edit/"+lecture_id[i]+"'>"+lecture_name[i]+"</a></li>");
                    }
                  }
                   $("#latest").show("slide", { direction: "up" }, 500)},500);
                 }

              )
             }
        )          
     }
  );


/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */

 $(function() {
    var name = $( "#lecturename" ),
         
        allFields = $( [] ).add( lecturename )
        tips = $( ".validateTips" );    
    
 
    $( "#dialog-formlecture" ).dialog({
      autoOpen: false,
      height: 220,
      width: 450,
      modal: true,
      buttons: {
          "Create a lecture": function() {         
          allFields.removeClass( "ui-state-error" );                       
          $.post('/api/createlecture',
                      {
                      name:name.val(), 
                      course_id:courseid                   
                      },
           function(data){                    
                     var result = jQuery.parseJSON(JSON.stringify(data))
                     var isOkay = result.isOkay
                     var error = result.error
                     var name= result.name
                     var id= result.lecture_id
                     if (isOkay==false)
                        {
                        color = "red";
                                 
                        }
                    else
                       { color = "green"                        
                        setTimeout(function(){
                              $("#dialog-formlecture").dialog( "close" )
                              $("#forerror").remove();
                              $("#lecturelist").prepend("<li><a href='edit/"+id+"'>"+name+"</a></li>")
                       }, 600)
                            
                        }
                   $("#createlecture_message_box").html("<span style='color:"+color+"'>"+error+"</span>")
           },
           "json"
           
          )
                 
        },
        Cancel: function() {
          $( this ).dialog( "close" );
                           }
        },
      close: function() {
        allFields.val( "" ).removeClass( "ui-state-error" );
      }
    });
 
    $(document).on("click","#create-lecture",function(){
        $( "#dialog-formlecture" ).dialog( "open" );
      });

  
    })




});
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$ ADD CLASS $$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
/* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
   /*
  $(function() {
    var ID = $( "#idclass" ),
        password = $( "#passwordclass" ),
        
        allFields = $( [] ).add(idclass ).add( passwordclass ),
        tips = $( ".validateTips" );
 
    
 
 
    $( "#dialog-formaddclass" ).dialog({
      autoOpen: false,
      height: 300,
      width: 450,
      modal: true,
      buttons: {
          "Add a class": function() {         
          allFields.removeClass( "ui-state-error" );        
           
                 
          $.post('/api/addcourse',
                      {
                      course_id:ID.val(),
                      password:password.val(),
                      },
           function(data){                    
                     var result = jQuery.parseJSON(JSON.stringify(data))
                     var isOkay = result.isOkay
                     var error = result.error
                     var name= result.name
                     var nlectures = 
                     if (isOkay==false)
                        {
                        color = "red";
                                 
                        }
                    else
                       { color = "green"
                        setTimeout(function(){$("#dialog-formclass").dialog( "close" )},400);
                        if ($(".newuser")[0]) 
                             {
                                  $("#listclass").html("<ul class='nav nav-tabs nav-stacked' id='classlist'><li id="+course_id+">"+name+"</li></ul>")
                                  $("#rightclass").html('<table border="0" id="problemstable"><tr><td> 0 lectures</td><td >0 problems</td><td >0 students</td></tr></table>')
                             }
                        else
                            {
                                 $("#classlist").prepend("<li id="+course_id+">"+name+"</li>");
                                 $("#problemstable").prepend("<tr><td> 0 lectures</td><td >0 problems</td><td >0 students</td></tr>");
                            }
                        }
                   $("#create_message_box").html("<span style='color:"+color+"'>"+error+"</span>")
           },
           "json"
           
          )
                 
        },
        Cancel: function() {
          $( this ).dialog( "close" );
                           }
        },
      close: function() {
        allFields.val( "" ).removeClass( "ui-state-error" );
      }
    });
 
    $( "#add-class" )
      .button()
      .click(function() {
        $( "#dialog-formclass" ).dialog( "open" );
      });

  
    });

    */
