function vote(pollid){
  //var data = new FormData($("#form-"+pollid)[0]);
  //console.log(data);
  var form = document.getElementById('form-'+pollid);
  var formData = new FormData(form);
  var cho = formData.get("choice");
  if (!cho){
    $("#error-title")[0].innerHTML = "No Choice selected"
    $("#error-desc")[0].innerHTML = "Please select a choice"
    $('#errmodal').modal('open');
    return; 
  }
  $.ajax({
    method:"POST",
    url: "/polls/vote/",
    data: {
      choice: formData.get("choice"),
      csrfmiddlewaretoken: formData.get("csrfmiddlewaretoken")
    }
  })
  .done(function(data){
    res = readResult(data["code"])
    errTitle = $("#error-title")[0]
    errDesc = $("#error-desc")[0]
    switch(res[0]){
      case "0":
        drawthispoll(pollid);
        break;
      case "1":
        switch(res[1]){
          case 1:
            errTitle.innerHTML = "Please Sign-in or Sign-up"
            errDesc.innerHTML = "To vote you must be registered and loged"
            break;
          case 2:
            errTitle.innerHTML = "This poll is closed"
            errDesc.innerHTML = "You can't vote in this poll anymore"
            break;
          case 3:
            errTitle.innerHTML = "Choice not found"
            errDesc.innerHTML = "The choice you voted for doesn't exist"
            break;
          case 4:
            errTitle.innerHTML = "Server Error"
            errDesc.innerHTML = "Please contact an administrator"
            break;
        }
        $('#errmodal').modal('open'); 
        break;
    }
  });
}

function readResult(res){
    status = parseInt(res & 8 >> 3)
    desc = parseInt(res & 7)
    return [status, desc]
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
        tooltip: {
          trigger: 'none'
        },
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
var count = 1;
$(document).ready(function(){
  document.getElementById("choice"+count).addEventListener("input", addChoice);
  document.getElementById("confirm_poll").addEventListener("click", addPoll);
  
});

function addChoice(){
    var btn = document.createElement("INPUT");
    count += 1;
    btn.placeholder="Choice "+count;
    btn.id="choice"+count
    btn.name="choice"+count
    btn.addEventListener("input", addChoice)
    document.getElementById("newpoll").appendChild(btn);
    document.getElementById("choice"+(count-1)).removeEventListener("input",addChoice)
   
};

function addPoll(){

  var form = document.getElementById('create_poll');
  var formData = new FormData(form);
  var title = formData.get("polltitle")
  var workhours = formData.get("workhours")
  var choices = []
    for (var i=0;i<count;i++){
      choices[i] = formData.get("choice"+(i+1))
    }
  $.ajax({
    method:"POST",
    url: "/polls/new/",
    data: {"Title":title,"hours":workhours,"answers":choices,"csrfmiddlewaretoken":formData.get("csrfmiddlewaretoken")}
  })
  .done(function(data){
    window.location.reload()
  });
}
//function addPoll(){
//  var title = document.getElementById("polltitle").value
//  var workhours = document.getElementById("workhours").value
// var choices = []
//    for (var i=0;i<count;i++){
//      choices[i] = document.getElementById("choice"+(i+1)).value
//     }
//   console.log(title)
//   console.log(workhours)
//   console.log(choices)
//   $.ajax({
//     method:"POST",
//     url: "/polls/new/",
//     data: {}
//   })
//   .done(function(data){
    
//   });
// }

$(document).ready(function(){
  google.charts.load('current', {packages: ['corechart']});
    $('#errmodal').modal();

});

