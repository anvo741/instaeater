"use strict";
// get value from select dropdown menu here, pass to api route
$('#account').change(() => {
	$("#posts").empty();
	$.get('/api/get_shortcodes', (shortcodes) => {
		for (shortcode of shortcodes) {
			$("#posts").append(
				`<blockquote class="instagram-media">
					<a href="https://instagram.com/p/${shortcode}/"></a>
				</blockquote>`
			)
		}
	instgrm.Embeds.process();
	})
});

// $.get('/api/get_shortcodes', (shortcodes) => {

// }