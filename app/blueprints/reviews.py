from flask import request
from flask_restx import Namespace, Resource, fields
from ..extensions import db
from ..models.review import Review
from ..models.product import Product
from ..models.user import User
from ..schemas.serializers import serialize_review

reviews_ns = Namespace("reviews", description="Product reviews and ratings")

review_input = reviews_ns.model("ReviewInput", {
    "user_id": fields.Integer(required=True, description="Reviewer user ID"),
    "rating": fields.Integer(required=True, description="Rating from 1 to 5"),
    "comment": fields.String(description="Review text"),
})


@reviews_ns.route("/product/<int:product_id>")
class ProductReviews(Resource):
    def get(self, product_id):
        """Get all reviews for a product."""
        product = Product.query.get_or_404(product_id, description="Product not found")
        reviews = Review.query.filter_by(product_id=product_id).order_by(
            Review.created_at.desc()
        ).all()

        return {
            "product_id": product.id,
            "product_name": product.name,
            "average_rating": product.average_rating,
            "review_count": product.review_count,
            "reviews": [serialize_review(r) for r in reviews],
        }, 200

    @reviews_ns.expect(review_input)
    def post(self, product_id):
        """Add a review for a product. One review per user per product."""
        Product.query.get_or_404(product_id, description="Product not found")
        data = request.json

        user_id = data.get("user_id")
        rating = data.get("rating")
        comment = data.get("comment", "")

        if not user_id or not rating:
            return {"message": "user_id and rating are required"}, 400

        User.query.get_or_404(user_id, description="User not found")

        if not (1 <= rating <= 5):
            return {"message": "Rating must be between 1 and 5"}, 400

        # Check for existing review
        existing = Review.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing:
            return {"message": "User already reviewed this product. Use PUT to update."}, 409

        review = Review(
            user_id=user_id,
            product_id=product_id,
            rating=rating,
            comment=comment,
        )
        db.session.add(review)
        db.session.commit()

        return serialize_review(review), 201


@reviews_ns.route("/<int:review_id>")
class ReviewDetail(Resource):
    def get(self, review_id):
        """Get a specific review."""
        review = Review.query.get_or_404(review_id, description="Review not found")
        return serialize_review(review), 200

    @reviews_ns.expect(reviews_ns.model("ReviewUpdate", {
        "rating": fields.Integer(description="Updated rating (1-5)"),
        "comment": fields.String(description="Updated comment"),
    }))
    def put(self, review_id):
        """Update an existing review."""
        review = Review.query.get_or_404(review_id, description="Review not found")
        data = request.json

        if "rating" in data:
            if not (1 <= data["rating"] <= 5):
                return {"message": "Rating must be between 1 and 5"}, 400
            review.rating = data["rating"]

        if "comment" in data:
            review.comment = data["comment"]

        db.session.commit()
        return serialize_review(review), 200

    def delete(self, review_id):
        review = Review.query.get_or_404(review_id, description="Review not found")
        db.session.delete(review)
        db.session.commit()
        return {"message": "Review deleted"}, 200
