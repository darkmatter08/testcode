 
 $(document).ready(function(){
 var color=['#041a6d', '#1a269f', '#05519e', '#059e99','#059e51',  '#059e09' , '#036205', '#498700', '#2d5003', '#847f00']
 var chart1= new Array(), 
     chart2= new Array(),
     chart20= new Array(), 
     chart21= new Array(),
     submission_id= new Array(),
     name,date= new Array(), 
     grade= new Array(), 
     notsubmit= new Array()
     array= new Array()
 var n,ntest 
   
  

  function getInfo()
  { 

   var problem_id=$(".active").attr('id');
   

    $.post( '/api/viewperformance',
             {
              problem_id:problem_id
             },
             function(data)
                   {
                    var result = jQuery.parseJSON(JSON.stringify(data))             
                    notsubmit=result.unsubmitted
                    submission_id=result.submission_id, 
                    name=result.name, 
                    date=result.date, 
                    grade=result.grade                    
                    n=name.length
                    for (var i=0; i<n;i++)
                        {array[i]=jQuery.parseJSON(grade[i]) }
                    grade=array                             
                     if (n==0)
                      {$("#shit").html("This problem has no submissions")}
                     else
                      { $("#insert").html(n+' students submitted a solution')  
                        var    scored= new Array()
                         var       score= new Array()
                          var      passed= new Array()
                          var      failed= new Array()                           
                          ntest=grade[0].length                           
                            for (var j=0; j<ntest+1; j++)
                            {
                              score[j]=0; scored[j]=0; failed[j]=0; passed[j]=0; 
                            }

                           for (var i=0; i<n; i++)
                              { 
                                for (var j=0; j<ntest; j++)
                                    {                                       
                                      if (grade[i][j]=="True") 
                                          {
                                            passed[j]++
                                            score[i]++
                                          } 
                                      else 
                                          {
                                            failed[j]++
                                          }
                                    }
                                scored[score[i]]++
                              }                           
                            for (var i=0; i<ntest+1; i++)
                              {
                                  chart1[i]=new Array("Passed "+i+" testcases", scored[i])
                              }                           
                            var plot1 = jQuery.jqplot ('chart_div', [chart1], 
                                    {  title:'Students\' score chart',
                                      seriesDefaults: {
                                        renderer: jQuery.jqplot.PieRenderer, 
                                        rendererOptions: 
                                        {showDataLabels: true
                                        }
                                      }, 
                                      grid: { background: 'none'   ,
                                        borderColor: 'none',
                                         shadow: false,  
                                        },
                                       legend: { show:true, location: 'e' }
                                    }
                                  );
                             for (var i=1; i<ntest+1; i++)
                              {
                                chart20[i-1]=[passed[i-1], '#'+i]
                                chart21[i-1]=[failed[i-1], '#'+i]
                              } 
                            chart2=new Array(chart20, chart21)                            
                            var plot2 = $.jqplot('chart_div2', [chart20, chart21], {
                                        title:'Performance per test case',
                                        seriesDefaults: {                                            
                                            renderer:$.jqplot.BarRenderer,                                           
                                            pointLabels: { show: true, location: 'e', edgeTolerance: -15 },
                                            shadowAngle: 135,
                                            rendererOptions: {
                                                barDirection: 'horizontal'
                                            }
                                        },
                                        series:[
                                             {label:'Passed'},
                                             {label:'Failed'},
                                            
                                               ],
                                         grid: { background: 'none'   ,
                                        borderColor: 'none',
                                         shadow: false,  
                                        },
                                        legend: {
                                      show: true,
                                      location: 'e',
                                      placement: 'outside'
                                    } ,
                                        axes: {
                                            yaxis: {
                                                label:'Testcase',
                                                renderer: $.jqplot.CategoryAxisRenderer,
                                                labelRenderer: $.jqplot.CanvasAxisLabelRenderer,                                               
                                        }
                                      }}) } })}                

getInfo()
var checked= new Array()


var icon
var row
$("input:radio").change(function(){   
  var j=0;
  var string=""
 for (var i=1; i<ntest+1; i++)
   {
   checked[i]=$("input:radio[name='"+i+"']:checked").val()
   }
   $("#filter").remove()  
   for (var i=1; i<ntest+1; i++) 
   {
    string=string+'<td> TC #'+i+' </td>'
  }
   string='<table class="table table-hover" id="filter"><thead><tr > <span style="font-weight:900"><td > # </td> <td> Student\'s name </td><td> Date sent </td>'+string+' </span></tr></thead>'
   for (var i=0; i<n; i++)
      {
        
        tohide=false
        row=""        
        for (var k=1; k<ntest+1; k++)
              {                
                if (grade[i][k-1]=="True") icon="ok"; else icon="remove"
                row=row+'<td> <i class="icon-'+icon+'"></i></td>'
                if (checked[k]=='pass' && grade[i][k-1]=="False") {tohide=true} else{ if (checked[k]=='fail' && grade[i][k-1]=="True") {tohide=true}}
                
              }
        if (!(tohide)) {j=j+1; string=string+'<tr id="'+submission_id[i]+'" class="submissionlinks"> <td>'+j+'</td><td>'+name[i]+'</td> <td>'+date[i]+'</td>'+row+'</tr>'}
      }
    string=string+' </tr></table>'
    $("#latest").append(string)  
      })

 $(".submissionlinks").live('click', function() {
                  
                    var id=$(this).attr('id');
                    alert(id);
                    $.post(
                        '/api/getsubmissionteacher',
                        {
                          submission_id:id
                        },
                        function(data)
                        {
                         var result = jQuery.parseJSON(JSON.stringify(data))
                         var text=result.solution;
                         $(".language-py").html(text)
                         $( "#viewsubmission" ).dialog( "open" )
                        })
                  })                              
 
  $( "#viewsubmission" ).dialog({
      autoOpen: false,
      height: 700,
      show: 'fade',
      hide: 'fade',
      width: 900,
      modal: true,
      // buttons: {
        
      //   Cancel: function() {
      //     $( this ).dialog( "close" );
      //                      }
      //   },
      close: function() {
        allFields.val( "" ).removeClass( "ui-state-error" );
      }
    });

  
        



       }) ;                