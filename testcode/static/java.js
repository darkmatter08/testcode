
       
     
  
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
    var name = $( "#name" ),
        email = $( "#email" ),
        password = $( "#password" ),          
        ifAdmin=false;
        
        $('input[name=q1]').click(function(){
            if($(this).val()=="t"){
              ifAdmin=true;
              };             
           } );
        
        allFields = $( [] ).add( name ).add( email ).add( password ),
        tips = $( ".validateTips" );
 
    function updateTips( t ) {
      tips
        .text( t )
        .addClass( "ui-state-highlight" );
      setTimeout(function() {
        tips.removeClass( "ui-state-highlight", 1500 );
      }, 500 );
    }
 
   function checkLength( o, n, min, max ) {
      if ( o.val().length > max || o.val().length < min ) {
        o.addClass( "ui-state-error" );
        updateTips( "Length of " + n + " must be between " +
          min + " and " + max + "." );
        return false;
      } else {
        return true;
      }
    }
 
    function checkRegexp( o, regexp, n ) {
      if ( !( regexp.test( o.val() ) ) ) {
        o.addClass( "ui-state-error" );
        updateTips( n );
        return false;
      } else {
        return true;
      }
    }
    
 
    $( "#dialog-form" ).dialog({
      autoOpen: false,
      height: 395,
      width: 450,
      modal: true,
      buttons: {
        "Create an account": function() {         
          allFields.removeClass( "ui-state-error" );

          $.post(
           "api/signup",
           {
                      name:name.val(),
                      email:email.val(),
                      password:password.val(),
                      ifAdmin:ifAdmin,
           },
           function(data){
                     var result = jQuery.parseJSON(data)
                     var status = result.isOkay
                     var message = result.message
                     if (status)
                        {
                        color = "red";
                                 
                        }
                    else
                       { color = "green"
                        setTimeout(function(){$("#dialog-form").dialog( "close" )},300);
                        //$(".alert").alert(message);
                        }
                   $("#signup_message_box").html("<span style='color:"+color+"'>"+message+"</span>")
           }
           
          )
          $( this ).dialog( "close" );          
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
        $( "#dialog-form" ).dialog( "open" );
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
   $(function ()
     {
      $( "#logout" )
      .button()
      .click(function() {
        $.post ("api/logout")
      });
     });
  
   $(function() { 

  var email = $( "#emaillogin" ),
      password = $( "#passwordlogin" ),
      allFields = $( [] ).add( email ).add( password ),
      tips = $( ".validateTips" );
 
 
    $( "#dialog-form1" ).dialog({
      autoOpen: false,
      height: 275,
      width: 450,
      modal: true,
      buttons: {
        "Login": function() {
         
          $.post(
           "api/login",
           {
                      email:email.val(),
                      password:password.val(),                  
           },
           function(data){
                     var result = jQuery.parseJSON(data)
                     var status = result.isOkay
                     var message = result.message
                     if (status == false)
                        {
                        color = "red";
                                 
                        }
                   
                   $("#login_message_box").html("<span style='color:"+color+"'>"+message+"</span>")
           }
           
          )
          
            $( this ).dialog( "close" );
          
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
  
  
   $(function() { 
  var name = $( "#nameclass" ),
      password = $( "#passwordclass" ),
      allFields = $( [] ).add( name ).add( password ),
      tips = $( ".validateTips" );
 

  
 
    $( "#dialog-formclass" ).dialog({
      autoOpen: false,
      height: 255,
      width: 450,
      modal: true,
      buttons: {
        "Create a class": function() {
         
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
 
    $( "#create-class" )
      .button()
      .click(function() {
        $( "#dialog-formclass" ).dialog( "open" );
      });

   }); 
  
  
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* Add class */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
  
  
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
  
  
