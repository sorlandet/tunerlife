var SearchButton = function(container){
    this.form = container.find('form');

    this.search = function(event){
        event.preventDefault(); //prevent default form submit

        var paramObj = {};
        $.each($(this).serializeArray(), function(_, kv) {
            if (paramObj.hasOwnProperty(kv.name)) {
                paramObj[kv.name] = $.makeArray(paramObj[kv.name]);
                paramObj[kv.name].push(kv.value);
            }
            else {
                paramObj[kv.name] = kv.value;
            }
        });

        paramObj.aucminprice = Number(paramObj.aucminprice).calculateInYens(0.33);
        paramObj.aucmaxprice = Number(paramObj.aucmaxprice).calculateInYens(0.33);

        window.searchData = paramObj;

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            context: container,
            data: window.searchData,
            traditional: true,
            dataType: 'json',
            success: function(response){

                var total = response.ResultSet['@attributes'].totalResultsAvailable;
                var per_query = response.ResultSet['@attributes'].totalResultsReturned;

                window.Pages = Math.ceil(total / per_query);

                $('#totalResultsAvailable').html(total);
                //$('#totalResultsReturned').html(per_query)
                //$('#totalPages').html(Math.ceil(total / per_query))

                //console.log('total: ' + total);
                //console.log('pages: ' + window.Pages);

                $(document).trigger('ajaxResponse', response);


            },
            error: function(request, errorType, errorMessage){
                console.log('Error: ' + errorType + ' with message: ' + errorMessage);
            },
            beforeSend: function(){
                container.find('#test-box').val('');
                container.find('#ajax-result').html('');
                container.find('#for-comparison').html('');

                $('#totalResultsAvailable').html('0');
                $('#totalLotsForComparison').html('0');
            },
            complete: function(){
                $(document).simpleInfiniteScroll({
                    threshold: 200,
                    method: 'post',
                    url: $('#searchForm').attr('action'),
                    totalPagesNumber: window.Pages,
                    ajaxData: window.searchData,
                    newPageLoaded: ajaxResponseHandler
                });
            }
        })

    }

    this.form.on('submit', this.search)
}

var ajaxResponseHandler = function(e, response) {
    if (typeof response.ResultSet != "undefined"){
        $('#test-box').val(JSON.stringify(response.ResultSet));

        if (typeof response.ResultSet.Result != "undefined"){
            var list = response.ResultSet.Result;

            if (typeof list.Item != "undefined"){
                list.Item.forEach(function(entry) {
                    var rusMoment = moment(entry.EndTime).lang('ru');
                    rusMoment.lang()._relativeTime.s = "секунды";
                    entry.ttl = rusMoment.fromNow(true);

                    entry.current_price = Number(entry.CurrentPrice).formatMoneyShort(2, '.', ' ');
                    entry.buyout_price = Number(entry.BidOrBuy).formatMoneyShort(2, '.', ' ');
                    entry.current_price_rubles = Number(entry.CurrentPrice).calculateInRubles(0.33).formatMoneyShort(2, '.', ' ');;
                });
                var data = Mustache.render(window.ItemsTemplate, list)
                var lots = $("div#ajax-result").children();
                if (lots.length == 0) {
                    $("div#ajax-result").html(data);
                }
                lots.last().after(data);
                $('.title.translate').each(function() {
                    $(this).trigger('ajaxTranslate');
                });
            }
        }
    }
};



$('#myTab a:first').tab('show');


$(document).on('ajaxResponse', ajaxResponseHandler);
$(document).on('ajaxTranslate', ajaxTranslateHandler);
//$(document).on('click', '.title', ajaxTranslateHandler);

$(document).on('click', '.to-compare', function(e){
    e.preventDefault();
    var lot = $(this).closest($('.lot'));
    var lots = $("div#for-comparison").children();
    if (lots.length == 0) {
        $("div#for-comparison").html(lot);
    }
    lots.last().after(lot);

    var total = parseInt($('#totalLotsForComparison').html());
    $('#totalLotsForComparison').html(total + 1);
});

$(document).ready(function(){

    var yahoosearchform = new SearchButton($('.container'));
    $.get('/static/assets/templates/yahoolotList.mustache.html', function(template, textStatus, jqXhr) {
        window.ItemsTemplate = $(template).filter('#yahoolotListTpl').html();
    });

    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });

    $('.scrollup').click(function(){
        $("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    });

    window.searchData = null;


    $('#myTab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    })





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
