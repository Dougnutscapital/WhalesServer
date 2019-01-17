paper.install(window);
// Keep global references to both tools, so the HTML
// links below can access them.
var tool1;

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
      path.strokeWidth = 4;
      path.add(event.point);
    }

    tool1 = new Tool();
    tool1.onMouseDown = onMouseDown;

    tool1.onMouseDrag = function(event) {
      path.add(event.point);
    }
};