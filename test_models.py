#!/usr/bin/env python3
"""
Test script to verify that the newly created models can be imported
and basic functionality works.
"""
import sys
import os

# Add the backend directory to the path so we can import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that we can import the newly created models."""
    try:
        # Test cart models
        from app.models.cart import Cart
        from app.models.cart_item import CartItem
        print("✓ Cart models imported successfully")

        # Test order models
        from app.models.order import Order, OrderStatusEnum
        from app.models.payment import Payment, PaymentStatusEnum
        from app.models.shipping import Shipping
        print("✓ Order models imported successfully")

        # Test that we can create instances
        cart = Cart(id="test-cart-id", session_id="test-session-123")
        print("✓ Cart instance created successfully")

        cart_item = CartItem(
            id="test-cart-item-id",
            quantity=2,
            product_id="test-product-id",
            cart_id="test-cart-id"
        )
        print("✓ CartItem instance created successfully")

        order = Order(
            id="test-order-id",
            order_number="TEST-001",
            user_id="test-user-id",
            billing_address_id="test-address-id",
            shipping_address_id="test-address-id",
            subtotal=100.0,
            tax_amount=8.0,
            shipping_amount=0.0,
            discount_amount=0.0,
            total_amount=108.0
        )
        print("✓ Order instance created successfully")

        payment = Payment(
            id="test-payment-id",
            order_id="test-order-id",
            amount=108.0,
            currency="USD",
            status="completed",
            payment_method="credit_card"
        )
        print("✓ Payment instance created successfully")

        shipping = Shipping(
            id="test-shipping-id",
            order_id="test-order-id",
            service="Standard",
            cost=0.0,
            address_line_1="123 Main St",
            city="Anytown",
            state_province="CA",
            postal_code="12345",
            country="USA"
        )
        print("✓ Shipping instance created successfully")

        print("\nAll model tests passed!")
        return True

    except Exception as e:
        print(f"✗ Error during model testing: {e}")
        return False

def test_repository_imports():
    """Test that we can import the newly created repositories."""
    try:
        from app.repositories.cart_repository import CartRepository
        from app.repositories.cart_item_repository import CartItemRepository
        from app.repositories.order_repository import OrderRepository
        from app.repositories.order_item_repository import OrderItemRepository
        from app.repositories.payment_repository import PaymentRepository
        from app.repositories.shipping_repository import ShippingRepository
        print("✓ Repository imports successful")
        return True
    except Exception as e:
        print(f"✗ Error importing repositories: {e}")
        return False

def test_service_imports():
    """Test that we can import the newly created services."""
    try:
        from app.services.cart_service import CartService
        from app.services.order_service import OrderService
        print("✓ Service imports successful")
        return True
    except Exception as e:
        print(f"✗ Error importing services: {e}")
        return False

if __name__ == "__main__":
    print("Testing newly created models and services...")
    print("=" * 50)

    success = True
    success &= test_imports()
    success &= test_repository_imports()
    success &= test_service_imports()

    print("=" * 50)
    if success:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)