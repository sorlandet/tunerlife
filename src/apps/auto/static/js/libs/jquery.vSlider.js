$j.fn.extend({
	vSlider:function(opt){
		opt=$j.extend({prev:'.v_prev',next:'.v_next',easing:'',duration:'normal',items:'.gn_static_1',keeper:'.keeper',show:4},opt)
		var ke=$j(opt.keeper,this),i,
			it=$j('>'+opt.items,ke),
			keH=0,lsI,
			slide=function(){
				ke.stop().animate({top:'-'+$j('>.current',ke).attr('offsetTop')+'px'},opt.duration,opt.easing)
			}
		for(i=0;i<opt.show;i++)
			keH+=parseInt(it.eq(i).outerHeight())
		ke.parent().css({overflow:'hidden',height:keH+'px',position:'relative'})
		ke.css({position:'relative',top:0})
		it.eq(0).addClass('current')
		it.eq(-opt.show).addClass('lastItem')
		lsI=$j('>.lastItem',ke).attr('offsetTop')
		ke.parent().bind('vSliderNext',function(){
			var t
			if((t=$j('>.current',ke).next()).length)
				t.addClass('current').siblings().removeClass('current')
			else
				ke.find('>.gn_static_1').removeClass('current').eq(0).addClass('current')
			if(-parseInt(ke.css('top'))>=lsI)it.eq(0).addClass('current').siblings().removeClass('current')
			slide()
			return false
		})
		ke.parent().bind('vSliderPrev',function(){
			var t
			if((t=$j('>.current',ke).prev()).length)
				t.addClass('current').siblings().removeClass('current')
			else
				ke.find('>.gn_static_1').removeClass('current').eq(-opt.show).addClass('current')
			slide()
			return false
		})
		$j(opt.next).bind('click',function(){
			ke.parent().trigger('vSliderNext')
			return false
		})
		$j(opt.prev).bind('click',function(){
			ke.parent().trigger('vSliderPrev')
			return false
		})
	}
})