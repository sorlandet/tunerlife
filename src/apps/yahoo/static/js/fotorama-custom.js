$(function () {
    $(".js-arrow").on("mousedown", function (o) {
        o.preventDefault();
        var t = $(this),
            a = t.data(),
            n = $(a.fotorama).data("fotorama");
        n && n.show({
            index: a.show,
            slow: o.altKey
        })
    })
}), window.console = window.console || {
    log: $.noop
}, $(function () {
    var o = $(".fotorama-frontpage");
    o[0] && ($(window).width() > 768 && $("a", o).each(function () {
        var o = $(this);
        o.attr("href", o.attr("href").replace("-lo.jpg", ".jpg"))
    }), console.log("# Fotorama events"), o.on("fotorama:ready fotorama:show fotorama:showend fotorama:load fotorama:error fotorama:fullscreenenter fotorama:fullscreenexit ", function (o, t, a) {
        console.log("## " + o.type), a && a.src || console.log("active image: " + t.activeFrame.img), a && (a.time && console.log("transition duration: " + Math.round(a.time) + "ms"), a.src && console.log(("fotorama:load" === o.type ? "loaded" : "broken") + " image: " + a.src)), console.log("")
    }).fotorama({
        spinner: {
            color: "rgba(255, 255, 255, .75)"
        }
    }).parent().next(".photos-by").show())
}), $(function () {
    $(".js-set-options").on("change", function () {
        var o = $($(this).data("fotorama")).data("fotorama"),
            t = {};
        o && ($(":input", this).each(function () {
            var o = $(this);
            t[o.attr("name")] = "checkbox" === o.attr("type") ? o.is(":checked") : o.val()
        }), o.setOptions(t))
    })
}), $(function () {
    $(".js-shuffle").on("click", function (o) {
        o.preventDefault();
        var t = $(this),
            a = $(t.attr("data-fotorama")).data("fotorama");
        a && a.shuffle()
    })
}), $(function () {
    $(".js-transition-switch").on("click", function (o) {
        o.preventDefault();
        var t = $(this),
            a = $(t.attr("data-fotorama")).data("fotorama");
        a && (t.addClass("active inverse").siblings().removeClass("active inverse"), a.setOptions({
            transition: t.text().toLowerCase()
        }))
    })
});