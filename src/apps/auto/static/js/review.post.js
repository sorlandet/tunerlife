
$j.getJSON('/ajax/review/image/tumbloader/', {'review_id': review_id },
	function(data) {
		$j.each(data, function(i, obj){
			attachedPostPhotos.push(obj.id);
			var thumb = 'iu-img' + obj.id;
			var photo = '<div class="iu-img" id="' + thumb + '" style="width: 120px; height: 90px; background-image: url(&quot;' + obj.tumb + '&quot;); visibility: visible; opacity: 1;"><ins><del><em id="' + obj.id + '">Удалить</em></del></ins></div>';

			$j("#photos_bar").append(photo);
		
		});
	}
);


// .po file like language pack
plupload.addI18n({
    'Select files' : 'Выберите файлы',
    'Add files to the upload queue and click the start button.' : 'Добавьте файлы в очередь загрузки и нажмите кнопку "Начать загрузку".',
    'Filename' : 'Имя файла',
    'Status' : 'Статус',
    'Size' : 'Размер',
    'Add files' : 'Добавить файлы',
    'Stop current upload' : 'Остановить загрузку',
    'Start uploading queue' : 'Начать загрузку',
    'Start upload' : 'Начать загрузку',
    'Drag files here.' : 'Перетяните файлы сюда.'
});


$j("#upload_btn").click(function() {
	$j("#uploader_container").show("slow");
});

$j("#upload_closebtn").click(function() {
	$j("#uploader_container").hide("slow");
});

$j("#uploader").pluploadQueue({
	// General settings ()
	runtimes : 'flash,html5',
	url : '/ajax/review/image/uploader/',
	max_file_size : '10mb',
	max_file_count: 20,
	chunk_size : '1mb',
	unique_names : true,
//		multiple_queues : true,
	preinit: attachCallbacks,
	
	// Resize images on clientside if we can
	resize : {width : 920, height : 615, quality : 90},

	// Specify what files to browse for
	filters : [	{title : "Изображения", extensions : "jpg,gif,png"}	],

	// Flash settings
	flash_swf_url : '/static/plupload/js/plupload.flash.swf'

});

// Client side form validation
$j('form').submit(function(e) {
	$j('#attachedPostPhotos').val(attachedPostPhotos);
//		var uploader = $('#uploader').pluploadQueue();
//		
//		// Validate number of uploaded files
//		if (uploader.total.uploaded == 0) {
//			// Files in queue upload them first
//			if (uploader.files.length > 0) {
//				// When all files are uploaded submit form
//				uploader.bind('UploadProgress', function() {
//					if (uploader.total.uploaded == uploader.files.length)
//						$('form').submit();
//				});
//				uploader.start();
//			} else
//				alert('You must at least upload one file.');
//
//			e.preventDefault();
//		}
	
});


$j('em').live('click', function(e) {
	var id =  $j(this).attr("id");
//		alert(id);
	attachedPostPhotos = attachedPostPhotos.filter(function(element, index, array) { return (element != id);})
	var thumb = '#iu-img' + id;
	$j(thumb).remove();
});

function attachCallbacks(Uploader) {
    Uploader.bind('FileUploaded', function(Up, File, Response) {
//			alert( Response.response );
		var obj = jQuery.parseJSON(Response.response);			
//			alert( obj.id )
		attachedPostPhotos.push(obj.id);
		var photo = '<div class="iu-img" id="' + obj.id + '" style="width: 120px; height: 90px; background-image: url(&quot;' + obj.tumb + '&quot;); visibility: visible; opacity: 1;"><ins><del><em>Удалить</em></del></ins></div>';

		$j("#photos_bar").append(photo);
//			$('#id_body').val($('#id_body').val() + '<br /><img src="' + obj.img + '">'); 
		
		var toAdd = tinyMCE.editors['id_body'].getContent() + '<br /><img src="' + obj.img + '">';
		tinyMCE.editors['id_body'].setContent(toAdd, {format : 'raw'})
//			alert(toAdd);
		
      });
};