$(function () {
    $('.comment-success').hide();
    $('.update-success').hide();
    $('.update-failure').hide();
    $('.upload_loader').hide();
    $('.upload-success').hide();
    $('.upload-failure').hide();
    $('.vip-check-mark').hide();

    //UPDATE PROFILE
    $('.profile-btn').click(function () {
        $('#profile-btn').text('UPDATING.....').attr('disabled', 'disabled');
        $.ajax({
            url: '/profileInfo',
            data: $('#profile-form').serialize(),
            type: 'POST',
            success: function (response) {
                $('.update-success').show("drop", {direction: "down"}, "slow");
                $('#profile-btn').text('UPDATE PROFILE').attr('disabled', false);

            },
            error: function (error) {
                $('.update-failure').show("drop", {direction: "down"}, "slow");
            }
        });
        setTimeout(function () {
            $('.update-success').hide();
        }, 3000)
    });

    //VIP MEMBER CODE CHECK
    $('.btn-coupon').click(function () {
        $.ajax({
            url: '/getVipCode',
            data: $('#vip-form').serialize(),
            type: 'POST',
            success: function (response) {
                $('.vip-check-mark').show();
                $('.btn-coupon').text('Verified Vip');
                setTimeout(function () {
                    $('.coupon').hide();
                    $('.profile-social-verified').show("drop", {direction: "down"}, "slow");
                    $('.success-vip-message').text('Verified Vip').show("drop", {direction: "down"}, "slow");
                }, 5000);
            },
            error: function (error) {
                return error;
            }
        })
    });

    //RUN SEARCH ON KEY PRESS
    var search = $("#search");
    search.keyup(function () {
        $.get("/queryroute/" + search.val(), function (result) {
            result = jQuery.parseJSON(result);
            hits = result;
            hitsLength = hits.length;
            $('.upload_loader').show();
            if (hits.length > 0) {
                var result_html = '';
                result_html += hitsLength + ' results found <p><a href="/search/' + search.val() + '">View Search Results</a></p>';
                setTimeout(function () {
                    $('.upload_loader').hide();
                    $("#search_results").html(result_html);
                }, 300)

            } else {
                $('.upload_loader').hide();
                $("#search_results").html("Nothing Found");
            }
        })
    });
    //SUBMIT CNTACT FORM
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
        "Apache Spark",
        "AngularJs",
        "AppleScript",
        "Assembly",
        "Asp",
        "BASIC",
        "Bootstrap",
        "Brainfuck",
        "C",
        "C sharp",
        "C++",
        "Clojure",
        "CoffeeScript",
        "COBOL",
        "Cobra",
        "ColdFusion",
        "Common Lisp",
        "D3",
        "DotNet",
        "Erlang",
        "ExpressJs",
        "Firebase",
        "Fortran",
        "GO",
        "Groovy",
        "Haskell",
        "Ionic",
        "J",
        "Java",
        "JavaScript",
        "JavaFX Script",
        "Jquery",
        "Julia",
        "Kamailio Script",
        "K",
        "Kitten",
        "Laravel",
        "Lisp",
        "LiveScript",
        "LOLCODE",
        "LotusScript",
        "Lua",
        "Lucid",
        "MATLAB",
        "MongoDb",
        "MySQL",
        "NodeJs",
        "Objective-C",
        "Perl",
        "PHP",
        "PowerShell",
        "Python",
        "R",
        "Ruby",
        "Scala",
        "Scheme",
        "SheerPower 4GL",
        "Shiny",
        "Swift",
        "UNIX Shell",
        "Visual Basic"
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
                return false;
            }
        });

    //Autocomplete to select only one language
    $("#major_skill").autocomplete({
        source: availableTags
    });

    //-------------------------------TOOLTIP------------------
    $('[data-toggle="tooltip"]').tooltip();


    //----------------------------SOCIAL LINKS-----------------

    function ConfigSocialLink(btnClass, swalTitle, swalText, swalInputPlaceholder, ajaxUrl, successClassId,
                              swalSuccessTitle, successClassIdHtml, twitterClassLink) {
        $(btnClass).click(function () {
            return swal({
                title: swalTitle,
                text: swalText,
                type: "input",
                html: true,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: swalInputPlaceholder
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError("You need to write something!");
                    return false;
                }
                $.ajax({
                    url: ajaxUrl,
                    data: {ajaxDataJsObj: inputValue},
                    type: 'POST',
                    success: function (response) {
                        link = jQuery.parseJSON(response);
                        $(successClassId).attr('href', link.details[0]).show("drop", {direction: "up"}, "slow");
                        $(successClassId).text(link.details[0]).show("drop", {direction: "up"}, "slow");
                        $(successClassIdHtml).html("<a href=" + link.details[0] + ">" + link.details[0] + "</a>").show("drop", {direction: "up"}, "slow");
                        if (twitterClassLink) {
                            $('.profile-twitter-link').attr('href', 'https://twitter.com/' + link.details[0]).show("drop",
                                {direction: "up"}, "slow");
                            $(twitterClassLink).text(link.details[0]).show("drop", {direction: "up"}, "slow");
                        }
                        swal({
                            imageUrl: '../static/img/thumbs-up.jpg',
                            title: swalSuccessTitle,
                            text: "It has been added to your public profile"
                        });

                    },
                    error: function (error) {
                        console.log(error);
                    }
                });

            });
        });
    }

    //Website
    ConfigSocialLink('.website-btn', 'Website Link', 'Please put in the link to your website', 'http://->Link',
        '/profileWeblink', '.profile-website-link', 'Link Added Successfully');
    //github
    ConfigSocialLink('.github-btn', 'Github Link', 'Please put in the link to your github or simply click the icon' +
        'below<br><a href=\'/gitconnect\'><i class=\'fa fa-github fa-2x\'></i></a>', 'Please enter your github' +
        ' profile link', '/profileGitlink', '.profile-github-link', 'Github Link Added Successfully', '.git span');

    //twitter
    ConfigSocialLink('.twitter-btn', 'Twitter Link', 'Please put in your twitter username or simply click the icon' +
        ' below<br><a href=\'/twitconnect\'> <i class=\'fa fa-twitter fa-2x\'></i></a>', 'Username(no need for the' +
        ' @symbol)', '/profileTweetLink', '.profile-twitter-link', 'Twitter username Added Successfully', '', '.tweet' +
        ' span');


});
