$(document).ready(function(){

$(".problemlinks").eq(0).addClass("active")

$(function(){
       problem_id=$(".problemlinks").eq(0).attr("id");       
       $.post(
                '/api/getproblem',
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
                                   editor.setValue("");
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
                                    '/api/getsubmission',
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
                '/api/getproblem',
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
                        $("#descriptionplace").html(description);
                        $("#feedback").html('<br/>Press "Save & Run" to see your results.<br/>') 
                        $('form').attr('id', id);                       
                        if (hasPrev) {$("#previous").removeClass("disabled")}  else {$("#previous").addClass("disabled")}                    	 	
                        $("next").addClass("disabled");
                        var testinput=result.testcase_input;
                        var testoutput=result.testcase_output; 
                        var num_testcases=testinput.length;
                        var initialcode=result.initial_code;
                        var timelimit=result.timelimit;
                        localStorage['inputs']=JSON.stringify(testinput);
                        localStorage['outputs']=JSON.stringify(testoutput);
                    }
	           )
 })

 $("#run").click(function()
    {
       problem_id=$(".active").eq(0).attr("id");
       var solution=editor.getValue();       
      $.post('/api/submit',
         {
             problem_id:problem_id,
             solution:solution        
         },
         function(data)
         {
         	 var result = jQuery.parseJSON(JSON.stringify(data));
         	 var ifpassed=result.grade;
         	 var n=ifpassed.length   
         	 
         	   
          }
       )
    }
)





});