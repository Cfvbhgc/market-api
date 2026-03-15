from flask import request
from flask_restx import Namespace, Resource, fields
from ..extensions import db
from ..models.order import Order, OrderItem, ORDER_STATUSES
from ..models.cart import Cart, CartItem
from ..models.user import User
from ..schemas.serializers import serialize_order

orders_ns = Namespace("orders", description="Order management")

order_status_input = orders_ns.model("OrderStatusUpdate", {
    "status": fields.String(
        required=True,
        description="New order status",
        enum=list(ORDER_STATUSES),
    ),
})


@orders_ns.route("/user/<int:user_id>")
class UserOrders(Resource):
    def get(self, user_id):
        """Get all orders for a user, newest first."""
        User.query.get_or_404(user_id, description="User not found")
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        return {
            "orders": [serialize_order(o) for o in orders],
            "count": len(orders),
        }, 200


@orders_ns.route("/checkout/<int:user_id>")
class Checkout(Resource):
    def post(self, user_id):
        """
        Create an order from the user's current cart.
        This empties the cart and decrements product stock.
        """
        user = User.query.get_or_404(user_id, description="User not found")
        cart = Cart.query.filter_by(user_id=user.id).first()

        if not cart or not cart.items:
            return {"message": "Cart is empty, nothing to checkout"}, 400

        # Validate stock for every item before proceeding
        for ci in cart.items:
            if ci.quantity > ci.product.stock:
                return {
                    "message": f"Not enough stock for '{ci.product.name}'. "
                               f"Requested: {ci.quantity}, Available: {ci.product.stock}"
                }, 400

        # Build the order
        order = Order(user_id=user.id, total=0)
        db.session.add(order)
        db.session.flush()  # get the order id

        total = 0
        for ci in cart.items:
            line_total = ci.product.price * ci.quantity
            total += line_total

            order_item = OrderItem(
                order_id=order.id,
                product_id=ci.product_id,
                quantity=ci.quantity,
                price_at_time=ci.product.price,
            )
            db.session.add(order_item)

            # reduce stock
            ci.product.stock -= ci.quantity

        order.total = round(total, 2)

        # Clear the cart
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()

        return serialize_order(order), 201


@orders_ns.route("/<int:order_id>")
class OrderDetail(Resource):
    def get(self, order_id):
        """Get details of a specific order."""
        order = Order.query.get_or_404(order_id, description="Order not found")
        return serialize_order(order), 200

    @orders_ns.expect(order_status_input)
    def patch(self, order_id):
        """Update order status (e.g. pending -> paid -> shipped -> delivered)."""
        order = Order.query.get_or_404(order_id, description="Order not found")
        data = request.json

        new_status = data.get("status")
        if new_status not in ORDER_STATUSES:
            return {
                "message": f"Invalid status. Must be one of: {', '.join(ORDER_STATUSES)}"
            }, 400

        order.status = new_status
        db.session.commit()

        return serialize_order(order), 200
