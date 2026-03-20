"""
Seed script to populate the database with realistic test data.
Run with: python seed.py
"""
import os
import random
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.extensions import db
from app.models import User, Product, Review

app = create_app()

# -- Product catalog --
PRODUCTS = [
    # Electronics
    {"name": "Wireless Bluetooth Headphones", "description": "Active noise-cancelling over-ear headphones with 30h battery life. Deep bass and crystal clear mids.", "price": 79.99, "category": "electronics", "stock": 150, "image_url": "https://picsum.photos/seed/headphones/400/400"},
    {"name": "USB-C Fast Charger 65W", "description": "GaN compact charger compatible with laptops, tablets and phones. Dual port.", "price": 34.99, "category": "electronics", "stock": 300, "image_url": "https://picsum.photos/seed/charger/400/400"},
    {"name": "Mechanical Keyboard RGB", "description": "Hot-swappable switches, PBT keycaps, per-key RGB lighting. Compact 75% layout.", "price": 109.99, "category": "electronics", "stock": 85, "image_url": "https://picsum.photos/seed/keyboard/400/400"},
    {"name": "4K Webcam with Microphone", "description": "Ultra HD webcam with auto-focus and built-in noise-cancelling mic. Great for streaming.", "price": 59.99, "category": "electronics", "stock": 200, "image_url": "https://picsum.photos/seed/webcam/400/400"},
    {"name": "Portable SSD 1TB", "description": "NVMe external solid state drive with USB 3.2 Gen 2. Read speeds up to 1050 MB/s.", "price": 89.99, "category": "electronics", "stock": 120, "image_url": "https://picsum.photos/seed/ssd/400/400"},
    {"name": "Smart Watch Fitness Tracker", "description": "Heart rate monitor, GPS, sleep tracking. Water resistant to 50m. 7-day battery.", "price": 149.99, "category": "electronics", "stock": 95, "image_url": "https://picsum.photos/seed/smartwatch/400/400"},
    {"name": "Wireless Mouse Ergonomic", "description": "Vertical ergonomic design reduces wrist strain. 2.4GHz wireless with USB receiver.", "price": 29.99, "category": "electronics", "stock": 250, "image_url": "https://picsum.photos/seed/mouse/400/400"},

    # Clothing
    {"name": "Classic Fit Cotton T-Shirt", "description": "100% organic cotton, pre-shrunk. Available in multiple colors. Everyday essential.", "price": 19.99, "category": "clothing", "stock": 500, "image_url": "https://picsum.photos/seed/tshirt/400/400"},
    {"name": "Slim Fit Denim Jeans", "description": "Stretch denim with a modern slim fit. Dark wash. Comfortable all-day wear.", "price": 49.99, "category": "clothing", "stock": 200, "image_url": "https://picsum.photos/seed/jeans/400/400"},
    {"name": "Waterproof Hiking Jacket", "description": "Breathable GORE-TEX membrane. Sealed seams, adjustable hood. Lightweight and packable.", "price": 129.99, "category": "clothing", "stock": 75, "image_url": "https://picsum.photos/seed/jacket/400/400"},
    {"name": "Running Shoes Lightweight", "description": "Cushioned midsole with responsive foam. Breathable mesh upper. Great for daily training.", "price": 89.99, "category": "clothing", "stock": 160, "image_url": "https://picsum.photos/seed/shoes/400/400"},
    {"name": "Merino Wool Beanie", "description": "Soft merino wool blend. Warm, breathable, and itch-free. One size fits most.", "price": 24.99, "category": "clothing", "stock": 300, "image_url": "https://picsum.photos/seed/beanie/400/400"},

    # Books
    {"name": "Clean Code by Robert C. Martin", "description": "A handbook of agile software craftsmanship. Essential reading for any developer.", "price": 33.99, "category": "books", "stock": 400, "image_url": "https://picsum.photos/seed/cleancode/400/400"},
    {"name": "Designing Data-Intensive Applications", "description": "By Martin Kleppmann. Deep dive into the big ideas behind reliable, scalable systems.", "price": 42.99, "category": "books", "stock": 180, "image_url": "https://picsum.photos/seed/ddia/400/400"},
    {"name": "The Pragmatic Programmer", "description": "20th Anniversary Edition. Timeless advice on writing better software and growing as a developer.", "price": 39.99, "category": "books", "stock": 220, "image_url": "https://picsum.photos/seed/pragmatic/400/400"},
    {"name": "Python Crash Course 3rd Edition", "description": "A hands-on, project-based introduction to programming. Perfect for beginners.", "price": 29.99, "category": "books", "stock": 350, "image_url": "https://picsum.photos/seed/pythonbook/400/400"},
    {"name": "Atomic Habits by James Clear", "description": "Practical strategies to form good habits, break bad ones, and master tiny behaviors.", "price": 16.99, "category": "books", "stock": 600, "image_url": "https://picsum.photos/seed/atomichabits/400/400"},

    # Home & Kitchen
    {"name": "Stainless Steel Water Bottle 750ml", "description": "Double-wall vacuum insulated. Keeps drinks cold 24h or hot 12h. BPA-free.", "price": 22.99, "category": "home", "stock": 400, "image_url": "https://picsum.photos/seed/bottle/400/400"},
    {"name": "LED Desk Lamp with Wireless Charger", "description": "Adjustable color temperature and brightness. Built-in Qi wireless charging pad.", "price": 45.99, "category": "home", "stock": 130, "image_url": "https://picsum.photos/seed/desklamp/400/400"},
    {"name": "Cast Iron Skillet 12 inch", "description": "Pre-seasoned, oven safe to 500F. Even heat distribution. Will last a lifetime.", "price": 34.99, "category": "home", "stock": 90, "image_url": "https://picsum.photos/seed/skillet/400/400"},
    {"name": "French Press Coffee Maker", "description": "Borosilicate glass carafe with stainless steel frame. Makes 8 cups. Simple, no filters.", "price": 27.99, "category": "home", "stock": 175, "image_url": "https://picsum.photos/seed/frenchpress/400/400"},
    {"name": "Bamboo Cutting Board Set", "description": "Set of 3 boards in different sizes. Anti-microbial bamboo. Easy on knife edges.", "price": 19.99, "category": "home", "stock": 250, "image_url": "https://picsum.photos/seed/cuttingboard/400/400"},

    # Sports
    {"name": "Yoga Mat Non-Slip 6mm", "description": "High-density TPE material. Alignment marks printed. Includes carrying strap.", "price": 29.99, "category": "sports", "stock": 200, "image_url": "https://picsum.photos/seed/yogamat/400/400"},
    {"name": "Resistance Bands Set (5 Pack)", "description": "5 different resistance levels. Latex-free TPE. Perfect for home workouts and rehab.", "price": 14.99, "category": "sports", "stock": 350, "image_url": "https://picsum.photos/seed/bands/400/400"},
    {"name": "Adjustable Dumbbell Set 25kg", "description": "Quick-lock mechanism to change weights in seconds. Replaces 15 sets of dumbbells.", "price": 199.99, "category": "sports", "stock": 45, "image_url": "https://picsum.photos/seed/dumbbell/400/400"},
]

# -- Users --
USERS = [
    {"username": "alice_dev", "email": "alice@example.com", "password": "password123"},
    {"username": "bob_builder", "email": "bob@example.com", "password": "password123"},
    {"username": "charlie_brown", "email": "charlie@example.com", "password": "password123"},
    {"username": "diana_prince", "email": "diana@example.com", "password": "password123"},
    {"username": "edward_teach", "email": "edward@example.com", "password": "password123"},
    {"username": "fiona_green", "email": "fiona@example.com", "password": "password123"},
    {"username": "george_costanza", "email": "george@example.com", "password": "password123"},
    {"username": "hannah_montana", "email": "hannah@example.com", "password": "password123"},
    {"username": "ivan_drago", "email": "ivan@example.com", "password": "password123"},
    {"username": "julia_child", "email": "julia@example.com", "password": "password123"},
]

# Sample review comments by rating
REVIEW_COMMENTS = {
    5: [
        "Absolutely love this! Best purchase I've made this year.",
        "Exceeded my expectations. Highly recommended.",
        "Perfect quality, fast shipping. Will buy again.",
        "Outstanding product. Worth every penny.",
    ],
    4: [
        "Really good product. Minor packaging issue but otherwise great.",
        "Solid quality, does exactly what it promises.",
        "Very happy with this purchase, almost perfect.",
        "Great value for the price. Would recommend.",
    ],
    3: [
        "It's okay. Does the job but nothing special.",
        "Decent product for the price. Some room for improvement.",
        "Average quality. Not bad, not great either.",
    ],
    2: [
        "Disappointing. Doesn't quite live up to the description.",
        "Below average. Had issues right out of the box.",
    ],
    1: [
        "Terrible quality. Broke after a week of use.",
        "Not as advertised. Very disappointed.",
    ],
}


def seed():
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()

        # Create users
        print("Creating users...")
        users = []
        for u in USERS:
            user = User(username=u["username"], email=u["email"])
            user.set_password(u["password"])
            db.session.add(user)
            users.append(user)
        db.session.commit()

        # Create products
        print("Creating products...")
        products = []
        for p in PRODUCTS:
            product = Product(**p)
            db.session.add(product)
            products.append(product)
        db.session.commit()

        # Create reviews (randomly assign some reviews)
        print("Creating reviews...")
        review_count = 0
        for product in products:
            # each product gets between 2-6 reviews from random users
            num_reviews = random.randint(2, 6)
            reviewers = random.sample(users, min(num_reviews, len(users)))

            for user in reviewers:
                # weighted towards higher ratings
                rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 15, 35, 35])[0]
                comment = random.choice(REVIEW_COMMENTS[rating])

                review = Review(
                    user_id=user.id,
                    product_id=product.id,
                    rating=rating,
                    comment=comment,
                )
                db.session.add(review)
                review_count += 1

        db.session.commit()

        print(f"\nSeeding complete!")
        print(f"  Users:    {len(users)}")
        print(f"  Products: {len(products)}")
        print(f"  Reviews:  {review_count}")


if __name__ == "__main__":
    seed()
