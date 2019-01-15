paper.install(window);
// Keep global references to both tools, so the HTML
// links below can access them.
var tool1;

// var canvas = document.getElementById("canvas"),
//     ctx = canvas.getContext("2d");
//
// window.src = new Image();
// background.src = "http://i.imgur.com/yf6d9SX.jpg";

window.onload = function() {
    paper.setup('myCanvas');

    //ctx.drawImage(background)
    // Create two drawing tools.
    // tool1 will draw straight lines,

    // Both share the mouseDown event:
    var path;
    function onMouseDown(event) {
      path = new Path();
      path.strokeColor = 'black';
      path.add(event.point);
    }

    tool1 = new Tool();
    tool1.onMouseDown = onMouseDown;

    tool1.onMouseDrag = function(event) {
      path.add(event.point);
    }
};