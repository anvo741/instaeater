"""Models and database functions for Instaeater project."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
	"""Post data for Instaeater website."""

	__tablename__="posts"

	post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    shortcode = db.Column(db.String(64), nullable=True)
    location_name = db.Column(db.String(64), nullable=True)
    slug = db.Column(db.String(64), nullable=True)
    # lat =
    # lng =
    # viewport_
    # viewport_
    # viewport_
    # viewport_
    # formatted_address = 
    # rating =

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Post post_id={self.post_id} shortcode={self.shortcode}>"


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
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