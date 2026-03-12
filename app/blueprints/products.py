from flask import request
from flask_restx import Namespace, Resource, fields
from ..extensions import db
from ..models.product import Product
from ..schemas.serializers import serialize_product, serialize_product_short

products_ns = Namespace("products", description="Product operations")

# Swagger models for documentation
product_input = products_ns.model("ProductInput", {
    "name": fields.String(required=True, description="Product name"),
    "description": fields.String(description="Product description"),
    "price": fields.Float(required=True, description="Price in USD"),
    "category": fields.String(required=True, description="Product category"),
    "stock": fields.Integer(description="Available stock", default=0),
    "image_url": fields.String(description="URL to product image"),
})


@products_ns.route("/")
class ProductList(Resource):
    @products_ns.doc("list_products", params={
        "category": "Filter by category",
        "min_price": "Minimum price",
        "max_price": "Maximum price",
        "search": "Search in name and description",
        "sort_by": "Sort field (price, name, created_at)",
        "order": "Sort order (asc, desc)",
        "page": "Page number (default 1)",
        "per_page": "Items per page (default 20)",
    })
    def get(self):
        """List all products with optional filtering and pagination."""
        query = Product.query

        # Filtering
        category = request.args.get("category")
        if category:
            query = query.filter(Product.category.ilike(f"%{category}%"))

        min_price = request.args.get("min_price", type=float)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        max_price = request.args.get("max_price", type=float)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        search = request.args.get("search")
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                )
            )

        # Sorting
        sort_by = request.args.get("sort_by", "created_at")
        order = request.args.get("order", "desc")

        sort_column = getattr(Product, sort_by, Product.created_at)
        if order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Pagination
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        per_page = min(per_page, 100)  # cap at 100

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "products": [serialize_product_short(p) for p in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": per_page,
        }, 200

    @products_ns.expect(product_input)
    @products_ns.doc("create_product")
    def post(self):
        """Create a new product."""
        data = request.json

        if not data.get("name") or not data.get("price"):
            return {"message": "Name and price are required"}, 400

        product = Product(
            name=data["name"],
            description=data.get("description", ""),
            price=data["price"],
            category=data.get("category", "general"),
            stock=data.get("stock", 0),
            image_url=data.get("image_url"),
        )
        db.session.add(product)
        db.session.commit()

        return serialize_product(product), 201


@products_ns.route("/<int:product_id>")
class ProductDetail(Resource):
    def get(self, product_id):
        """Get a single product by ID."""
        product = Product.query.get_or_404(product_id, description="Product not found")
        return serialize_product(product), 200

    @products_ns.expect(product_input)
    def put(self, product_id):
        """Update a product."""
        product = Product.query.get_or_404(product_id)
        data = request.json

        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price = data.get("price", product.price)
        product.category = data.get("category", product.category)
        product.stock = data.get("stock", product.stock)
        product.image_url = data.get("image_url", product.image_url)

        db.session.commit()
        return serialize_product(product), 200

    def delete(self, product_id):
        """Delete a product."""
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}, 200


@products_ns.route("/categories")
class CategoryList(Resource):
    def get(self):
        """Get all unique product categories."""
        categories = db.session.query(Product.category).distinct().all()
        return {"categories": [c[0] for c in categories]}, 200
