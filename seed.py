"""Utility file to seed instaeater database from posts data in seed_data/"""

import datetime
from sqlalchemy import func

from model import Post, connect_to_db, db, User, Favorite, Place
from server import app

def load_posts():
    """Load users from posts.txt into database."""

    print("Posts")

    for i, row in enumerate(open("seed_data/posts.txt")):
        row = row.rstrip()
        if len(row.split("|")) != 15:
            print(f'The row is {row}')
            print(f'The length is {len(row.split("|"))}')
            print(row)
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

def load_users():
    """Load users from users.txt into database."""

    print("Users")

    for i, row in enumerate(open("seed_data/users.txt")):
        row = row.rstrip()
        user_id, email, password = row.split("|")

        user = User(user_id=user_id,
                    email=email,
                    password=password)

        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    db.session.commit()


def load_places():
    """Load places from places.txt into database."""

    print("Places")

    for i, row in enumerate(open("seed_data/places.txt")):
        row = row.rstrip()
        place_id, lat, lng, viewport_ne_lat, viewport_ne_lng, viewport_sw_lat, viewport_sw_lng, formatted_address, maps_name, rating, phone_number, opening_hours, website = row.split('|')
        if len(row.split('|')) != 13:
            print(row)

        place = Place(place_id=place_id,
                        lat=lat,
                        lng=lng,
                        viewport_ne_lat=viewport_ne_lat,
                        viewport_ne_lng=viewport_ne_lng,
                        viewport_sw_lat=viewport_sw_lat,
                        viewport_sw_lng=viewport_sw_lng,
                        formatted_address=formatted_address,
                        maps_name=maps_name,
                        rating=rating,
                        phone_number=phone_number,
                        opening_hours=opening_hours,
                        website=website)

        db.session.add(place)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

        db.session.commit()


def load_favorites():
    """Load favorites from favorites.txt into database."""

    print("Favorites")

    for i, row in enumerate(open("seed_data/favorites.txt")):
        row = row.rstrip()
        if len(row.split('|')) != 10:
            print(row)
        favorite_id, place_id, user_id = row.split('|')

        favorite = Favorite(favorite_id=favorite_id,
                            place_id=place_id,
                            user_id=user_id)

        db.session.add(favorite)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_places()
    load_posts()
    load_users()
    load_favorites()

