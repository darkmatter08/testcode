
       
     
  
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
      height: 350,
      width: 450,
      modal: true,
      buttons: {
        "Create an account": function() {         
          allFields.removeClass( "ui-state-error" );

          $.post(
           "lib/signup.php",
           {
                      name:name.val(),
                      mail:email.val(),
                      pass:password.val()
           },
           function(data){
                     var result = jQuery.parseJSON(data)
                     alert(result.message)
                      //alert(data);
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
  
  
   $(function() { 

  var email = $( "#emaillogin" ),
      password = $( "#passwordlogin" ),
      allFields = $( [] ).add( email ).add( password ),
      tips = $( ".validateTips" );
 
 
    $( "#dialog-form1" ).dialog({
      autoOpen: false,
      height: 255,
      width: 450,
      modal: true,
      buttons: {
        "Login": function() {
         
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
 
    $( "#login-user" )
      .button()
      .click(function() {
        $( "#dialog-form1" ).dialog( "open" );
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

  
  
  
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* Add class */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
    /* /////////////////// */
  
  

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
  
  
