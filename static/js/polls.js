function vote(pollid){
  //var data = new FormData($("#form-"+pollid)[0]);
  //console.log(data);
  var form = document.getElementById('form-'+pollid);
  var formData = new FormData(form);
  var cho = formData.get("choice");
  $.ajax({
    method:"POST",
    url: "/polls/vote/",
    data: {
      choice: formData.get("choice"),
      csrfmiddlewaretoken: formData.get("csrfmiddlewaretoken")
    }
  })
  .done(function(data){
    drawthispoll(pollid);
  });
}


function drawthispoll(id){

  $.ajax({
    method: "GET",
    url: "/polls/getpoll/" + id,
  })
    .done(function (info) {

      var data = new google.visualization.DataTable();

      data.addColumn('string', 'Choice');
      data.addColumn('number', 'Votes');

      data.addRows(info.columns);

      var options = {
        backgroundColor: "#000000",
        legend: {
          position: 'bottom', 
          textStyle: {
            color: 'white'}},
      }

      var chart = new google.visualization.PieChart($('#graph-'+info.id)[0]);
      chart.draw(data, options);

      
    });
}

//drawthispoll(
//{
//    pollid: 1,
//    "choices":[["hola", 5],["chau", 8]],
//    }, );
//

$(document).ready(function(){
  google.charts.load('current', {packages: ['corechart']});
});