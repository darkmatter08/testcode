var input;
var output;
var youroutput; 
var ifpassed=new Array()
var error
var pass
 var initialcode
$(document).ready(function(){

$(".problemlinks").eq(0).addClass("active")

$(function(){
       problem_id=$(".problemlinks").eq(0).attr("id");       
       $.post(
                '/testcode/api/getproblem',
                 {
                  problem_id:problem_id,
                 },
                  function(data)
                    {
                        var result = jQuery.parseJSON(JSON.stringify(data))
                        var text=result.solution                       
                        var id=result.submission_id;                        
                        $('form').attr('id', id);   
                         editor.setValue(""+text); 
                         var hasNext=result.hasNext;
                         var hasPrev=result.hasPrev;
             if (hasPrev) {$("#previous").removeClass("disabled")}  else {$("#previous").addClass("disabled")}                        
                          if (hasNext) {$("#next").removeClass("disabled")}   else {$("#next").addClass("disabled")}                   
                     }
             )


 });


 $( "#reset1" ).click(function() {                                                                               
                                   editor.setValue(""+initialcode);
                                 });
 var problem_id=$(".active").attr("id");
 $( ".changecode" ).click(
                          function() 
          { if (! ($(this).is('.disabled')) ) 
                {var type=$(this).attr("id");   
          isNextSubmission=1;
          submission_id=$('form').attr('id');
         
          if (type=="previous") {isNextSubmission=0}                                                                                
                            $.post(
                                    '/testcode/api/getsubmission',
                                    {  

                                      submission_id:submission_id,
                                      isNextSubmission:isNextSubmission
                                    },
                                      function(data)
                                        {
                                            var result = jQuery.parseJSON(JSON.stringify(data))
                                            var text=result.solution;
                                            var hasNext=result.hasNext;
                                            var hasPrev=result.hasPrev;
                                            editor.setValue( ""+text);                                           
                                            var id=result.submission_id;
                                            $('form').attr('id', id);
                                            if (hasPrev) {$("#previous").removeClass("disabled")}  else {$("#previous").addClass("disabled")}                       
                                            if (hasNext) {$("#next").removeClass("disabled")}   else {$("#next").addClass("disabled")}
                                        },
                                    "json"
                                  )
                            }
                      }
                            );

 $(".problemlinks").click(function(){
       problem_id=$(this).attr("id");
       $(".active").eq(0).removeClass("active");
       $(this).addClass("active");      
        $.post(
                '/testcode/api/getproblem',
                 {
                  problem_id:problem_id,
                 },
                  function(data)
                    {
                        var result = jQuery.parseJSON(JSON.stringify(data))
                        var text=result.solution                       
                        var hasPrev=result.hasPrev;
                        editor.setValue(""+text);
                        var description=result.description;
                        var id=result.submission_id;                        
                        var name=result.name; 
                        initialcode=result.initial_code                       
                        $("#descriptionplace").html(description);
                        $("#insidefeedback").html('Press "Save & Run" to see your results.<br/>') 
                        $('form').attr('id', id);                       
                        if (hasPrev) {$("#previous").removeClass("disabled")}  else {$("#previous").addClass("disabled")}                       
                        $("next").addClass("disabled");                       
                        initialcode=result.initial_code;                        
                    }
             )
 })

 $("#run").click(function()
    {
       problem_id=$(".active").eq(0).attr("id");
       var solution=editor.getValue();       
        $("#run").button('loading');
        $("#insidefeedback").fadeOut(1000);

      $.post('/testcode/api/submit',
         {
             problem_id:problem_id,
             solution:solution        
         },
         function(data)
         {
           $("#run").button('reset');
           var result = jQuery.parseJSON(JSON.stringify(data));
           pas=result.grade;
           input=result.inputs;
           output=result.expected_outputs;
           youroutput=result.outputs;
           error=result.errors;
           var score=0;
           var n=pas.length 
           for (var i=0;i<n;i++) {if (pas.charAt(i)==1) {ifpassed[i]=true} else ifpassed[i]=false}
           $("#previous").removeClass("disabled") 
           for (var i=1; i<n+1;i++) {if (ifpassed[i-1]) score++}
           if (score==n) { $("#insidefeedback").html('<p style="font-weight:900; color:#008A05; font-size:16px"> Correct:'+n+'/'+n+'</p>')} else
                         { $("#insidefeedback").html('<p style="font-weight:900; color:#FA2100; font-size:16px"> Correct:'+score+'/'+n+'</p>')}
           $("#insidefeedback").append('<div style="-webkit-column-count:3">')
           for (var i=1; i<n+1;i++) {
            if (ifpassed[i-1]) 
                 $("#insidefeedback").append('<button type="button" class="btn btn-success test" id="'+i+'">Testcase '+i+'</button>');
            else
                 $("#insidefeedback").append('<button type="button" class="btn btn-danger test" id="'+i+'">Testcase '+i+'</button>');
              }
            $("#insidefeedback").append('</div>')
            $("#insidefeedback").fadeIn(800);
          }
       )
    }
)

$( "#viewtest" ).dialog({
      autoOpen: false,
      height: 'auto',
      show: 'fade',
      hide: 'fade',
      width: 'auto',
      modal: true,
     close: function() {
        allFields.val( "" ).removeClass( "ui-state-error" );
      }
    });

$(".test").live('click', function()
            {
              var id=$(this).attr('id')
              $("#forcorr").html("")
              $("#forwrong").html("")
              if (ifpassed[id-1]) { $("#forcorr").html(error[id-1])} else { $("#forwrong").html(error[id-1])}
              $("#in").html(input[id-1])
              $("#yourout").html(youroutput[id-1])
              $("#corrout").html(output[id-1])
              $("#viewtest").dialog("open")
            }
               )
});