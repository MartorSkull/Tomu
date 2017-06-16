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

