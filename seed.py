"""Utility file to seed instaeater database from posts data in seed_data/"""

import datetime
from sqlalchemy import func

from model import Post, connect_to_db, db
from server import app

def load_posts():
    """Load users from posts.txt into database."""

    print("Posts")

    for i, row in enumerate(open("seed_data/posts.txt")):
        row = row.rstrip()
        post_id, account, shortcode, location_name, slug, lat, lng, viewport_ne_lat, viewport_ne_lng, viewport_sw_lat, viewport_sw_lng, formatted_address, maps_name, rating, place_id = row.split("|")

        post = Post(post_id=post_id,
                    account=account,
                    shortcode=shortcode,
                    location_name=location_name,
                    slug=slug,
                    lat=lat,
                    lng=lng,
                    viewport_ne_lat=viewport_ne_lat,
                    viewport_ne_lng=viewport_ne_lng,
                    viewport_sw_lat=viewport_sw_lat,
                    viewport_sw_lng=viewport_sw_lng,
                    formatted_address=formatted_address,
                    maps_name=maps_name,
                    rating=rating,
                    place_id = place_id)

        db.session.add(post)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_posts()

