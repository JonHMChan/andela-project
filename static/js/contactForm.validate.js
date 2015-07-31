//contact form validation

$(function () {
    var validate = {
        inputId: ['name', 'email', 'subject', 'message'],
        init: function () {
            this.checkDirtyInput();
            this.onKeyUpDirtyInputCheck();
        },

        checkDirtyInput: function () {
            var count = 0;
            for (var i = 0; i < this.inputId.length; i++) {
                count++;
                if ($('#' + this.inputId[i]).val() < 1) {
                    return $('#btnContactUs').attr('disabled', 'disabled').html('Please fill required fields');
                } else {
                    $('#btnContactUs').attr('disabled', false).html('SEND MESSAGE');
                }
            }
        },

        onKeyUpDirtyInputCheck: function () {
            for (var i = 0; i < this.inputId.length; i++) {
                $('#' + this.inputId[i]).keyup(function () {
                    validate.checkDirtyInput();
                });
            }
        }
    };

    validate.init();
});