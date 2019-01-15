$(document).ready(function() {
    $('#image-holder').hide();
    $('#query-button').hide();
    $('#similar-image').hide();
    $('#file').on('change', handleUpload);
});

function handleUpload() {
    var formData = new FormData();
    formData.append('file', $('#file')[0].files[0]);

    $.ajax({
        url: '/upload_image',  
        type: 'POST',
        data: formData,
        success: function (data) {
            //alert(data);
            var image = $('#image-holder');
            image.attr('src', data);
            image.show();
            var queryButton = $('#query-button');
            queryButton.show();
        },
        cache: false,
        contentType: false,
        processData: false
    });
}

$( "#query-button" ).click(function () {
    var filename = $('#image-holder').attr("src").substr(8);
    $.ajax({
        url: '/query/' + filename,
        type: 'GET',
        success: function (data) {
            console.log(data);
            var images = $('#similar-image')
            for (i = 0; i < Math.min(data.length, 3); i++) {
                var path = data[i]
                var id = "img" + i
                var image = '<img id=' + id + ' src=' + path + ' />'
                images.append(image)
            }
            images.show()
        }
    });
})