$(document).ready(function() {
    $('#image-holder').hide();
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
        },
        cache: false,
        contentType: false,
        processData: false
    });
}
