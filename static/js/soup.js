"use strict";
let map;
let markers = [];

// The below adds Google map, markers, and info windows. 
function initMap() {
	// create map centered in Bay Area
	map = new google.maps.Map($('#map')[0], {
		center: {
			lat: 37.601773,
			lng: -122.202870
		},
		scrollwheel: false,
	    zoom: 10,
	    zoomControl: true,
	    panControl: false,
	    streetViewControl: false
	});
	// create instance of InfoWindow. 
	const markerInfo = new google.maps.InfoWindow();
	let bounds = new google.maps.LatLngBounds();

	$.get('/api/get_default_markers', (posts) => {
		for (const post of posts) {
			// create an info window for each post.
			const markerInfoContent = (`
				<div class="window-content">
					<b>${post.maps_name}</b>
					<li><b>Address:</b> ${post.formatted_address}</li>
					<li><b>Rating:</b> ${post.rating}</li>
				</div>
			`);
			
			// create a marker for each post.
			const postMarker = new google.maps.Marker({
				position: {
					lat: post.lat,
					lng: post.lng
				},
				title: `Shortcode: ${post.shortcode}`,
				map: map,
			});
			// extend the bounds to include the marker
			bounds.extend(postMarker.position);

			// add click listener for markers.
			postMarker.addListener('click', () => {
				markerInfo.close();
				markerInfo.setContent(markerInfoContent);
				markerInfo.open(map, postMarker);
			});
		} // end of for loop
	map.fitBounds(bounds); // auto-zoom
	map.panToBounds(bounds); // auto-center
	})
}

// When a user changes the account they would like to view, the below
// changes the embedded posts and markers on the map.
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
