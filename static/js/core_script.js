$(function () {
    $('.comment-success').hide();
    $('.upload_loader').hide();
    $('.upload-success').hide();

    $('.home-btn').click(function () {
        var comment = $('txtComment').val();
        $.ajax({
            url: '/homeContact',
            data: $('#contact-form').serialize(),
            type: 'POST',
            success: function (response) {
                console.log(response, 'submitted');
                $('.comment-success').show("drop", {direction: "up"}, "slow");
            },
            error: function (error) {
                console.log(error);
            }
        });
    });


    $('.image-btn').click(function () {

        var ext = $('#file_field').val().split('.').pop().toLowerCase();
        if ($.inArray(ext, ['gif', 'png', 'jpg', 'jpeg']) == -1) {
            alert('invalid extension!');
        }
        else {
            var form_data = new FormData($('#image-form')[0]);
            $('.upload_loader').show();
            $.ajax({
                type: 'POST',
                url: '/fileUpload',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                success: function (data) {
                    var dataIT = jQuery.parseJSON(data);
                    $('.profile-img').attr('src', dataIT.details.secure_url).show("drop", {direction: "up"}, "slow");
                },
                complete: function () {
                    $('.upload_loader').hide();
                    $('.upload-success').text('Image Successfully Uploaded').show();
                    return true;
                },
                error: function (error) {
                    return false;
                }
            });
        }
    });
});
