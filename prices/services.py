from .models import Shop


def can_access_shop(shop: Shop):
    """
    Central business rule:
    Only paid sellers can use premium features
    """
    if not shop.subscription_valid():
        return False
    return True