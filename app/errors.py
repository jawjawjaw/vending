class NotEnoughMoneyError(Exception):
    """Raised when the user has not inserted enough coins to purchase"""

    def __init__(self, message="Not enough funds to purchase product"):
        super().__init__(message)


class NotEnoughProductError(Exception):
    """Raised when there is not enough product available to purchase"""

    def __init__(self, message="Not enough product available"):
        super().__init__(message)


class NotEnoughChangeError(Exception):
    """Raised when there is not enough change available to return"""

    def __init__(self, message="Not enough change available"):
        super().__init__(message)


class ProductNotFoundError(Exception):
    """Raised when the product is not found"""

    def __init__(self, message="Product not found"):
        super().__init__(message)


class UserNotFoundError(Exception):
    """Raised when the user is not found"""

    def __init__(self, message="User not found"):
        super().__init__(message)


class InvalidCoinError(Exception):
    """Raised when when used is not valid"""

    def __init__(self, message="Invalid coin"):
        super().__init__(message)



class InvalidCostError(Exception):
    """Raised when when used is not valid"""

    def __init__(self, message="Invalid cost - must be positive and divisible by 5"):
        super().__init__(message)
        
        
class InvalidRoleError(Exception):
    """Raised when when used is not valid"""

    def __init__(self, message="Invalid role"):
        super().__init__(message)