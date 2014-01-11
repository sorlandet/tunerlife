/**
 * Created by Evgeniy on 02.01.14.
 */

var ajaxTranslateHandler = function(e) {
    e.preventDefault();
    var title = e.target;
    var translationAPI = '/translate/ajax/';
    $(title).removeClass('translate');
//    console.log(title);
    $.get( translationAPI, {title: title.innerHTML, sl: "ja", tl: "en"})
        .done(function( data ) {
//            console.log( "Data Loaded: " + data );
            if (data) {
              $(title).html(data);
            }
        }).fail(function( jqxhr, textStatus, error ) {
            var err = textStatus + ", " + error;
            console.log( "Request Failed: " + err );
        });
}