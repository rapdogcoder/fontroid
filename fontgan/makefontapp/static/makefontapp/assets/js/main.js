/*
	Highlights by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$html = $('html');

	// Breakpoints.
		breakpoints({
			large:   [ '981px',  '1680px' ],
			medium:  [ '737px',  '980px'  ],
			small:   [ '481px',  '736px'  ],
			xsmall:  [ null,     '480px'  ]
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Touch mode.
		if (browser.mobile) {

			var $wrapper;

			// Create wrapper.
				$body.wrapInner('<div id="wrapper" />');
				$wrapper = $('#wrapper');

				// Hack: iOS vh bug.
					if (browser.os == 'ios')
						$wrapper
							.css('margin-top', -25)
							.css('padding-bottom', 25);

				// Pass scroll event to window.
					$wrapper.on('scroll', function() {
						$window.trigger('scroll');
					});

			// Scrolly.
				$window.on('load.hl_scrolly', function() {

					$('.scrolly').scrolly({
						speed: 1500,
						parent: $wrapper,
						pollOnce: true
					});

					$window.off('load.hl_scrolly');

				});

			// Enable touch mode.
				$html.addClass('is-touch');

		}
		else {

			// Scrolly.
				$('.scrolly').scrolly({
					speed: 1500
				});

		}

	// Header.
		var $header = $('#header'),
			$headerTitle = $header.find('header'),
			$headerContainer = $header.find('.container');

		// Make title fixed.
			if (!browser.mobile) {

				$window.on('load.hl_headerTitle', function() {

					breakpoints.on('>medium', function() {

						$headerTitle
							.css('position', 'fixed')
							.css('height', 'auto')
							.css('top', '50%')
							.css('left', '0')
							.css('width', '100%')
							.css('margin-top', ($headerTitle.outerHeight() / -2));

					});

					breakpoints.on('<=medium', function() {

						$headerTitle
							.css('position', '')
							.css('height', '')
							.css('top', '')
							.css('left', '')
							.css('width', '')
							.css('margin-top', '');

					});

					$window.off('load.hl_headerTitle');

				});

			}

		// Scrollex.
			breakpoints.on('>small', function() {
				$header.scrollex({
					terminate: function() {

						$headerTitle.css('opacity', '');

					},
					scroll: function(progress) {

						// Fade out title as user scrolls down.
							if (progress > 0.5)
								x = 1 - progress;
							else
								x = progress;

							$headerTitle.css('opacity', Math.max(0, Math.min(1, x * 2)));

					}
				});
			});

			breakpoints.on('<=small', function() {

				$header.unscrollex();

			});

	// Main sections.
		$('.main').each(function() {

			var $this = $(this),
				$primaryImg = $this.find('.image.primary > img'),
				$bg,
				options;

			// No primary image? Bail.
				if ($primaryImg.length == 0)
					return;

			// Create bg and append it to body.
				$bg = $('<div class="main-bg" id="' + $this.attr('id') + '-bg"></div>')
					.css('background-image', (
						'url("C:/Users/user/Downloads/fontgan/fontgan/makefontapp/static/makefontapp/assets/css/images/overlay.png"), url("' + $primaryImg.attr('src') + '")'
					))
					.appendTo($body);

			// Scrollex.
				$this.scrollex({
					mode: 'middle',
					delay: 200,
					top: '-10vh',
					bottom: '-10vh',
					init: function() { $bg.removeClass('active'); },
					enter: function() { $bg.addClass('active'); },
					leave: function() { $bg.removeClass('active'); }
				});



		});



})(jQuery);

var iuploadname = 0;
const add_textbox = () => {
	var fileCheck = document.getElementById("file"+iuploadname).value;
	if(!fileCheck){
        alert("파일을 첨부해 주세요");
        return false;
	}
	else{
		iuploadname = iuploadname + 1;
		const box = document.getElementById("divbox_id");
		const newP = document.createElement('div')
		newP.classList.add('filebox')
		newP.innerHTML = '<div><input class="text" type="text" name="char'+iuploadname+'" placeholder="가"></div> <input id="upload-name'+iuploadname+'" class="upload-name" value="첨부파일" placeholder="첨부파일"> <label for="file'+iuploadname+'">파일찾기</label>  <input type="file" id="file'+iuploadname+'" name="char_img'+iuploadname+'" accept="image/png, image/jpg">';
		box.appendChild(newP);

		
		$("#file"+iuploadname).on('change',function(){
			var fileName = $("#file"+iuploadname).val();
			$("#upload-name"+iuploadname).val(fileName);
		});
	}
}
const remove = (obj) => {
	document.getElementById('box').removeChild(obj.parentNode);
}

$("#file0").on('change',function(){
	var fileName = $("#file0").val();
	$("#upload-name0").val(fileName);
});


const check_file = () => {
	var email = document.getElementById("email").value;
	var password = document.getElementById("password").value;
	var file = document.getElementById("file").value;
	if(!email || !password || !file){
        alert("양식을 채워주세요");
        return false;
	}
	else{
		return true;
	}
}