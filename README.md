# MarketAPI

![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

A full-featured marketplace REST API built with Flask, PostgreSQL, and SQLAlchemy. Includes products catalog, shopping cart, order management, and product reviews with ratings.

## Quick Start

### Using Docker (recommended)

```bash
git clone https://github.com/cfvbhgc/market-api.git
cd market-api
docker-compose up --build
```

The API will be available at `http://localhost:5000` and Swagger docs at `http://localhost:5000/api/docs`.

### Manual Setup

```bash
# Clone and install
git clone https://github.com/cfvbhgc/market-api.git
cd market-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your PostgreSQL connection string

# Run seed and start
python seed.py
python run.py
```

## API Endpoints

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products/` | List products (with filtering, pagination, search) |
| `POST` | `/api/products/` | Create a new product |
| `GET` | `/api/products/<id>` | Get product details |
| `PUT` | `/api/products/<id>` | Update a product |
| `DELETE` | `/api/products/<id>` | Delete a product |
| `GET` | `/api/products/categories` | List all categories |

### Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/cart/<user_id>` | View user's cart |
| `DELETE` | `/api/cart/<user_id>` | Clear cart |
| `POST` | `/api/cart/<user_id>/items` | Add item to cart |
| `PUT` | `/api/cart/<user_id>/items/<item_id>` | Update item quantity |
| `DELETE` | `/api/cart/<user_id>/items/<item_id>` | Remove item from cart |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/orders/user/<user_id>` | Get user's order history |
| `POST` | `/api/orders/checkout/<user_id>` | Place order from cart |
| `GET` | `/api/orders/<order_id>` | Get order details |
| `PATCH` | `/api/orders/<order_id>` | Update order status |

### Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/reviews/product/<product_id>` | Get reviews for a product |
| `POST` | `/api/reviews/product/<product_id>` | Add a review |
| `GET` | `/api/reviews/<review_id>` | Get a review |
| `PUT` | `/api/reviews/<review_id>` | Update a review |
| `DELETE` | `/api/reviews/<review_id>` | Delete a review |

## Tech Stack

- **Framework:** Flask 3.0 + flask-restx (Swagger UI)
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy via Flask-SQLAlchemy
- **Migrations:** Flask-Migrate (Alembic)
- **Containerization:** Docker & Docker Compose
- **WSGI Server:** Gunicorn

## Project Structure

```
market-api/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration
│   ├── extensions.py        # DB and migration setup
│   ├── blueprints/
│   │   ├── products.py      # Product CRUD
│   │   ├── cart.py          # Cart management
│   │   ├── orders.py        # Order placement & history
│   │   └── reviews.py       # Reviews and ratings
│   ├── models/
│   │   ├── product.py
│   │   ├── user.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── review.py
│   └── schemas/
│       └── serializers.py   # Response serialization
├── seed.py                  # Database seeding script
├── run.py                   # Development entry point
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Screenshots

> Screenshots of Swagger UI will be added here.

## License

MIT
