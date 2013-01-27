 $(document).ready(function(){

 $(function() {
    var name;
    
    lectureid=$(".lectureelement").attr('id');  
        
        allFields = $( [] ).add( problemname )

 $( "#dialog-formproblem" ).dialog({
      autoOpen: false,
      height: 220,
      width: 450,
      modal: true,
      buttons: {
          "Create and start editing": function() {         
          allFields.removeClass( "ui-state-error" );      
           name=$( "#problemname" ).val();
          
          $.post('/api/createproblem',
                      {
                      problem_name:name,
                      lecture_id:lectureid
                      },
           function(data){                    
                     var result = jQuery.parseJSON(JSON.stringify(data))
                     var isOkay = result.isOkay
                     var error = result.error                     
                     var id= result.problem_id
                     if (isOkay==false)
                        {
                        color = "red";
                                 
                        }
                    else
                       { color = "green"
                        
                        setTimeout(function()
                        {
                        
                          $("#dialog-formproblem").dialog( "close" )
                          $("#shit").remove();
                          $("#problemlist").prepend("<li id="+id+" class='problemlinks'><a href='#''>"+name+"</a></li>");
                          $("#problemstable").prepend(' <tr>'+                                 
                                 '<td> <div class="btn-group in rightm">'+       
                            '<button class="btn viewsubmissions " type="button higher" id="'+id+'"> <i class="icon-signal"></i> View students\' performance</button> </div></td></tr>')
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


 $(function() 
{
var i;
var problem_id;
$(document).on("click",".problemlinks",function(){
              
              $(".active").eq(1).removeClass("active");
              $(this).addClass("active");
              problem_id=$(this).attr('id'); 
              var name
              var description                   
              var testinput
              var testoutput
              var num_testcases
            $.post( '/api/getproblemteacher',
                      {
                        problem_id:problem_id                        
                      },
                    function(data){
                       var result = jQuery.parseJSON(JSON.stringify(data));
                       name=result.name;
                       description=result.problem_description;                       
                       testinput=result.testcase_input;
                       testoutput=result.testcase_output;                    

                       num_testcases=testinput.length;
                       
                    },

                    "json"
                ); 
              $("#latest").hide("slide", { direction: "up" }, 500);
               setTimeout(function(){            
                    
                     $("#latest").html('<div class="classe">'+                    
                           '<div class="margins">'+name+' </div> '+ 
                          ' </div> '+ 
                            ' <div class="fields1"> Description  <span class="errormesage" id="desc" style="font-size:13px"> </span></div>     '+                
                          ' <div id="problemdescription"> <form><textarea id="description1" name="description" rows="10" style="background-color: #FFF; font-size:14px"></textarea> </form> </div>'+ 
                        ' <div class=" marginbottom"> <div class="btn-group in forsave"><button class="btn" type="button" id="savedescription"><i class="icon-ok-circle"></i> Save</button></div> </div>')
                     $("#description1").val(description);
                     for (var j=1; j<(num_testcases+1); j++)
                     {
                        $("#latest").append( '   <div class="fields "> Test case '+j+' <span class="terrormessage" style="font-size:13px"> </span> </div>'+ 
                         '   <div class="casebigbox"> '+ 
                        '       <div class="inputtest"> '+                           
                         '        <p class="indents"> Input </p>  '+ 
                           '       <form><textarea class="inputtext" name="inputtext"  rows="10" style="background-color: #FFF; font-size:14px"></textarea> </form> '+ 
                           '     </div> '+ 
                           '     <div class="outputtest"> '+ 
                           '    <p class="indents">  Output</p>'+ 
                            '    <form><textarea class="outputtext" name="outputtext"  rows="10" style="background-color: #FFF; font-size:14px"></textarea> </form> <div class="btn-group in forsave"><button class="btn savetestcase" type="button" id="1"><i class="icon-ok-circle"></i> Save</button></div></div>'+ 
                           '    </div>')  
                        $(".inputtext").eq(j-1).val(testinput[j-1]);
                        $(".outputtext").eq(j-1).val(testoutput[j-1]);
                      }
                    i=j-1;
                    $("#latest").append( ' <div class=" marginbottom" id="fordelete"> <div class="btn-group in"><button class="btn" type="button" id="testcase"><i class="icon-tasks"></i> Add a new test case</button></div> </div>')
                   $("#latest").show("slide", { direction: "up" }, 600)},600);

 }


 )
 
 $(document).on("click","#testcase",function(){

  i=i+1;
  $("#fordelete").remove();
  $("#latest").append('   <div class="fields "> Test case '+i+' <span class="terrormessage" style="font-size:13px"> </span> </p></div>'+ 
                         '   <div class="casebigbox"> '+ 
                        '       <div class="inputtest"> '+                           
                         '        <p class="indents"> Input </p>'+ 
                           '       <form><textarea class="inputtext" name="inputtext" cols="45" rows="10" style="background-color: #FFF; font-size:14px"></textarea> </form> '+ 
                           '     </div> '+ 
                           '     <div class="outputtest"> '+ 
                           '    <p class="indents">  Output</p>'+ 
                            '    <form><textarea class="outputtext" name="outputtext" cols="45" rows="10" style="background-color: #FFF; font-size:14px"></textarea> </form> <div class="btn-group in forsave"><button class="btn savetestcase" type="button"><i class="icon-ok-circle"></i> Save</button></div></div>'+ 
                           '    </div>'+ 
                           '   <div class=" marginbottom" id="fordelete"> <div class="btn-group in"><button class="btn" type="button" id="testcase"><i class="icon-tasks"></i> Add a new test case</button></div> </div>')
     })

$(document).on("click","#savedescription",function(){
  descr=$("#description1").val();

  $.post('/api/createproblem',
  {
    problem_id:problem_id,
    description:descr
  },
  function(data){
       var result = jQuery.parseJSON(JSON.stringify(data));
       isOkay=result.isOkay
       error=result.error
       if (isOkay)
       {
        var date= new Date();

        $("#desc").html('<span style="color:green; font-weight:normal; font-size:12; float:right"> Saved '+date.toLocaleTimeString()+'  </span>')
       }
       else
       {
        $("#desc").html('<span style="color:red; font-weight:normal; font-size:12; float:right">'+error+'</span>')
       }

      }

  )
})

$(document).on("click",".savetestcase",function(){
  var k = $(".savetestcase").index(this);
  tinput=$(".inputtext").eq(k).val();
  toutput=$(".outputtext").eq(k).val();
  $.post('/api/createtestcase',
  {
    problem_id:problem_id,
    testcase_number:(k+1),
    input_value:tinput,
    expected_output:toutput
  },
    function(data){
       var result = jQuery.parseJSON(JSON.stringify(data));
       isOkay=result.isOkay
       error=result.error       
       if (isOkay)
       {
        var date= new Date();

        $(".terrormessage").eq(k).html('<span style="color:green; font-weight:normal; font-size:12; float:right"> Saved '+date.toLocaleTimeString()+'  </span>')
       }
       else
       {
        $(".terrormessage").eq(k).html('<span style="color:red; font-weight:normal; font-size:12; float:right">'+error+'</span>')
       }

      }
  )


})} )



});


