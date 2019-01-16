$(document).ready(function() {
    $('#file').on('change', handleUpload);
    $('#query-button').on('click', handleQuery);
    $('#draw-button').on('click', handleDraw);
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
            $('#query-button').prop('disabled', false);
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
    var formData = new FormData();
    formData.append('image', dataUrl);

    $.ajax({
        url: '/draw',
        type: 'POST',
        data: formData,
        success: function (data) {
            console.log(data);
            var images = $('#draw-group');
            images.children('div.result').remove();
            for (i = 0; i < Math.min(data.length, 3); i++) {
                var path = data[i];
                var id = "draw-result-" + i;
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
        },
        cache: false,
        contentType: false,
        processData: false
    });
}