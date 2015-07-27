$(function () {
    $('#tag-loader').hide();
    //CONSUME GITHUB AND MANIPULATE DOM EXTENSIVELY
    PATH_TO_CALL_API = '/devtools';
    if (window.location.pathname === '/devtools') {
        $('#tag-loader').show();
        $.get('/devjson', function (data) {

                $('#tag-loader').hide();


            var parseResult, count = '';
            _.forEach(data, function (result) {
                parseResult = JSON.parse(result)
            });

            $.each(parseResult, function (key, value) {
                count = value;
                li = '<li class="stepped-tech">' + count.category + '</li>';
                ul = $('.tech-tag-list').append(li);
            });

            $('.stepped-tech').click(function () {
                $("#toggle").toggle("fadeOut");
                var ideLink = '';
                thisList = $(this).text();

                //create element after click, so ide-block doesn't so one first page load
                var CreateElem = $('<br/><br/><div class="tech-ide"><h4>IDE\'s</h4>' +
                    '<hr/>');

                $.each(parseResult, function (key, value) {
                    if (thisList == value.category) {
                        $('#tech-lang').text(value.category);
                        $('#tech-about').text(value.about);
                        $('#append-others').html(CreateElem);

                        //loop through ides and ide links
                        for (var i = 0; i < value.IDE.length; i++) {
                            var valueIde = value.IDE[i];
                            for (ide in valueIde) {
                                ideLink = valueIde[ide];
                            }
                            $('#tech-ide').remove();
                            $('#append-others').append('<ul><li><a href=' + ideLink + ' target="_blank">' + ide + '</a></ul></li>');
                        }
                    }
                });

                $("#toggle").toggle("fadeIn");
            });
        });
    }
});