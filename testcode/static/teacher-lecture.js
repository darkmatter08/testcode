 $(document).ready(function(){

$(".viewsubmissions").live('click', function(){ 
                var id=$(this).attr('id')
                 $(location).attr('href','/testcode/teacher/edit/performance/'+id);
                 })

 $(function() {
  
    
    lectureid=$(".lectureelement").attr('id');  
      var  pname=$( "#problemname" );
     

 $( "#dialog-formproblem" ).dialog({
      autoOpen: false,
      height: 220,
      width: 450,
      modal: true,
      buttons: {
          "Create a problem": function() {               
            var name=pname.val()
            allFields = $( [] ).add( pname )
          
          $.post('/testcode/api/createproblem',
                      {
                      problem_name:pname.val(),
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
                          $("#problemstable1").prepend(' <tr>'+                                 
                                 '<td>0 submissions</td> <td> <div class="btn-group in rightm">'+       
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

var problem_id;
 $(function() 
{
var i;

$(document).on("click",".problemlinks",function(){
              
              $(".active").eq(1).removeClass("active");
              $(this).addClass("active");
              problem_id=$(this).attr('id'); 
              var name
              var description                   
              var testinput
              var testoutput
              var num_testcases
              var code
              var timelimit
            $.post( '/testcode/api/getproblemteacher',
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
                       code=result.initial_code;
                       timelimit=result.timeout;

                    },

                    "json"
                ); 
              $("#latest").hide("slide", { direction: "up" }, 500);
               setTimeout(function(){            
                    
                     $("#latest").html('<div class="classe">'+                    
                           '<div class="margins">'+name+' </div> '+ 
                          ' </div> '+ 
                            ' <div class="fields1"> Description  <div class="pull-right" style="width:320px">Initial code <span class="errormesage" id="desc" style="font-size:13px"> </span></div></div>     '+                
                          ' <div class="casebigbox1"><div id="problemdescription" class="pull-left"> <form><textarea id="description1" name="description" rows="10" placeholder="Enter your problem description here. Make sure to include all information a student requires to solve the problem" Print the result." style="background-color: #FFF; font-size:14px"></textarea> </form> </div>'+
                          ' <div id="initialcode" class="pull-right"> <form><textarea id="incode" name="code" rows="10" placeholder="Any code you want provided to the student automatically. Ex: import statements, Input values to the problem: a=int(raw_input()) \n b=str(raw_input())" style="background-color: #FFF; font-size:14px"></textarea> </form> '+ 
                        '  '+
                        '</div> </div><div class=" marginbottom1"><div class="btn-group in forsave"><button class="btn" type="button" id="savedescription"><i class="icon-ok-circle"></i> Save</button></div> </div></div>'+
                      '<div class="fields "> Test cases </div>')
                     $("#description1").val(description);
                     $("#appendedInput").val(timelimit);
                     $("#incode").val(code);
                     for (var j=1; j<(num_testcases+1); j++)
                     {
                        $("#latest").append( '   <div class="casebigbox"> '+ 
                        '       <div class="inputtest"> '+                           
                         '        <p class="indents"> Input '+j+' </p>  '+ 
                           '       <form><textarea class="inputtext" name="inputtext"   placeholder="Assign values to each raw_input(), enter values separated by new line" rows="3" style="background-color: #FFF; font-size:14px"></textarea> </form> '+ 
                           '     </div> '+ 
                           '     <div class="outputtest"> '+ 
                           '    <p class="indents">  Output '+j+' <span class="terrormessage" style="font-size:13px"> </span></p>'+ 
                            '    <form><textarea class="outputtext" name="outputtext"  placeholder="Enter correct output values for the input data. Be careful with new lines" rows="3" style="background-color: #FFF; font-size:14px"></textarea> </form></div> </div> <div class="margins"> <div class="btn-group in forsave"><button class="btn savetestcase" type="button" id="1"><i class="icon-ok-circle"></i> Save</button></div>'+ 
                           ' </div>  ')  
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
  $("#latest").append( '   <div class="casebigbox"> '+ 
                        '       <div class="inputtest"> '+                           
                         '        <p class="indents"> Input  '+i+'  </p>'+ 
                           '       <form><textarea class="inputtext" name="inputtext" placeholder="To assign values to each raw_input(), enter values separated by new line" cols="45" rows="3" style="background-color: #FFF; font-size:14px"></textarea> </form> '+ 
                           '     </div> '+ 
                           '     <div class="outputtest"> '+ 
                           '    <p class="indents">  Output '+i+' <span class="terrormessage" style="font-size:13px"> </span> </p>'+ 
                            '    <form><textarea class="outputtext" name="outputtext" cols="45" rows="3" style="background-color: #FFF; font-size:14px"></textarea> </form> </div></div><div class="margins"> <div class="btn-group in forsave"><button class="btn savetestcase" type="button"><i class="icon-ok-circle"></i> Save</button></div>'+ 
                           '    </div>'+ 
                           '   <div class=" marginbottom" id="fordelete"> <div class="btn-group in"><button class="btn" type="button" id="testcase"><i class="icon-tasks"></i> Add a new test case</button></div> </div>')
     })

$(document).on("click","#savedescription",function(){
  var descr=$("#description1").val();
  var initialcode=$("#incode").val();
  var timelimit=$("#appendedInput").val();
  $.post('/testcode/api/createproblem',
  {
    problem_id:problem_id,
    description:descr,
    timeout:timelimit,
    initial_code:initialcode
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
  $.post('/testcode/api/createtestcase',
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


