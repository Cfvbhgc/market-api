"""
Serialization helpers for converting SQLAlchemy models to dicts.
Using plain functions here instead of marshmallow to keep things simple.
"""


def serialize_product(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "stock": product.stock,
        "image_url": product.image_url,
        "average_rating": product.average_rating,
        "review_count": product.review_count,
        "created_at": product.created_at.isoformat() if product.created_at else None,
    }


def serialize_product_short(product):
    """Compact version for listings."""
    return {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "stock": product.stock,
        "average_rating": product.average_rating,
        "image_url": product.image_url,
    }


def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


def serialize_cart(cart):
    items = []
    for item in cart.items:
        items.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "subtotal": round(item.product.price * item.quantity, 2),
        })
    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "items": items,
        "total": cart.total,
        "item_count": len(items),
    }


def serialize_order(order):
    items = []
    for item in order.items:
        items.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product.name if item.product else "Deleted product",
            "quantity": item.quantity,
            "price_at_time": item.price_at_time,
            "subtotal": round(item.price_at_time * item.quantity, 2),
        })
    return {
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "total": order.total,
        "items": items,
        "created_at": order.created_at.isoformat() if order.created_at else None,
    }


def serialize_review(review):
    return {
        "id": review.id,
        "user_id": review.user_id,
        "username": review.user.username if review.user else None,
        "product_id": review.product_id,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at.isoformat() if review.created_at else None,
    }
