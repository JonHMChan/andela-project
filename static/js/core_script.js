$(function () {
    $('.comment-success').hide();
    $('.update-success').hide();
    $('.update-failure').hide();
    $('.upload_loader').hide();
    $('.upload-success').hide();
    $('.upload-failure').hide();

    $('.home-btn').click(function () {
        $.ajax({
            url: '/homeContact',
            data: $('#contact-form').serialize(),
            type: 'POST',
            success: function (response) {
                $('.comment-success').show("drop", {direction: "up"}, "slow");
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    $('.profile-btn').click(function () {
        $.ajax({
            url: '/profileInfo',
            data: $('#profile-form').serialize(),
            type: 'POST',
            success: function (response) {
                $('.update-success').show("drop", {direction: "down"}, "slow");
            },
            error: function (error) {
                $('.update-failure').show("drop", {direction: "down"}, "slow");
            }
        })
    });

    //------------------------------CLOUDINARY IMAGE UPLOAD
    $('.image-btn').click(function () {

        var ext = $('#file_field').val().split('.').pop().toLowerCase();
        if ($.inArray(ext, ['gif', 'png', 'jpg', 'jpeg']) == -1) {
            alert('invalid extension!');
        }
        else {
            var form_data = new FormData($('#image-form')[0]);
            $('.upload_loader').show("drop", {direction: "up"}, "slow");
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
                    $('.header-profile-img').attr('src', dataIT.details.secure_url).show("drop", {direction: "up"}, "slow");
                },
                complete: function () {
                    $('.upload_loader').hide();
                    $('.upload-success').text('Image Successfully Uploaded').show();
                    return true;
                },
                error: function (error) {
                    $('.upload-failure').text('Error, please try again').show();
                    return false;
                }
            });
        }
    });


    //----------------------------------AUTOCOMPLETE TAG
    var availableTags = [
        "ActionScript",
        "AppleScript",
        "Asp",
        "BASIC",
        "C",
        "C++",
        "Clojure",
        "COBOL",
        "ColdFusion",
        "Erlang",
        "Fortran",
        "GO",
        "Groovy",
        "Haskell",
        "Java",
        "JavaScript",
        "Lisp",
        "Perl",
        "PHP",
        "Python",
        "Ruby",
        "Scala",
        "Scheme"
    ];

    function split(val) {
        return val.split(/,\s*/);
    }

    function extractLast(term) {
        return split(term).pop();
    }

    $("#tags")
        // don't navigate away from the field on tab when selecting an item
        .bind("keydown", function (event) {
            if (event.keyCode === $.ui.keyCode.TAB &&
                $(this).autocomplete("instance").menu.active) {
                event.preventDefault();
            }
        })
        .autocomplete({
            minLength: 0,
            source: function (request, response) {
                // delegate back to autocomplete, but extract the last term
                response($.ui.autocomplete.filter(
                    availableTags, extractLast(request.term)));
            },
            focus: function () {
                // prevent value inserted on focus
                return false;
            },
            select: function (event, ui) {
                var terms = split(this.value);
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push(ui.item.value);
                // add placeholder to get the comma-and-space at the end
                //terms.push( "" );
                this.value = terms.join(", ");
                console.log(terms);
                return false;
            }
        });

    //-------------------------------TOOLTIP------------------
    $('[data-toggle="tooltip"]').tooltip();


    //----------------------------SOCIAL LINKS-----------------

    $('.website-btn').click(function () {
        return swal({
            title: "Website Link",
            text: "Please put in the link to your website",
            type: "input",
            showCancelButton: true,
            closeOnConfirm: false,
            animation: "slide-from-top",
            inputPlaceholder: "http://->Link"
        }, function (inputValue) {
            if (inputValue === false) return false;
            if (inputValue === "") {
                swal.showInputError("You need to write something!");
                return false
            }
            $.ajax({
                url: '/profileWeblink',
                data: {websitelink: inputValue},
                type: 'POST',
                success: function (response) {
                    swal({
                        imageUrl: '../static/img/thumbs-up.jpg',
                        title: "Link Added Successfully",
                        text: "It has been added to your public profile"
                    });
                },
                error: function (error) {
                    console.log(error);
                }
            });

        });
    });

    $('.github-btn').click(function () {
        return swal({
            title: "Github Link",
            text: "Please put in the link to your github or simply click the icon below<br><i class='fa fa-github" +
            " fa-2x'></i>",
            html: true,
            type: "input",
            showCancelButton: true,
            closeOnConfirm: false,
            animation: "slide-from-top",
            inputPlaceholder: "Link"
        }, function (inputValue) {
            if (inputValue === false) return false;
            if (inputValue === "") {
                swal.showInputError("You need to write something!");
                return false
            }
            $.ajax({
                url: '/profileGitlink',
                data: {githublink: inputValue},
                type: 'POST',
                success: function (response) {
                    swal({
                        imageUrl: '../static/img/thumbs-up.jpg',
                        title: "Github Link Added Successfully",
                        text: "It has been added to your public profile"
                    });
                },
                error: function (error) {
                    console.log(error);
                }
            });
        });
    });

});
