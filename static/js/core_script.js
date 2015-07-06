$(function () {
    $('.comment-success').hide();
    $('.upload_loader').hide();
    $('.upload-success').hide();

    $('.home-btn').click(function () {
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

    $('.profile-btn').click(function () {
        $.ajax({
            url: '/profileInfo',
            data: $('#profile-form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        })
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


    //AUTOCOMPLETE TAG
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
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }

    $( "#tags" )
      // don't navigate away from the field on tab when selecting an item
      .bind( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        minLength: 0,
        source: function( request, response ) {
          // delegate back to autocomplete, but extract the last term
          response( $.ui.autocomplete.filter(
            availableTags, extractLast( request.term ) ) );
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          // add placeholder to get the comma-and-space at the end
          //terms.push( "" );
          this.value = terms.join( ", " );
            console.log(terms);
          return false;
        }
      });

});
