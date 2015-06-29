$(function () {
    $('.comment-success').hide();
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

    $('.image-btn').click(function() {
        var form_data = new FormData($('#image-form')[0]);
        console.info(form_data)
        $.ajax({
            type: 'POST',
            url: '/fileUpload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(data) {
                console.log('Success!', data);
            },
            error: function(error) {
                console.error(error);
            }
        });
    });
});
