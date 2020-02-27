"""Utility file to seed instaeater database from posts data in seed_data/"""

import datetime
from sqlalchemy import func

from model import User, Rating, Movie, connect_to_db, db
from server import app

def load_posts():
    """Load users from posts.txt into database."""

    print("Posts")

    for i, row in enumerate(open("seed_data/u.user")):
        row = row.rstrip()
        post_id, account, shortcode, location_name, slug = row.split("|")

        post = Post(post_id=post_id,
                    account=account,
                    location_name=location_name,
                    slug=slug)

        # We need to add to the session or it won't ever be stored
        db.session.add(post)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_posts()

