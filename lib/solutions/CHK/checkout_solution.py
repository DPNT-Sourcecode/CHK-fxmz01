from collections import Counter


ERROR = -1

prices = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
}

discounts = {
    "A": (3, 130),
    "B": (2, 45),
}


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    if not isinstance(skus, str):
        return ERROR

    total = 0
    for sku, count in _counter(skus).items():
        print(sku)
        print(count)

    for sku in skus.split():
        if sku not in prices:
            return ERROR
        total += prices[sku]
    return total


def _counter(skus: str) -> dict[str, int]:
    return Counter(skus.split())


def _discountpacks(total: int, pack_size) -> tuple[int, int]:
    """Returns number of packs, number of individual priced items"""
    return total // pack_size, total % pack_size


