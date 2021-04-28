# Table of Contents

- [Introduction](#Introduction)
- [API Endpoints](<#API\ Endpoints>)
- [Technologies](#Technologies)
- [Installation](#Installation)

# Introduction

A simple e-commerce RESTful API, it features:

- Authentication and Authorization using JWT.
- Shopping Cart.
- Payment and Checkout using [Stripe](https://stripe.com/).

# API Endpoints

| Endpoint                     | Available Methods | Description                                                                                |
| ---------------------------- | ----------------- | ------------------------------------------------------------------------------------------ |
| `<domain>/api/register`      | POST              | Registers a user to the api and receiving a new access and refresh JWT token.              |
| `<domain>/api/token`         | POST              | Obtains a new pair of JWT tokens after submitting valid credentials.                       |
| `<domain>/api/token/refresh` | POST              | Obtains a new access token after submitting a valid refresh token.                         |
| `<domain>/carts`             | POST              | Creates a new cart resource.                                                               |
| `<domain>/carts/<cart-id>`   | GET               | Obtains user's cart details, only available to authenticated and users who own the cart.   |
| `<domain>/checkout`          | POST              | Creates a new payment resource that will issue necessary billing information for the user. |

# Technologies

- Django rest framework
- PostgreSQL
- Docker
- JWT
- Stripe

# Installation

## Requirements

- Docker and docker-compose.
- [Stripe API developer's key](https://stripe.com/docs/keys).

Clone the repo and in the project root, run:

```bash
$ export STRIPE_API_KEY=<your-key>
$ docker-compose up
```
