from collections import Counter


ERROR = -1

prices = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40,
}

discounts = {
    # By hardcoding discounts ordering (big to small) we can simplify calculating item prices.
    # This of course wouldn't apply in a real case where this data would come from a DB
    "A": [(5, 200), (3, 130)],
    "B": [(2, 45)],
}

free_items = {"E": [(2, 1, "B")]}


def get_items_price(sku, count):
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

    counter = _counter(skus)
    total = 0
    for sku, count in counter.items():
        if sku not in prices:
            return ERROR

        total += get_items_price(sku, count)
        free_items_discount = 
    return total


def _counter(skus: str) -> dict[str, int]:
    return Counter(skus.replace(" ", ""))
