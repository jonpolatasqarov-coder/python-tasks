def vip_discount(func):
    def wrapper(self):
        total = func(self)

        if self.customer.is_vip:
            return total * 0.9

        return total

    return wrapper
