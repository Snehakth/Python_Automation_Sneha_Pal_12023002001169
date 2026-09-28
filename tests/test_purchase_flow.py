"""End-to-end customer purchase scenario."""

from tests.pages.storefront import Storefront


def test_customer_can_update_cart_quantity(driver, purchase_data, capture_screenshot):
    storefront = Storefront(driver, purchase_data["base_url"])
    storefront.open()
    storefront.register_account_and_login()
    storefront.search_for_product(purchase_data["product_name"])
    storefront.add_product_to_cart()
    capture_screenshot("product-added")

    cart = storefront.update_and_read_cart(purchase_data["product_name"], purchase_data["quantity"])
    capture_screenshot("cart-updated")

    assert cart["product_name"] == purchase_data["product_name"]
    assert cart["quantity"] == str(purchase_data["quantity"])
    assert "$" in cart["row_text"]