from flask import request
from flask_restx import Namespace, Resource, fields
from ..extensions import db
from ..models.cart import Cart, CartItem
from ..models.product import Product
from ..models.user import User
from ..schemas.serializers import serialize_cart

cart_ns = Namespace("cart", description="Shopping cart operations")

cart_item_input = cart_ns.model("CartItemInput", {
    "product_id": fields.Integer(required=True, description="Product ID to add"),
    "quantity": fields.Integer(required=True, description="Quantity", default=1),
})


def _get_or_create_cart(user_id):
    """Find existing cart or create one for the user."""
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    return cart


@cart_ns.route("/<int:user_id>")
class CartResource(Resource):
    def get(self, user_id):
        """Get the cart for a specific user."""
        user = User.query.get_or_404(user_id, description="User not found")
        cart = _get_or_create_cart(user.id)
        return serialize_cart(cart), 200

    def delete(self, user_id):
        """Clear all items from the user's cart."""
        User.query.get_or_404(user_id, description="User not found")
        cart = Cart.query.filter_by(user_id=user_id).first()
        if cart:
            CartItem.query.filter_by(cart_id=cart.id).delete()
            db.session.commit()
        return {"message": "Cart cleared"}, 200


@cart_ns.route("/<int:user_id>/items")
class CartItems(Resource):
    @cart_ns.expect(cart_item_input)
    def post(self, user_id):
        """Add an item to the cart (or update quantity if it already exists)."""
        User.query.get_or_404(user_id, description="User not found")
        data = request.json

        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)

        if not product_id or quantity < 1:
            return {"message": "Valid product_id and quantity >= 1 required"}, 400

        product = Product.query.get_or_404(product_id, description="Product not found")

        if product.stock < quantity:
            return {"message": f"Not enough stock. Available: {product.stock}"}, 400

        cart = _get_or_create_cart(user_id)

        # Check if item already in cart
        existing = CartItem.query.filter_by(
            cart_id=cart.id, product_id=product_id
        ).first()

        if existing:
            existing.quantity += quantity
            if existing.quantity > product.stock:
                return {"message": f"Total quantity exceeds stock. Available: {product.stock}"}, 400
        else:
            item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(item)

        db.session.commit()
        return serialize_cart(cart), 200


@cart_ns.route("/<int:user_id>/items/<int:item_id>")
class CartItemDetail(Resource):
    @cart_ns.expect(cart_ns.model("UpdateQuantity", {
        "quantity": fields.Integer(required=True, description="New quantity"),
    }))
    def put(self, user_id, item_id):
        """Update the quantity of a cart item."""
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            return {"message": "Cart not found"}, 404

        item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
        if not item:
            return {"message": "Item not in cart"}, 404

        new_quantity = request.json.get("quantity", 1)
        if new_quantity < 1:
            return {"message": "Quantity must be at least 1"}, 400

        if new_quantity > item.product.stock:
            return {"message": f"Not enough stock. Available: {item.product.stock}"}, 400

        item.quantity = new_quantity
        db.session.commit()
        return serialize_cart(cart), 200

    def delete(self, user_id, item_id):
        """Remove a single item from the cart."""
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            return {"message": "Cart not found"}, 404

        item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
        if not item:
            return {"message": "Item not in cart"}, 404

        db.session.delete(item)
        db.session.commit()
        return serialize_cart(cart), 200
