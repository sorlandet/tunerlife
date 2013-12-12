(function($) {

var InfiniteScroll = function(target, total, threshold, url, method, data) {
    //console.log(target, total, threshold, url, method, data);

    this.target = target;
    this.page = 1;
    this.total = total;
    this.threshold = threshold;
    this.url = url;
    this.data = data;
    this.method = method;

    this.target.scroll($.proxy(this.scroll, this));
};

InfiniteScroll.prototype = {
    constructor: InfiniteScroll,
    loadPage: function() {
        var target = this.target, url = this.url;

        this.page++;

        this._loading = $[this.method](url, this.getData())
                .success(function(data) { target.trigger('pageLoaded', data); });

        if (this.page === this.total) {
            this.target.off('scroll');
        }
    },
    scroll: function() {

        if (!this._loading || this._loading.state() == "resolved") {

            var innerWrap = $(document);
            var margin = innerWrap.height() - this.target.height() <= this.target.scrollTop() + this.threshold;

            if (margin) {
                this.loadPage();
            }
        }
    },
    getData: function() {

        if (!this.data) {
            return { page: this.page };
        }
        if (this.data instanceof Object) {
            this.data.page = this.page;
            return this.data;
        } else {
            return [this.data, '&page=', this.page].join('');
        }
    }
};

$.fn.simpleInfiniteScroll = function(options) {

    var infScroll = new InfiniteScroll(this, options.totalPagesNumber, options.threshold, options.url, options.method, options.ajaxData);

    this.data('infiniteScroll', infScroll)
        .on('pageLoaded', options.newPageLoaded);

    return this;
};

}(jQuery));
