var back_url = "https://494c0b1d.ngrok.io/";

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$wrapper = $('#page-wrapper'),
		$banner = $('#banner'),
		$header = $('#header');

	// Breakpoints.
		breakpoints({
			xlarge:   [ '1281px',  '1680px' ],
			large:    [ '981px',   '1280px' ],
			medium:   [ '737px',   '980px'  ],
			small:    [ '481px',   '736px'  ],
			xsmall:   [ null,      '480px'  ]
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Mobile?
		if (browser.mobile)
			$body.addClass('is-mobile');
		else {

			breakpoints.on('>medium', function() {
				$body.removeClass('is-mobile');
			});

			breakpoints.on('<=medium', function() {
				$body.addClass('is-mobile');
			});

		}

	// Scrolly.
		$('.scrolly')
			.scrolly({
				speed: 1500,
				offset: $header.outerHeight()
			});

	// Menu.
		$('#menu')
			.append('<a href="#menu" class="close"></a>')
			.appendTo($body)
			.panel({
				delay: 500,
				hideOnClick: true,
				hideOnSwipe: true,
				resetScroll: true,
				resetForms: true,
				side: 'right',
				target: $body,
				visibleClass: 'is-menu-visible'
			});

	// Header.
		if ($banner.length > 0
		&&	$header.hasClass('alt')) {

			$window.on('resize', function() { $window.trigger('scroll'); });

			$banner.scrollex({
				bottom:		$header.outerHeight() + 1,
				terminate:	function() { $header.removeClass('alt'); },
				enter:		function() { $header.addClass('alt'); },
				leave:		function() { $header.removeClass('alt'); }
			});

		}

})(jQuery);

var defnav = 1;

function openNav(i) {
  document.getElementById("myNav").style.width = "100%";
  defnav = i;
  $("#def"+defnav).toggle();
}

function closeNav() {
  document.getElementById("myNav").style.width = "0%";
  $("#def"+defnav).toggle();
}

// ///////////////////////// AJAX ///////////////////////////////

function transcription(){
      var url = $("#img_url").val();
      $("#spinner").toggle();
      $.ajax({
          url: back_url+"notes/web?url="+url,
          type: 'get',
          data: url,
          processData: false,
          crossDomain: true,
          contentType: "application/json",
          success: function(response){
          	console.log(response);
          	$('#image_div').toggle();
          	$("#spinner").toggle();
            $("#aud_res").attr("src","data:audio/ogg;base64," + response.audio);
            $("#img_res").attr("href", back_url+"notes/download?url="+response.image);
          },
      });
    }

function narration(){
  var url = $("#img_url").val();
  $("#spinner").toggle();
      $.ajax({
          url: back_url+"book/web?url="+url,
          type: 'get',
          processData: false,
          crossDomain: true,
          contentType: "application/json",
          success: function(response){
            console.log(response);
            $("#spinner").toggle();
            $("#aud_res").attr("src","data:audio/ogg;base64," + response.audio)
          },
      });
}

function signlang(){
  var url = $("#img_url").val();
  $("#spinner").toggle();
      $.ajax({
          url: back_url+"sign/web?url="+url,
          type: 'get',
          processData: false,
          crossDomain: true,
          contentType: "application/json",
          success: function(response){
            console.log(response);
            $("#vid_res").attr("href", back_url+"sign/download?url="+response.video);
            $("#spinner").toggle();
            $("#vid_div").toggle();
          },
      });
}

