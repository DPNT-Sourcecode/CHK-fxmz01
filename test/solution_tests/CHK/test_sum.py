from lib.solutions.CHK import checkout_solution


class TestSum:
    def test_singleitems(self):
        assert checkout_solution.checkout(["A"]) == 50
        assert checkout_solution.checkout(["A"]) == 50
