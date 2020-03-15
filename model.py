"""Models and database functions for Instaeater project."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
	"""Post data for Instaeater website."""

	__tablename__ = "posts"

	post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	account = db.Column(db.String(64), nullable=True)
	shortcode = db.Column(db.String(64), nullable=True)
	location_name = db.Column(db.String(64), nullable=True)
	slug = db.Column(db.String(64), nullable=True)
	lat = db.Column(db.Float, nullable=True)
	lng = db.Column(db.Float, nullable=True)
	viewport_ne_lat = db.Column(db.Float, nullable=True)
	viewport_ne_lng = db.Column(db.Float, nullable=True)
	viewport_sw_lat = db.Column(db.Float, nullable=True)
	viewport_sw_lng = db.Column(db.Float, nullable=True)
	formatted_address = db.Column(db.String(200), nullable=True)
	maps_name = db.Column(db.String(100),nullable=True)
	rating = db.Column(db.Float, nullable=True)
	place_id = db.Column(db.String(64), db.ForeignKey('places.place_id'))

	def __repr__(self):
		"""Provide helpful representation when printed."""

		return f"<Post post_id={self.post_id} account={self.account} shortcode={self.shortcode}>"


class User(db.Model):
	"""User data for Instaeater website."""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(64), nullable=True)
	password = db.Column(db.String(64), nullable=True)

	favorites = db.relationship('Favorite')

	def __repr__(self):
		"""Provide helpful representation when printed."""

		return f"<User user_id={self.user_id} email={self.email}>"


class Place(db.Model):
	"""Place data for Instaeater website."""

	__tablename__ = "places"

	place_id = db.Column(db.String(64), primary_key=True)
	lat = db.Column(db.Float, nullable=True)
	lng = db.Column(db.Float, nullable=True)
	viewport_ne_lat = db.Column(db.Float, nullable=True)
	viewport_ne_lng = db.Column(db.Float, nullable=True)
	viewport_sw_lat = db.Column(db.Float, nullable=True)
	viewport_sw_lng = db.Column(db.Float, nullable=True)
	formatted_address = db.Column(db.String(200), nullable=True)
	maps_name = db.Column(db.String(100),nullable=True)
	rating = db.Column(db.Float, nullable=True)
	phone_number = db.Column(db.String(20), nullable=True)
	opening_hours = db.Column(db.String(400), nullable=True)
	website = db.Column(db.String(200), nullable=True)

	posts = db.relationship('Post')
	favorites = db.relationship('Favorite')

	def __repr__(self):
		"""Provide helpful representation when printed."""

		return f'<Place place_id={self.place_id} maps_name={self.maps_name}>' 


class Favorite(db.Model):
	"""Favorite data for Instaeater website."""

	__tablename__ = "favorites"

	favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	place_id = db.Column(db.String(64), db.ForeignKey('places.place_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

	user = db.relationship('User')
	place = db.relationship('Place')

	def __repr__(self):
		"""Provide helpful representation when printed."""

		return f'<Favorite favorite_id={self.favorite_id} place_id={self.place_id} by user_id={self.user_id}>'


class Tag(db.Model):
	"""Tag data on favorite locations for Instaeater website."""

	__tablename__ = "tags"

	tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	favorite_id = db.Column(db.Integer, db.ForeignKey('favorites.favorite_id'))
	tag_text = db.Column(db.String(100), nullable=False)

	favorite = db.relationship('Favorite')

	def __repr__(self):
		"""Provide helpful representation when printed."""

		return f'<Tag tag_id={self.tag_id} favorite_id={self.favorite_id}>'


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///instaeater'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print("Connected to DB.")