from flask_restx import Api


def register_blueprints(app):
    """Set up flask-restx API and register all namespaces."""
    api = Api(
        app,
        version="1.0",
        title="MarketAPI",
        description="A marketplace REST API with products, cart, orders and reviews",
        doc="/api/docs",
        prefix="/api",
    )

    from .products import products_ns
    from .cart import cart_ns
    from .orders import orders_ns
    from .reviews import reviews_ns

    api.add_namespace(products_ns, path="/api/products")
    api.add_namespace(cart_ns, path="/api/cart")
    api.add_namespace(orders_ns, path="/api/orders")
    api.add_namespace(reviews_ns, path="/api/reviews")
