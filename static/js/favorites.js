"use strict";
let map;
let markers = [];

// post request used to submit tags
// const submit_tag = (favorite_id, tag_text) => {
// 	$.post('/process_tags', { 'favorite_id' : favorite_id, tag_text : tag_text } (tag_response) => {
// 		alert(tag_response)
// 	})
// }

// click listener for tag submission button
// $('#btn-submit-tag').on("click", () => {
// 	$.post('/process_tags', { 'favorite_id' : $().val(), tag_text : $().val()} => {
// 		// do stuff
// 	})
// })


// grab favorite id and tag_text
// clear input text field
// append tag

// post request used to favorite places on click event.
function unfavoritePlace(id) {
	$.post('/api/favorite', { 'place_id' : id }, (favorite) => {
		let status = 'un-favorite'
		if (favorite.is_favorite) {
			status = 'is-favorite'
			for (let i = 0; i < markers.length; i +=1 ) {
				if (markers[i]['title'] === `Name: ${favorite.maps_name}`) {
					markers[i].setMap(map);
				}
			}
		}
		$(`#map_${favorite.place_id}`).attr("class", `${status}`);
		$(`#fav_${favorite.place_id}`).attr("class", `${status}`);
		// remove from markers
		if (! favorite.is_favorite) {
			for (let i = 0; i < markers.length; i += 1) {
				if (markers[i]['title'] === `Name: ${favorite.maps_name}`) {
					markers[i].setMap(null)
				}
			}
		}
		// adjust bounds
		let bounds = new google.maps.LatLngBounds();
		$.get('/api/get_favorite_places', (favorites) => {
			for (const favorite of favorites) {
				const position = new google.maps.LatLng(favorite.lat, favorite.lng)
				bounds.extend(position)
			} // end of for loop
			map.fitBounds(bounds); // auto-zoom
			map.panToBounds(bounds); // auto-center
		}) // end of get request
	}) // end of post request
}

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

	const markerInfo = new google.maps.InfoWindow();
	let bounds = new google.maps.LatLngBounds();

	$.get('/api/get_favorite_places', (favorites) => {
		for (const favorite of favorites) {
			// get favorite status
			let status = 'un-favorite'
			if (favorite.is_favorite) {
				status = 'is-favorite'
			}

			// create an info window for each post.
			const markerInfoContent = (`
				<div class="window-content">
					<b>${favorite.maps_name}</b>
					<li><b>Address:</b> ${favorite.formatted_address}</li>
					<li><b>Rating:</b> ${favorite.rating}</li>
					<br><button onclick="unfavoritePlace(this.id)" class=${status} id=map_${favorite.place_id}>♥</button>
				</div>
			`);

			// create a marker for each post.
			const postMarker = new google.maps.Marker({
				position: {
					lat: favorite.lat,
					lng: favorite.lng
				},
				title: `Name: ${favorite.maps_name}`,
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
				const obj = document.querySelector(`#favorites_${favorite.place_id}`)
				obj.scrollIntoView({behavior: 'smooth'});
			});
		} // end of for loop
	map.fitBounds(bounds); // auto-zoom
	map.panToBounds(bounds); // auto-center
	}) // end of get request
}