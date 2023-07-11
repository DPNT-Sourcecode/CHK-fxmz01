# NOTES
# - Functional approach
#   At some point I considered creating classes (e.g. Cart) to handle data here.
#   I ended up deciding trying to get to the end of the exercise following a
#   functional like approach. I'm not dogmatic about OOP vs Functional
#   (or about anything else really) and I think both approaches could work nicely here.
#   But I think this kind of exercise suits functional nicely, and testing
#   becomes easier due to the lack of coupling between tests and object state.
#
# - Debugging
#   I don't normally rely on prints for debugging purposes. I started doing it because
#   I couldn't make my IDE run the tests. I just realised why that is (silly me!)
#   I always try to encourage fellow devs to make use of proper debugging tools rather
#   than use prints (or better, in addition to). It can make the process so much faster!
#   I guess I'm paying a few minutes of extra time because of it.
#
# - Final cleanup
#   In a real case, unless there is a huge time pressure to realease a fix for production,
#   I always spend a bit time cleaning up my code and trying to make it a bit easier to
#   read and work with. I'm doing the same here. I believe this kind of thing is a clear
#   time saver in the long run (or actually, often sooner, as soon as during the review process!)


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
    total, counter = add_group_discounted_items(counter)
    for sku, count in counter.items():
        if sku not in prices:
            return ERROR

        total += get_items_price(sku, count)

    return total


def get_items_price(sku, count):
    price = 0
    for pack_size, pack_price in discounts_bulk.get(sku, []):
        packs, count = divmod(count, pack_size)
        price += packs * pack_price
    return price + count * prices[sku]


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


def add_group_discounted_items(counter: dict[str, int]) -> tuple[int, dict[str, int]]:
    total = 0
    new_counter = copy(counter)
    for skus_group, pack_size, pack_price in discounts_groups:
        group_count = sum(
            (count for sku, count in counter.items() if sku in skus_group)
        )
        packs, rest = divmod(group_count, pack_size)
        rest_price = n_cheapest_total(skus_group, rest, counter)
        total += packs * pack_price + rest_price

        # Remove sku so we don't charge twice
        for sku in skus_group:
            del new_counter[sku]

    return total, new_counter


def n_cheapest_total(skus: list[str], n: int, counter: dict[str, int]) -> int:
    total = 0
    for sku in sorted(skus, key=lambda sku: prices[sku]):
        take = min(n, counter[sku])
        n -= take
        total += take * prices[sku]
    return total


def _counter(skus: str) -> dict[str, int]:
    return Counter(skus.replace(" ", ""))





