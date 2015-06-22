$(function() {
    $('.comment-success').hide();
    $('.home-btn').click(function() {
        var comment = $('txtComment').val();
        $.ajax({
            url: '/homeContact',
            data: $('#contact-form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response, 'submitted');
                $('.comment-success').show("drop", { direction: "up" }, "slow");
            },
            error: function(error) {
                console.log(error);
            }
        });
    });


});