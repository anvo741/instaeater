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
			// add favorite button to each content window.
			const markerInfoContent = (`
				<div class="window-content">
					<b>${post.maps_name}</b>
					<br><b>Address:</b> ${post.formatted_address}
					<br><b>Rating:</b> ${post.rating}
					<br><input type='button' class="favorite" id=favorite_place_${post.place_id} value='favorite'>
				</div>
			`);
			google.maps.event.addListener(markerInfo, 'domready',() => {
				google.maps.event.addDomListener($('.favorite'), 'click', () => {
					alert('test');
				});
			});
			// create a marker for each post.
			const postMarker = new google.maps.Marker({
				position: {
					lat: post.lat,
					lng: post.lng
				},
				title: `Shortcode: ${post.shortcode}`,
				map: map,
			});
			// add marker to array
			markers.push(postMarker);

			// extend the bounds to include the marker
			bounds.extend(postMarker.position);

			// add click listener for markers.
			postMarker.addListener('click', () => {
				markerInfo.close();
				markerInfo.setContent(markerInfoContent);
				markerInfo.open(map, postMarker);
				const obj = document.querySelector(`#${post.shortcode}`)
				obj.scrollIntoView({behavior: 'smooth'});
			});
		} // end of for loop
	map.fitBounds(bounds); // auto-zoom
	map.panToBounds(bounds); // auto-center
	}) // end of get request
}

// add dom ready listener to infoWindow


// https://developers.google.com/maps/documentation/javascript/examples/marker-remove

// Sets the map on all markers in the array.
function setMapOnAll(map) {
	for (var i = 0; i < markers.length; i++) {
		markers[i].setMap(map);
	}
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
	setMapOnAll(null);
}

// Shows any markers currently in the array.
function showMarkers() {
	setMapOnAll(map);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
	clearMarkers();
	markers = [];
}

// When a user changes the account they would like to view, the below
// changes the embedded posts and markers on the map.
$('#account').change(() => {
	// clear the posts
	$("#posts").empty();
	// remove the existing markers
	deleteMarkers();
	// create new info window instance
	const markerInfo = new google.maps.InfoWindow();
	// create new bounds object
	let bounds = new google.maps.LatLngBounds();
	const new_account = { 'account': $("#account").val() };
	$.get('/api/get_posts', new_account, (posts) => {
		for (const post of posts) {
			// embed new posts
			$("#posts").append(
				`<div id = ${post.shortcode}>
					<blockquote class="instagram-media">
						<a href="https://instagram.com/p/${post.shortcode}/"></a>
					</blockquote>
				</div>`
			)
			// create info window for each post.
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
			// add marker to array
			markers.push(postMarker);

			// extend the bounds to include the marker
			bounds.extend(postMarker.position);

			// add click listener for markers.
			postMarker.addListener('click', () => {
				markerInfo.close();
				markerInfo.setContent(markerInfoContent);
				markerInfo.open(map, postMarker);
				const obj = document.querySelector(`#${post.shortcode}`)
				obj.scrollIntoView({behavior: 'smooth'});
			});
		} // end of for loop
	instgrm.Embeds.process();
	showMarkers();
	map.fitBounds(bounds); // auto-zoom
	map.panToBounds(bounds); // auto-center
	})
});
