"use strict";
let map;
let markers = [];

// post request used to favorite places on click event.
function unfavoritePlace(id) {
	$.post('/api/favorite', { 'place_id' : id }, (favorite) => {
		let status = 'Favorite'
		if (favorite.is_favorite) {
			status = 'Un-Favorite'
		}
		console.log(status)
		$(`#${favorite.place_id}`).html(status)
	})
}