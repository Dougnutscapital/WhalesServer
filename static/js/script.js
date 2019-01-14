$(document).ready(function() {
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
            alert(data);
        },
        cache: false,
        contentType: false,
        processData: false
    });
}
