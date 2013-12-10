var ItemsTemplate = null;

var SearchButton = function(container){
    this.form = container.find('form');

    this.search = function(event){
        event.preventDefault(); //prevent default form submit

        $.ajax({
            type: 'GET',
            url: $(this).attr('action'),
            context: container,
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response){
                //console.log('Success: ' + response);

                var total = response.ResultSet['@attributes'].totalResultsAvailable;
                var per_query = response.ResultSet['@attributes'].totalResultsReturned;

                console.log('total: ' + total);
                console.log('pages: ' + Math.ceil(total/per_query));

                container.find('#test-box').val(JSON.stringify(response.ResultSet));
                container.find('#pages').val(Math.ceil(total/per_query));


                var output = Mustache.render(ItemsTemplate, response.ResultSet.Result);

                container.find('#ajax-result').hide().html(output).fadeIn();
            },
            error: function(request, errorType, errorMessage){
                console.log('Error: ' + errorType + ' with message: ' + errorMessage);
            },
            beforeSend: function(){

            },
            complete: function(){

                $(document).endlessScroll({
                    inflowPixels: 300,
//                    fireOnce: true,
//                    fireDelay: 100,
                    ceaseFireOnEmpty: false,
                    callback: function(fireSequence, pageSequence, scrollDirection) {
                        console.log('callback:', fireSequence, pageSequence, scrollDirection)
                        var pages = parseInt($('.container').find('#pages').val());

                        if (fireSequence >= pages){
                            console.log('callback -> true');
                            return true;
                        }

                        var form = $('.container').find('form');

                        $.ajax({
                            type: 'GET',
                            url: form.attr('action'),
                            data: form.serialize() + '&page=' + fireSequence,
                            dataType: 'json',
                            success: function(response){
                                console.log('Success: ' + response);

                                $('.container').find('#test-box').val(JSON.stringify(response.ResultSet));

                                var output = Mustache.render(ItemsTemplate, response.ResultSet.Result);
            //                    return output;
                                var last = $("ul#ajax-result li:last");
                                last.after(output);

                            },
                            error: function(request, errorType, errorMessage){
                                console.log('Error: ' + errorType + ' with message: ' + errorMessage);
                            },
                            beforeSend: function(){

                            },
                            complete: function(){

                            }
                        })



                    },
                    ceaseFire: function(fireSequence, pageSequence, scrollDirection){
                        console.log('ceaseFire:', fireSequence, pageSequence, scrollDirection)
                        var pages = parseInt($('.container').find('#pages').val());

                        if (fireSequence >= pages){
                            console.log('ceaseFire -> true');
                            return true;
                        }
                        console.log('ceaseFire -> false');
                        return false;
                    }
//                    intervalFrequency: 5
                });

            }
        })

    }

    this.form.on('submit', this.search)
}


$(document).ready(function(){
    var yahoosearchform = new SearchButton($('.container'));
    $.get('/static/assets/templates/yahoolotList.mustache.html', function(template, textStatus, jqXhr) {
        ItemsTemplate = $(template).filter('#yahoolotListTpl').html()
    });
});
