Number.prototype.formatMoney = function(c, d, t){
    var n = this,
    c = isNaN(c = Math.abs(c)) ? 2 : c,
    d = d == undefined ? "." : d,
    t = t == undefined ? "," : t,
    s = n < 0 ? "-" : "",
    i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "",
    j = (j = i.length) > 3 ? j % 3 : 0;
   return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
 };



var SearchButton = function(container){
    this.form = container.find('form');

    this.search = function(event){
        event.preventDefault(); //prevent default form submit

        window.searchData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            context: container,
            data: window.searchData,
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
        $('.container').find('#test-box').val(JSON.stringify(response.ResultSet));

        if (typeof response.ResultSet.Result != "undefined"){
            var list = response.ResultSet.Result;

            if (typeof list.Item != "undefined"){
                list.Item.forEach(function(entry) {
                    entry.ttl = moment(entry.EndTime).lang('ru').fromNow();
                    entry.current_price =  Number(entry.CurrentPrice).formatMoney(2, '.', ' ');
                    var end_price = entry.CurrentPrice * 1.05 + 5000 + 24000 + 500
                    entry.current_price_rubles = Number(end_price * 0.33).formatMoney(2, '.', ' ');
                });
                var data = Mustache.render(window.ItemsTemplate, list)
                var lots = $("div#ajax-result").children();
                if (lots.length == 0) {
                    $("div#ajax-result").html(data);
                }
                lots.last().after(data);
                $('.title').each(function() {
                    $(this).trigger('ajaxTranslate');
                });
            }
        }
    }
};

var ajaxTranslateHandler = function(e) {
    e.preventDefault();
    var title = e.target;
    var translationAPI = '/translate/ajax/';
    //console.log(title);
    $.get( translationAPI, {title: title.innerHTML, sl: "ja", tl: "ru"})
        .done(function( data ) {
            console.log( "Data Loaded: " + data );
            $(title).html(data);
        }).fail(function( jqxhr, textStatus, error ) {
            var err = textStatus + ", " + error;
            console.log( "Request Failed: " + err );
        });
}

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
