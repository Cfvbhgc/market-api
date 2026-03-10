from ..extensions import db


class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    items = db.relationship("CartItem", backref="cart", lazy=True, cascade="all, delete-orphan")

    @property
    def total(self):
        return round(sum(item.product.price * item.quantity for item in self.items), 2)

    def __repr__(self):
        return f"<Cart user_id={self.user_id}>"


class CartItem(db.Model):
    """Represents a single product entry in a user's cart."""

    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    product = db.relationship("Product", lazy=True)

    # make sure we don't have duplicates in the same cart
    __table_args__ = (
        db.UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),
    )
