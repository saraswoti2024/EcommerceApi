from .all_routes import *


COMMON_USER_URLS = [
    PRODUCT,
    PRODUCT_DETAIL,
    ADD_CART,
    ADD_CART2,
    WISHLIST,
    WISHLIST2,
    WISHLIST3,
    REVIEW,
    REVIEW2,
    REVIEW3,
    REMOVE_CART,
    USER_PROFILE,
]


ADMIN_URLS = [
    COMMON_USER_URLS,
    PRODUCT_DETAIL2,
    PRODUCT_DETAIL3,
    PRODUCT2,
    USER_REGISTER2,
   
]

permission_map = {
    "user": COMMON_USER_URLS,
    "Admin": ADMIN_URLS,
}

class PermissionManager:
    """Permission manager."""

    def __init__(self) -> None:
        """Init."""
        self.permission_map = permission_map

    def get_permission_map(self):
        """Provide role permission map."""
        return permission_map