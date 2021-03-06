///Custom validation
//form id = profile-form
//job id = jobInput
//about id = about

$(function () {
    var validate = {
        inputId: ['jobInput', 'about', 'major_skill', 'had_known', 'advice', 'recommended_reads'],
        init: function () {
            this.checkDirtyInput();
            this.onKeyUpDirtyInputCheck();
        },

        checkDirtyInput: function () {
            var count = 0;
            for (var i = 0; i < this.inputId.length; i++) {
                count++;
                if ($('#' + this.inputId[i]).val() < 1) {
                    return $('#profile-btn').attr('disabled', 'disabled').attr('class', 'btn btn-block btn-dark profile-btn').html('Please fill required fields');
                } else {
                    $('#profile-btn').attr('disabled', false).attr('class', 'btn btn-block btn-dark profile-btn btn-success').html('Update Profile');
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
