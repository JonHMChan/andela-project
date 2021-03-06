$(function () {
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


    //disable enter key press for code validation
    $('#vip-check').keydown(function (event) {
        var x = event.which;
        console.log(x);
        if (x === 13) {
            event.preventDefault();
        }
    });

    //VIP MEMBER CODE CHECK
    $('.btn-coupon').click(function () {
        if ($('#vip-check').val().length > 0) {
            $.ajax({
                url: '/getVipCode',
                data: $('#vip-form').serialize(),
                type: 'POST',
                success: function (response) {
                    $('.vip-check-mark').show();
                    $('.btn-coupon').text('Verified Vip');
                    $('.vip-message-style').attr('class', 'vip-message-style bg-success').text('Approved');//if showing already
                    setTimeout(function () {
                        $('.coupon').hide();
                        $('.profile-social-verified').show("drop", {direction: "down"}, "slow");
                        $('.success-vip-message').text('Verified Vip').show("drop", {direction: "down"}, "slow");
                    }, 5000);
                },
                error: function (error) {
                    $('.vip-message').attr('class', 'vip-message-style bg-danger').text('Sorry Invalid Code').show();
                }
            })
        } else {
            alert('Please enter code');
        }

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
        $('.home-btn').text('Sending...');
        $.ajax({
            url: '/homeContact',
            data: $('#contact-form').serialize(),
            type: 'POST',
            success: function (response) {
                $('.home-btn').text('SEND MESSAGE');
                $('.comment-success').show("drop", {direction: "up"}, "slow").text('Comment Successfully Sent');
                $('#contact-form').each(function () {
                    this.reset();
                });
                grecaptcha.reset();
            },
            error: function (error) {
                $('.home-btn').text('SEND MESSAGE');
                grecaptcha.reset();
                $('.comment-failure').show("drop", {direction: "up"}, "slow").text('Error Occured, please check all fields and accept captcha');
            }
        });
        setTimeout(function () {
            $('.comment-success').hide();
            $('.comment-failure').hide();
        }, 5000);
    });

//iMAGE CONFIGURATION
    var ImageValidation = {
        imageInputField: $('#file_field'),

        init: function () {
            this.disableIfNoFile();
            this.watchForChange();
            this.sendImage();
        },

        checkImgFileExt: function () {
            var ext = this.imageInputField.val().split('.').pop().toLowerCase();
            if ($.inArray(ext, ['gif', 'png', 'jpg', 'jpeg']) == -1) {
                $('.invalid-file-format').html('<p class="text-danger">Invalid File Type</p>').show();
                return false;
            }
        },

        disableIfNoFile: function () {
            if (this.imageInputField.val() === '') {
                $('.image-btn').attr('disabled', 'disabled');
            }
        },

        watchForChange: function () {
            this.imageInputField.change(function () {
                var checkExt = ImageValidation.checkImgFileExt();
                if ($(this).val() !== '' && checkExt !== false) {
                    $('.invalid-file-format').hide();
                    $('.image-btn').attr('disabled', false).attr('class', 'btn btn-block btn-dark profile-btn btn-success');
                }
            });
        },

        sendImage: function () {
            //------------------------------CLOUDINARY IMAGE UPLOAD
            $('.image-btn').click(function () {
                $('.upload_loader').attr('src', "static/img/ajax-loader.gif");

                var form_data = new FormData($('#image-form')[0]);

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
                        $('.upload-success').text('Image Successfully Uploaded').show();
                        return true;
                    },
                    error: function (error) {
                        $('.upload-failure').text('Error, please try again').show();
                        return false;
                    }
                });
                $('.upload_loader').hide();
            });
        }
    };
    ImageValidation.init();


    //----------------------------------AUTOCOMPLETE TAG
    var availableTags =
        ["ActionScript", "Agile", "Apache Spark", "AngularJs",
            "AppleScript", "Assembly", "Asp", "BASIC", "Bootstrap",
            "Brainfuck", "C", "CSS", "C sharp", "C++", "Clojure",
            "CoffeeScript", "COBOL", "Cobra", "ColdFusion", "Common Lisp",
            "D3", "DotNet", "Django", "Erlang", "ExpressJs", "Firebase", "FLask", "Fortran",
            "GO", "Git","Graphics", "Groovy", "Haskell", "HTML", "Ionic", "J", "Java",
            "JavaScript", "JavaFX Script", "Jquery", "Julia",
            "Kamailio Script", "K", "Kitten", "Laravel", "Lisp",
            "LiveScript", "LOLCODE", "LotusScript", "Lua", "Lucid",
            "MATLAB", "MeteorJs", "MongoDb", "MySQL", "NodeJs",
            "Objective-C", "Perl", "Photoshop", "PHP", "PowerShell",
            "Python", "R", "Ruby", "Scala", "Scheme", "SheerPower 4GL",
            "Shiny", "Swift", "UNIX Shell", "Visual Basic"];

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
                            $('.profile-twitter-pub').attr('href', 'https://twitter.com/' + link.details[0]).show("drop",
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
                        swal({
                            title: 'Error Occured',
                            text: "Please try later"
                        });
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
        ' profile pub', '/profileGitlink', '.profile-github-pub', 'Github Link Added Successfully', '.git span');

    //twitter
    ConfigSocialLink('.twitter-btn', 'Twitter Link', 'Please put in your twitter username or simply click the icon' +
        ' below<br><a href=\'/twitconnect\'> <i class=\'fa fa-twitter fa-2x\'></i></a>', 'Username(no need for the' +
        ' @symbol)', '/profileTweetLink', '.profile-linkedin-pub', 'LinkedIn profile Link added', '', '.tweet' +
        ' span');

    //linkedin
    ConfigSocialLink('.linkedin-btn', 'Linkedin Profile', 'Please put in your linkedin profile public link', 'http://->Link',
        '/profileLinkedIn', '.profile-linked-link', 'LinkedIn profile Link successfuly Added', '', '.linkedin' +
        ' span');


});
