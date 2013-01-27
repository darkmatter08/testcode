$(document).ready(function(){

$(".problemlinks").eq(0).addClass("active")


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
                                            var text=result.solution
                                            var hasNext=result.hasNext;
                                            var hasPrev=result.hasPrev;
                                            editor.setValue(text);                                           
                                            var id=result.submission_id;

                                            $('form').attr('id', id);
                                            if  (hasPrev) {$("#previous").removeClass("disabled")}  else {$("#previous").addClass("disabled")}                    	 	
                                            if (hasNext) {$("#next").removeClass("disabled")}   else {$("#next").addClass("disabled")}
                                        },
                                    "json"
                                  )
                            }
                      }
                            );

 $(".problemlinks").click(function(){
       problem_id=$(this).attr("id");
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
                        editor.setValue(text);
                        var description=result.description;
                        var id=result.sumbission_id;
                        $('form').attr('id', id);
                        if  (hasPrev) {$("previous").removeClass("disabled")}  else {$("previous").addClass("disabled")}                    	 	
                        $("next").addClass("disabled")
                    }
	           )


 })





});