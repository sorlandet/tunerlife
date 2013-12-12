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

        $.ajax({
            type: 'GET',
            url: $(this).attr('action'),
            context: container,
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response){

                var total = response.ResultSet['@attributes'].totalResultsAvailable;
                var per_query = response.ResultSet['@attributes'].totalResultsReturned;

                window.Pages = Math.ceil(total / per_query);

                console.log('total: ' + total);
                console.log('pages: ' + window.Pages);

                container.find('#test-box').val(JSON.stringify(response.ResultSet));

                var list = response.ResultSet.Result;
                list.Item.forEach(function(entry) {
                    entry.ttl = moment(entry.EndTime).lang('ru').fromNow();
                    entry.current_price =  Number(entry.CurrentPrice).formatMoney(2, '.', ' ');
                    entry.current_price_rubles = Number(entry.CurrentPrice * 0.319020012).formatMoney(2, '.', ' ');
                });

                var output = Mustache.render(window.ItemsTemplate, list);

                container.find('#ajax-result').html(output)
            },
            error: function(request, errorType, errorMessage){
                console.log('Error: ' + errorType + ' with message: ' + errorMessage);
            },
            beforeSend: function(){
                container.find('#test-box').val('');
                container.find('#ajax-result').html('');
            },
            complete: function(){
                $(document).simpleInfiniteScroll({
                    threshold: 200,
                    method: 'get',
                    url: $('#searchForm').attr('action'),
                    totalPagesNumber: window.Pages,
                    ajaxData: $('#searchForm').serialize(),
                    newPageLoaded: function(e, response) {
                        //console.log('newPageLoaded', response);

                        if (typeof response.ResultSet != "undefined"){
                            $('.container').find('#test-box').val(JSON.stringify(response.ResultSet));

                            if (typeof response.ResultSet.Result != "undefined"){
                                var list = response.ResultSet.Result;

                                if (typeof list.Item != "undefined"){
                                    list.Item.forEach(function(entry) {
                                        entry.ttl = moment(entry.EndTime).lang('ru').fromNow();
                                        entry.current_price =  Number(entry.CurrentPrice).formatMoney(2, '.', ' ');
                                        entry.current_price_rubles = Number(entry.CurrentPrice * 0.319020012).formatMoney(2, '.', ' ');
                                    });

                                    $("div#ajax-result div.lot:last")
                                        .after(Mustache.render(window.ItemsTemplate, list));
                                }
                            }
                        }
                    }
                });
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
