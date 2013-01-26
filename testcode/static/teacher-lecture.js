 $(document).ready(function(){

 $(function() {
    var name = $( "#problemname" ),
      
        
        allFields = $( [] ).add( problemname )

 $( "#dialog-formproblem" ).dialog({
      autoOpen: false,
      height: 220,
      width: 450,
      modal: true,
      buttons: {
          "Create and start editing": function() {         
          allFields.removeClass( "ui-state-error" );        
           
                 
          $.post('/api/createproblem',
                      {
                      name:name.val(),
                      
                      },
           function(data){                    
                     var result = jQuery.parseJSON(JSON.stringify(data))
                     var isOkay = result.isOkay
                     var error = result.error                     
                     var id= result.course_id
                     if (isOkay==false)
                        {
                        color = "red";
                                 
                        }
                    else
                       { color = "green"
                        
                        setTimeout(function()
                        {
                        
                          $("#dialog-formclass").dialog( "close" )
                          $("#shit").remove();
                          $("#classlist").prepend("<li id="+id+" class='classlinks'><a href='#''>"+name+"</a></li>");
                          $("#problemstable").prepend("<tr><td> 0 lectures</td><td >0 problems</td><td >0 students</td></tr>")


                        },600);
                            
                        }
                   $("#problem_message_box").html("<span style='color:"+color+"'>"+error+"</span>")
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
 
    $( "#create-problem" )
      .button()
      .click(function() {
        $( "#dialog-formproblem" ).dialog( "open" );
      });

  
    });

var problemid;
 $(function() 
{

$(document).on("click",".problemlinks",function(){
              problem_id=$(this).attr('id'); 
              $("#latest").hide("slide", { direction: "up" }, 500);
               setTimeout(function(){            
                    
                     $("#latest").html('<div class="classe">'+                    
                           '<div class="margins"> Problem 4 </div> '+ 
                          ' </div> '+ 
                            ' <div class="fields"> Description  <p class="errormesage" id="desc"> </p></div>     '+                
                          ' <div id="problemdescription"> <form><textarea id="description1" name="description" cols="98" rows="10" style="background-color: #FFF; font-size:14px"></textarea> </form> </div>'+ 
                        ' <div class=" marginbottom"> <div class="btn-group in forsave"><button class="btn" type="button" id="savedescription"><i class="icon-ok-circle"></i> Save</button></div> </div>'+ 
                         '   <div class="fields "> Test case 1 </div>'+ 
                         '   <div class="casebigbox"> '+ 
                        '       <div class="inputtest"> '+                           
                         '        <p class="indents"> Input </p>'+ 
                           '       <form><textarea id="inputtext" name="inputtext" cols="45" rows="10" style="background-color: #FFF; font-size:14px"></textarea> </form> '+ 
                           '     </div> '+ 
                           '     <div class="outputtest"> '+ 
                           '    <p class="indents">  Output</p>'+ 
                            '    <form><textarea id="outputtext" name="outputtext" cols="45" rows="10" style="background-color: #FFF; font-size:14px"></textarea> </form> <div class="btn-group in forsave"><button class="btn savetestcase" type="button" id="1"><i class="icon-ok-circle"></i> Save</button></div></div>'+ 
                           '    </div>'+ 
                           '   <div class=" marginbottom"> <div class="btn-group in"><button class="btn" type="button" id="testcase"><i class="icon-tasks"></i> Add a new test case</button></div> </div>')
          
                   $("#latest").show("slide", { direction: "up" }, 600)},600);
          }

 )} );

    var i=1;


$(document).on("click","#testcase",function(){

  i=i+1;
  $("#testcase").remove();
  $("#latest").append('   <div class="fields "> Test case '+i+' <p class="errormesage"> </p></div>'+ 
                         '   <div class="casebigbox"> '+ 
                        '       <div class="inputtest"> '+                           
                         '        <p class="indents"> Input </p>'+ 
                           '       <form><textarea id="inputtext" name="inputtext" cols="45" rows="10" style="background-color: #FFF; font-size:14px"></textarea> </form> '+ 
                           '     </div> '+ 
                           '     <div class="outputtest"> '+ 
                           '    <p class="indents">  Output</p>'+ 
                            '    <form><textarea id="outputtext" name="outputtext" cols="45" rows="10" style="background-color: #FFF; font-size:14px"></textarea> </form> <div class="btn-group in forsave"><button class="btn savetestcase" type="button"><i class="icon-ok-circle"></i> Save</button></div></div>'+ 
                           '    </div>'+ 
                           '   <div class=" marginbottom"> <div class="btn-group in"><button class="btn" type="button" id="testcase"><i class="icon-tasks"></i> Add a new test case</button></div> </div>')
     })

$(document).on("click",".savedescription",function(){}


  )






});


