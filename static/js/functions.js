function readResult(res){
    status = parseInt(res) & 8 >> 3
    console.log(status)
    desc = parseInt(res) & 7
    return [status, desc]
}

$(document).ready(function(){
 $('.dropdown-button').dropdown({
      inDuration: 300,
      outDuration: 225,
      constrainWidth: false, // Does not change width of dropdown to that of the activator
      hover: true, // Activate on hover
      gutter: 0, // Spacing from edge
      belowOrigin: true, // Displays dropdown below the button
      alignment: 'left', // Displays dropdown with edge aligned to the left of button
      stopPropagation: false // Stops event propagation
    }
  );
 $('.modal').modal();

 $('#profile_button').on("click", function(){
  console.log("adsasd");
  $('#userdrop').dropdown('open');
 });
});

  
