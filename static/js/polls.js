function vote(pollid){
  //var data = new FormData($("#form-"+pollid)[0]);
  //console.log(data);
  var form = document.getElementById('form-'+pollid);
  var formData = new FormData(form);
var choice = formData.get("choice");
  $.ajax({
    method:"POST",
    url: "/polls/vote/"+ choice,
  })
  .done(function(data){
    
  });
  drawthispoll(pollid);
  
}


function drawthispoll(id){

  $.ajax({
    method: "GET",
    url: "/polls/getpoll/" + id,
  })
    .done(function (info) {
      var chart = c3.generate({
        bindto: '#graph-'+info.id,
        data: {
          columns: info.columns,
          type: "pie"
        },
        size:{
          height: 200,
          width: 200
        }
      });
    });
}

//drawthispoll(
//{
//    "choices":["hola", "chau"],
//    "votes":[5,8],
//    "items":2
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
