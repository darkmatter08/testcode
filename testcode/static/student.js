$(document).ready(function(){

$(".problemlinks").eq(0).addClass("active")


 $( "#reset1" ).click(function() {                                                                               
                                   editor.setValue("");
                                 });
 var problem_id=$(".active").attr("id");
 $( ".changecode" ).click(function() 
 					{  
 					var type=$(this).attr("id");                                                                             
                    $.post('/api/getsubmission',
                    {
                    	problem_id:problem_id,
                    	sumbission_id:submission_id,
                    	type:type
                    },
                    function(data){
                    	var result = jQuery.parseJSON(JSON.stringify(data))
                    	text=result.text
                    	isfirst=result.is_first;
                    	islast=reulut.is_last;
                    	editor.setValue(text);
                    	if (isfirst) {$("previous").addClass("disabled")}                    	 	
                    	if (islast) {$("next").addClass("disabled")}


                    }


                    )

                    });





});