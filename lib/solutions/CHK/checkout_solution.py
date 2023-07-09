from collections import Counter
from copy import copy


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

free_items = {"E": (2, 1, "B")}


def get_items_price(sku, count):
    price = 0
    for pack_size, pack_price in discounts.get(sku, []):
        packs, count = _discountpack_counts(count, pack_size)
        price += packs * pack_price
    return price + count * prices[sku]


def _discountpack_counts(count: int, pack_size: int) -> tuple[int, int]:
    """Returns number of packs, number of individual priced items"""
    return count // pack_size, count % pack_size


# TODO At this point it probably makes senses to make counter a class
def remove_free_items(counter):
    # Let's follow a functional approach and not modify the original argument
    new_counter = copy(counter)
    for sku, (for_each, free_count, free_sku) in free_items.items():
        potential_free_count = (counter[sku] // for_each) * free_count
        if free_sku in new_counter:
            new_counter[free_sku] -= potential_free_count
            if new_counter[free_sku] == 0:
                del new_counter[free_sku]
    return new_counter


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    if not isinstance(skus, str):
        return ERROR

    counter = remove_free_items(_counter(skus))
    total = 0
    for sku, count in counter.items():
        if sku not in prices:
            return ERROR

        total += get_items_price(sku, count)

    return total


def _counter(skus: str) -> dict[str, int]:
    return Counter(skus.replace(" ", ""))

