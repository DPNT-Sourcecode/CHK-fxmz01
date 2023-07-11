# NOTES
# - 
At some point I considered creating classes (e.g. Cart) to handle data here. 

from collections import Counter
from copy import copy


ERROR = -1

prices = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40,
    "F": 10,
    "G": 20,
    "H": 10,
    "I": 35,
    "J": 60,
    "K": 70,
    "L": 90,
    "M": 15,
    "N": 40,
    "O": 10,
    "P": 50,
    "Q": 30,
    "R": 50,
    "S": 20,
    "T": 20,
    "U": 40,
    "V": 50,
    "W": 20,
    "X": 17,
    "Y": 20,
    "Z": 21,
}

discounts_bulk = {
    # By hardcoding discounts ordering (big to small) we can simplify calculating item prices.
    # This of course wouldn't apply in a real case where this data would come from a DB
    "A": [(5, 200), (3, 130)],
    "B": [(2, 45)],
    # This can be more easily implemented as a 1/3 discount for every pack of 3
    # The price is read from the prices dict so that we have a single source of truth for prices!
    "F": [(3, 2 * prices["F"])],
    "H": [(10, 80), (5, 45)],
    "K": [(2, 120)],
    "P": [(5, 200)],
    "Q": [(3, 80)],
    "U": [(4, 3 * prices["U"])],
    "V": [(3, 130), (2, 90)],
}

discounts_free_items = {
    "E": (2, 1, "B"),
    "N": (3, 1, "M"),
    "R": (3, 1, "Q"),
}

discounts_groups = [
    # There is only one group discount specified, but there's no
    # reason why we couldn't have more so I'm implementing this a list
    (["S", "T", "X", "Y", "Z"], 3, 45),
]


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    if not isinstance(skus, str):
        return ERROR

    counter = remove_free_items(_counter(skus))
    total, counter = apply_group_discounts(counter)
    for sku, count in counter.items():
        if sku not in prices:
            return ERROR

        total += get_items_price(sku, count)

    return total


def get_items_price(sku, count):
    price = 0
    for pack_size, pack_price in discounts_bulk.get(sku, []):
        packs, count = _discountpack_counts(count, pack_size)
        price += packs * pack_price
    return price + count * prices[sku]


def _discountpack_counts(count: int, pack_size: int) -> tuple[int, int]:
    """Returns number of packs, number of individual priced items"""
    return count // pack_size, count % pack_size


def remove_free_items(counter):
    # Let's follow a functional approach and not modify the original argument
    new_counter = copy(counter)
    for sku, (for_each, free_count, free_sku) in discounts_free_items.items():
        potential_free_count = (counter.get(sku, 0) // for_each) * free_count
        if free_sku in new_counter:
            new_counter[free_sku] -= potential_free_count
            if new_counter[free_sku] == 0:
                del new_counter[free_sku]
    return new_counter


def apply_group_discounts(counter: dict[str, int]) -> tuple[int, dict[str, int]]:
    total = 0
    new_counter = copy(counter)
    for skus_group, pack_size, pack_price in discounts_groups:
        print("OUTER_________________________")
        # By sorting from expensive to cheaper we ensure we favour
        # the customer by applying the best possible discount
        skus_group.sort(key=lambda sku: prices[sku], reverse=True)
        # TODO sorted iterator instead of sort in place?
        group_count = 0
        for sku in skus_group:
            print("---------------INNER")
            print(f"SKU {sku}")
            group_count += new_counter.get(sku, 0)

            packs, group_count = _discountpack_counts(group_count, pack_size)
            total += packs * pack_price
            print(f"total {total}, group_count { group_count}")

    return total, new_counter


def _counter(skus: str) -> dict[str, int]:
    return Counter(skus.replace(" ", ""))

