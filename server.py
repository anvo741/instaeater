"""Instaeater."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, jsonify, flash, redirect, session
# flash, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Post, User, Favorite, Place


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def login():
	"""Users must log in before accessing the site."""

	return render_template("login.html")


@app.route('/', methods=['POST'])
def login_process():
	"""Process login."""

	email = request.form["email"]
	password = request.form["password"]

	user = User.query.filter_by(email=email).first()

	if not user:
		flash("No such user")
		return redirect("/")

	if user.password != password:
		flash("Incorrect password")
		return redirect("/")

	session["user_id"] = user.user_id

	return redirect('/soup')


@app.route('/register')
def register_form():
	"""Show form for user signup."""

	return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
	"""Process registration."""

	email = request.form["email"]
	password = request.form["password"]

	user = User.query.filter_by(email=email).first()

	if user:
		flash("This email address is already registered.")
		return redirect('/register')
	else:
		new_user = User(email=email, password=password)
		db.session.add(new_user)
		db.session.commit()

	flash(f"User {email} added.")
	return redirect("/soup")


@app.route('/logout')
def logout():
	"""Log out."""

	del session["user_id"]
	flash("Logged out.")
	return redirect('/')


@app.route('/soup')
def default_view():
	"""Show default view of Instaeater."""

	if not session:
		return redirect("/")

	results = db.session.query(Post.account).group_by(Post.account)
	accounts = [result[0] for result in results]

	posts = db.session.query(Post.shortcode).filter_by(account='noodlesoupboyz')
	shortcodes = [post[0] for post in posts]

	return render_template("soup.html",
							accounts=accounts,
							shortcodes=shortcodes)


@app.route('/api/get_default_markers')
def get_default_markers():
	"""Get default markers for the Google Map."""

	posts = [
		{
			"shortcode" : post.shortcode,
			"lat" : post.lat,
			"lng" : post.lng,
			"maps_name" : post.maps_name,
			"formatted_address" : post.formatted_address,
			"rating" : post.rating,
			"place_id" : post.place_id,
			"is_favorite": False
		} for post in db.session.query(Post).filter_by(account="noodlesoupboyz")
	]

	# get all users favorite places
	user_id = session["user_id"]
	results = db.session.query(Favorite.place_id).filter_by(user_id=user_id)
	favorite_places = [result[0] for result in results]

	# loop over posts and add a field for if its favorited 
	for post in posts:
		if post['place_id'] in favorite_places: 
			post['is_favorite'] = True

	return jsonify(posts)


@app.route('/api/get_posts')
def get_posts():
	"""Get new posts after user selects new account to view."""
	
	new_account = request.args.get("account")
	
	posts = [
		{
			"shortcode" : post.shortcode,
			"lat" : post.lat,
			"lng" : post.lng,
			"maps_name" : post.maps_name,
			"formatted_address" : post.formatted_address,
			"rating" : post.rating,
			"is_favorite" : False
		}
		for post in db.session.query(Post).filter_by(account=new_account)
	]

	# loop over posts and add a field for if its favorited 
	for post in posts:
		if post['place_id'] in favorite_places: 
			post['is_favorite'] = True

	return jsonify(posts)


@app.route('/api/favorite', methods=['POST'])
def favorite():
	"""If favorite exists, un-favorite, i.e. delete from table. 
	Otherwise, add favorite."""

	# list slice starts at 15 because favorite id is of the format favorite_place_id
	user_id = session["user_id"]
	place_id = request.form.get("place_id")
	existing_favorite = Favorite.query.filter_by(user_id=user_id, place_id=place_id).first()
	favorite = {
		"place_id" : place_id,
		"is_favorite" : False
	}
	# if user has already favorited the place, un-favorite, i.e. delete from db.
	if existing_favorite:
		db.session.delete(existing_favorite)
		db.session.commit()
	# if user has not favorited the place, favorite it, i.e., create entry in db.
	else:
		favorite['is_favorite'] = True
		new_favorite = Favorite(place_id=place_id, user_id=user_id)
		db.session.add(new_favorite)
		db.session.commit()

	return jsonify(favorite)


@app.route('/favorites')
def render_favorites():
	"""Render favorites page."""
	if not session:
		return redirect("/")

	user_id = session["user_id"]

	favorites = [
		{
			"place_id" : favorite.place_id,
			"formatted_address" : favorite.place.formatted_address,
			"maps_name" : favorite.place.maps_name,
			"rating" : favorite.place.rating
		}
		for favorite in Favorite.query.filter_by(user_id=user_id).all()
	]

	return render_template("favorites.html",
							favorites=favorites)


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0")



