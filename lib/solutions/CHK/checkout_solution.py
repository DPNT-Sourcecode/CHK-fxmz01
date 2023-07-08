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

def items_prize(sku, count):
    prize = 0
    for pack_size, pack_prize in discounts.get(sku, []):
        
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
            pack_size, pack_prize = discount
            packs, singles = _discountpack_counts(count, [pack_size])
            total += packs * pack_prize + singles * prices[sku]
        else:
            total += count * prices[sku]

    return total


def _counter(skus: str) -> dict[str, int]:
    return Counter(skus.replace(" ", ""))





