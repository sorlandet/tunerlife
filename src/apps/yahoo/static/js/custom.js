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

                var template = '<li class="span3"> \
                <div class="thumbnail border-radius-top"> \
                    <div class="bg-thumbnail-img"> \
                        <img class="border-radius-top" src="{{ Image }}"> \
                    </div> \
                    <h5><a href="{{ AuctionItemUrl }}">{{ Title }}</a></h5> \
                </div> \
                <div class="box border-radius-bottom"> \
                    <p> \
                        <span class="title_torrent pull-left pull-left">ET</span> \
                        <span class="number-view pull-right">{{ EndTime }}</span> \
                    </p> \
                </div> \
            <div class="box border-radius-bottom"> \
                    <p> \
                        <span class="title_torrent pull-left pull-left">Bids</span> \
                        <span class="number-view pull-right">{{ Bids }}</span> \
                    </p> \
                </div> \
            <div class="box border-radius-bottom"> \
                    <p> \
                        <span class="title_torrent pull-left pull-left">Price</span> \
                        <span class="number-view pull-right">{{ CurrentPrice }}</span> \
                    </p> \
                </div> \
            </li>'
                var output = Mustache.render("{{#Item}}" + template + "{{/Item}}", response.ResultSet.Result);

                container.find('#ajax-result').hide().html(output).fadeIn();
            },
            error: function(request, errorType, errorMessage){
                console.log('Error: ' + errorType + ' with message: ' + errorMessage);
            },
            beforeSend: function(){

            },
            complete: function(){

            }
        })

    }

    this.form.on('submit', this.search)
}





$(document).ready(function(){
    var yahoosearchform = new SearchButton($('.container'));
});


$(function() {
    $(document).endlessScroll({
        bottomPixels: 100,
        fireOnce: true,
        fireDelay: 100,
        callback: function(fireSequence) {
            console.log('fireSequence: ' + fireSequence)

            var form = $('.container').find('form');

            $.ajax({
                type: 'GET',
                url: form.attr('action'),
                data: form.serialize() + '&page=' + fireSequence,
                dataType: 'json',
                success: function(response){
                    console.log('Success: ' + response);
//                    container.find('#test-box').val(JSON.stringify(response.ResultSet));

                    var template = '<li class="span3"> \
                    <div class="thumbnail border-radius-top"> \
                        <div class="bg-thumbnail-img"> \
                            <img class="border-radius-top" src="{{ Image }}"> \
                        </div> \
                        <h5><a href="{{ AuctionItemUrl }}">{{ Title }}</a></h5> \
                    </div> \
                    <div class="box border-radius-bottom"> \
                        <p> \
                            <span class="title_torrent pull-left pull-left">ET</span> \
                            <span class="number-view pull-right">{{ EndTime }}</span> \
                        </p> \
                    </div> \
                <div class="box border-radius-bottom"> \
                        <p> \
                            <span class="title_torrent pull-left pull-left">Bids</span> \
                            <span class="number-view pull-right">{{ Bids }}</span> \
                        </p> \
                    </div> \
                <div class="box border-radius-bottom"> \
                        <p> \
                            <span class="title_torrent pull-left pull-left">Price</span> \
                            <span class="number-view pull-right">{{ CurrentPrice }}</span> \
                        </p> \
                    </div> \
                </li>'
                    var output = Mustache.render("{{#Item}}" + template + "{{/Item}}", response.ResultSet.Result);

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
        ceaseFire: function(fireSequence){
            console.log('ceaseFire fireSequence: ' + fireSequence)
            var pages = $('.container').find('#pages').val();

            if (fireSequence >= pages){
                return true;
            }

            return false;
        }
    });
});

