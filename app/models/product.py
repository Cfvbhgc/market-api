from datetime import datetime, timezone
from ..extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    reviews = db.relationship("Review", backref="product", lazy=True)

    @property
    def average_rating(self):
        """Calculate the average rating from all reviews."""
        if not self.reviews:
            return None
        total = sum(r.rating for r in self.reviews)
        return round(total / len(self.reviews), 2)

    @property
    def review_count(self):
        return len(self.reviews)

    def __repr__(self):
        return f"<Product {self.name}>"
