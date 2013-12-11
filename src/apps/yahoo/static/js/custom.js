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
                console.log('success');

                var total = response.ResultSet['@attributes'].totalResultsAvailable;
                var per_query = response.ResultSet['@attributes'].totalResultsReturned;

                window.Pages = Math.ceil(total / per_query);

                console.log('total: ' + total);
                console.log('pages: ' + window.Pages);

                container.find('#test-box').val(JSON.stringify(response.ResultSet));
                var list = response.ResultSet.Result;

                list.Item.forEach(function(entry) {
                    entry.ttl = moment(entry.EndTime).lang('ru').fromNow();
                });

                var output = Mustache.render(window.ItemsTemplate, list);

                container.find('#ajax-result').html(output)
            },
            error: function(request, errorType, errorMessage){
                console.log('Error: ' + errorType + ' with message: ' + errorMessage);
            },
            beforeSend: function(){
                console.log('beforeSend');

                window.Pages = 0;
                window.EndlessScroll.firing = false;
                window.EndlessScroll.fireSequence = 0;
                window.EndlessScroll.pageSequence = 0;
                window.EndlessScroll.nextSequence = 1;
                window.EndlessScroll.prevSequence = -1;
                window.EndlessScroll.lastScrollTop = 0;
                window.EndlessScroll.didScroll = false;
                window.EndlessScroll.isScrollable = true;

                container.find('#test-box').val('');
                container.find('#ajax-result').html('');
            },
            complete: function(){
                console.log('complete');
                window.EndlessScroll.firing = true;
            }
        })

    }

    this.form.on('submit', this.search)
}


$(document).ready(function(){
    var yahoosearchform = new SearchButton($('.container'));
    $.get('/static/assets/templates/yahoolotList.mustache.html', function(template, textStatus, jqXhr) {
        window.ItemsTemplate = $(template).filter('#yahoolotListTpl').html();
    });

    window.EndlessScroll = new EndlessScroll($(document), {
        inflowPixels: 350,
        //fireOnce: true,
        //fireDelay: 100,
        ceaseFireOnEmpty: false,
        callback: function(fireSequence, pageSequence, scrollDirection) {
            console.log('callback:', fireSequence, pageSequence, scrollDirection);

            if (fireSequence >= window.Pages || scrollDirection != 'next'){
                console.log('callback -> true', fireSequence);
                return true;
            }

            var form = $('.container').find('form');

            $.ajax({
                type: 'GET',
                url: form.attr('action'),
                data: form.serialize() + '&page=' + fireSequence,
                dataType: 'json',
                success: function(response){
                    console.log('callback -> ajax -> success');

                    $('.container').find('#test-box').val(JSON.stringify(response.ResultSet));

                    list.Item.forEach(function(entry) {
                        entry.ttl = moment(entry.EndTime).lang('ru').fromNow();
                    });

                    var output = Mustache.render(window.ItemsTemplate, list);

                    $("div#ajax-result div.lot:last").after(
                        Mustache.render(ItemsTemplate, output)
                    );

                },
                error: function(request, errorType, errorMessage){
                    console.log('Error: ' + errorType + ' with message: ' + errorMessage);
                },
                beforeSend: function(){
                    console.log('callback -> ajax -> beforeSend');
                },
                complete: function(){
                    console.log('callback -> ajax -> complete');
                }
            })



        },
        ceaseFire: function(fireSequence, pageSequence, scrollDirection){
            //console.log('ceaseFire:', fireSequence, pageSequence, scrollDirection)

            if (fireSequence >= window.Pages){
                return true;
            }

            return false;
        }
    });

    window.EndlessScroll.run();


//    console.log(moment('2013-12-11T18:17:42+09:00').format('MMMM Do YYYY, h:mm:ss a'));
//    console.log(moment('2013-12-11T18:17:42+09:00').format('dddd'));
//    console.log(moment('2013-12-11T18:17:42+09:00').format("MMM Do YY"));
//    console.log(moment('2013-12-11T18:17:42+09:00').format('YYYY [escaped] YYYY'));
//    console.log(moment('2013-12-11T18:17:42+09:00').format());
//    console.log(moment('2013-12-11T18:17:42+09:00').zone());
//    console.log(moment('2013-12-11T18:17:42+09:00').fromNow());
//    console.log(moment('2013-12-11T18:17:42+09:00').fromNow(true));
//    console.log(moment('2013-12-11T18:17:42+09:00').fromNow(false));
});
