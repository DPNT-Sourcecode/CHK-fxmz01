from collections import Counter


ERROR = -1

prices = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
}

discounts = {
    # By hardcoding discounts ordering (big to small) we can simplify implementation.
    # This of course wouldn't apply in a real case where this data would come from a DB
    "A": [(5, 200), (3, 130)],
    "B": [(2, 45)],
}

# class Discounts:
#     discounts = {
#         # By hardcoding discounts ordering (big to small) we can simplify implementation.
#         # This of course wouldn't apply in a real case where this data would come from a DB
#         "A": [(5, 200), (3, 130)],
#         "B": [(2, 45)],
#     }

#     @classmethod
#     def get(cls, sku: str):
#         d = cls.discounts.get(sku)
#         if d:
#             return d[0]
#         else:
#             return None


def items_price(sku, count):
    price = 0
    for pack_size, pack_price in discounts.get(sku, []):
        packs, count = _discountpack_counts(count, pack_size)
        price += packs * pack_price
    return price + count * prices[sku]


def _discountpack_counts(count: int, pack_size: int) -> tuple[int, int]:
    """Returns number of packs, number of individual priced items"""
    return count // pack_size, count % pack_size


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    if not isinstance(skus, str):
        return ERROR

    total = 0
    for sku, count in _counter(skus).items():
        if sku not in prices:
            return ERROR

        discount = Discounts.get(sku)
        if discount:
            pack_size, pack_price = discount
            packs, singles = _discountpack_counts(count, [pack_size])
            total += packs * pack_price + singles * prices[sku]
        else:
            total += count * prices[sku]

    return total


def _counter(skus: str) -> dict[str, int]:
    return Counter(skus.replace(" ", ""))




