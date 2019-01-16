$(document).ready(function() {
    $('#file').on('change', handleUpload);
    $('#query-button').on('click', handleQuery);
    $('#draw-button').on('click', handleDraw);
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    // ctx.fillStyle = "white";
    // ctx.fillRect(0, 0, canvas.width, canvas.height);

    var background = new Image();
    background.src = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1547578848740&di=790d93a4122a73a06782638ecfc932d3&imgtype=0&src=http%3A%2F%2Fimg1.qunarzz.com%2Fvc%2F99%2Fe9%2F12%2F30ebcefe5f721501b3a9477bb4.gif_92.gif";

    ctx.drawImage(background,0,0);
});

function handleUpload() {
    var formData = new FormData();
    formData.append('file', $('#file')[0].files[0]);

    $.ajax({
        url: '/upload_image',  
        type: 'POST',
        data: formData,
        success: function (data) {
            var image = $('#image-holder');
            image.attr('src', data);
            $('#upload-group').show();
           //  $('#query-button').prop('disabled', false);
        },
        cache: false,
        contentType: false,
        processData: false
    });
}

function handleQuery() {
    var filename = $('#image-holder').attr("src").substr(8);
    $.ajax({
        url: '/query/' + filename,
        type: 'GET',
        success: function (data) {
            console.log(data);
            var images = $('#upload-group');
            images.children('div.result').remove();
            for (i = 0; i < Math.min(data.length, 3); i++) {
                var path = data[i];
                var id = "upload-result-" + i;
                var image = '<div class="col-xs-6 col-md-3 result">' +
                            '  <a href="' + path + '" class="thumbnail">' +
                            '    <img id="' + id + '" src="' + path + '">' +
                            '  </a>' +
                            '  <div class="caption caption-result">' +
                            '    <span class="label label-success">Result #' + (i+1) + '</span>' +
                            '  </div>' +
                            '</div>';
                images.append(image)
            }
            images.show();
        }
    });
}

function handleDraw() {
    var canvas = document.getElementById('myCanvas');
    var dataUrl = canvas.toDataURL();
    alert(dataUrl);
    $('#image-holder').attr('src', dataUrl);
    var formData = new FormData();
    formData.append('image', dataUrl);

    $.ajax({
        url: '/try',
        type: 'POST',
        data: formData,
        success: function (data) {
            console.log(data);
        },
        cache: false,
        contentType: false,
        processData: false
    });
}