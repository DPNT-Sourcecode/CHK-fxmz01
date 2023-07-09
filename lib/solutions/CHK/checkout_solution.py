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


def get_free_items_discount(sku: str, counter: dict[str, int]) -> tuple[str, int]:
    for_each, free_count, free_sku = free_items.get(sku, (0, 0, None))
    if free_sku:
        potential_free_count = (counter[sku] // for_each) * free_count
        actual_free_count = min(potential_free_count, counter.get(free_sku, 0))

        print(f"free disc {actual_free_count * prices[free_sku]}")
        return actual_free_count * prices[free_sku]
    else:
        return 0


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    if not isinstance(skus, str):
        return ERROR

    counter = _counter(skus)
    counter = remove_free_items()
    total = 0
    for sku, count in counter.items():
        if sku not in prices:
            return ERROR

        total += get_items_price(sku, count)
        total -= get_free_items_discount(sku, counter)
        # Free items?
        # free_sku, free_item_discount = get_free_items_discount(sku, count)

    return total


def _counter(skus: str) -> dict[str, int]:
    return Counter(skus.replace(" ", ""))



