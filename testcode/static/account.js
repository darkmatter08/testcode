$(function() {
    var name = $( "#name" )
    var  email = $( "#email" )
    var  newpassword = $( "#passwordn" )
    var  curpassword = $( "#password" )
          allFields = $( [] ).add( name ).add( email ).add( newpassword ).add( curpassword )

    $("#account_message_box").html(" ")  
    
 
    $( "#account1" ).dialog({
      autoOpen: false,
      height: 400,
      show: 'fade',
      hide: 'fade',
      width: 450,
      modal: true,
      buttons: {
        "Save changes": function() {         
          allFields.removeClass( "ui-state-error" );            
   
          $.post('/testcode/api/account',
                      {
                      name:name.val(),
                      email:email.val(),
                      new_password:newpassword.val(),
                      old_password:curpassword.val()
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
                        setTimeout(function(){$("#account1").dialog( "close" )},400);
                        //$(".alert").alert(message);
                        }
                   $("#account_message_box").html("<span style='color:"+color+"'>"+message+"</span>")
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
 
    $( "#account" )
      .button()
      .click(function() {
         $.post('/testcode/api/account',                      
           function(data){                    
                     var result = jQuery.parseJSON(JSON.stringify(data))
                     var name = result.name
                     var email = result.email                     
                     $("#email").val(email);
                     $("#name").val(name);                   
           }
                   
          )
        $("#account1").dialog('open');
      });

  
    });