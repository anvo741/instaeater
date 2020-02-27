"use strict";
// get value from select dropdown menu here, pass to api route
$('#account').change(() => {
	$("#posts").empty();
	const new_account = { 'account': $("#account").val() };
	$.get('/api/get_shortcodes', new_account, (shortcodes) => {
		for (const shortcode of shortcodes) {
			$("#posts").append(
				`<div id = ${shortcode.shortcode}>
					<blockquote class="instagram-media">
						<a href="https://instagram.com/p/${shortcode.shortcode}/"></a>
					</blockquote>
				</div>`
			)
		}
	instgrm.Embeds.process();
	})
});

// $.get('/api/get_shortcodes', (shortcodes) => {

// }