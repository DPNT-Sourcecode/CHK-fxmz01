


from lib.solutions.CHK.checkout_solution import checkout


class TestSum:

    def test_empty(self):
        assert checkout("") == -1
        
    def test_badtype_input():
        assert checkout(1) == -1

    def test_singleitems(self):
        assert checkout("A") == 50
        assert checkout("B") == 30
        assert checkout("C") == 20

    def test_
