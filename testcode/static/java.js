
       
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
 

 $(function(){
  $("#homelink" ).click(function() {
        $(location).attr('href', '/api/userhome');
      });
  $("#logout" ).click(function() {
        $(location).attr('href', '/api/logout');
      });

 });
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* SIGN UP */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    
  $(function() {
    var name = $( "#name" )
    var  email = $( "#email" )
    var  password = $( "#password" )
          allFields = $( [] ).add( name ).add( email ).add( password )

    $("#signup_message_box").html(" ")  
    
 
    $( "#dialog-form" ).dialog({
      autoOpen: false,
      height: 400,
      show: 'fade',
      hide: 'fade',
      width: 450,
      modal: true,
      buttons: {
        "Create an account": function() {         
          allFields.removeClass( "ui-state-error" );
            
     var ifAdmin=$("input:radio[name='q1']:checked").val()
                
          $.post('api/signup',
                      {
                      name:name.val(),
                      email:email.val(),
                      password:password.val(),
                      isAdmin:ifAdmin
                      },
           function(data){                    
                     var result = jQuery.parseJSON(JSON.stringify(data))
                     var status = result.isOkay
                     var message = result.error                     
                     if (status==false)
                        {
                        color = "red";
                                 
                        }
                    else
                       { color = "green"
                        setTimeout(function(){$("#dialog-form").dialog( "close" )},400);
                        //$(".alert").alert(message);
                        }
                   $("#signup_message_box").html("<span style='color:"+color+"'>"+message+"</span>")
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
 
    $( "#create-user" )
      .button()
      .click(function() {
        $("#dialog-form").dialog('open');
      });

  
    });
  
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* LOGIN */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
   
  
  
   $(function() { 

  var email = $( "#emaillogin" ),
      password = $( "#passwordlogin" ),
      allFields = $( [] ).add( email ).add( password )

     $("#login_message_box").html(" ")
 
 
    $( "#dialog-form1" ).dialog({
      autoOpen: false,
      height: 275,
      width: 450,
      modal: true,
      show: 'fade',
      hide: 'fade',
      buttons: {
        "Login": function() {
         
          $.post(
           "api/login",
           {
                      email:email.val(),
                      password:password.val(),                  
           },
           function(data){                     
                     var result = jQuery.parseJSON(JSON.stringify(data))
                     var isOkay=result.isOkay;
                     var message = result.error;
                     var url= result.url;
                     if (isOkay == true)
                     {
                      $(location).attr('href',url);
                     }
                     else
                     {
                     color = "red";
                     $("#login_message_box").html("<span style='color:"+color+"'>"+message+"</span>")
                     }
           }
           
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
 
    $( "#login-user" )
      .button()
      .click(function() {
        $( "#dialog-form1" ).dialog( "open" );
      });

 }); 
  
  
  
  
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* Create class */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
  

    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* Add class */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
  
  /*
   $(function() { 
  var name = $( "#idlass" ),
      password = $( "#passwordclass1" ),
      allFields = $( [] ).add( name ).add( password ),
      tips = $( ".validateTips" ); 

 
    $( "#dialog-formaddclass" ).dialog({
      autoOpen: false,
      height: 255,
      width: 450,
      modal: true,
      buttons: {
        "Add class": function() {
         
          var bValid = true;        
           if ( bValid ) {      
                      
          
            $( this ).dialog( "close" );
          }
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
        $( "#dialog-formaddclass" ).dialog( "open" );
      });
  });
  
  */
