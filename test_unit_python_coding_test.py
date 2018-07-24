import pytest


@pytest.fixture
def setup_pct():
    import python_coding_test_2 as pct
    return pct


def test_market_segments(setup_pct):
    pct = setup_pct
    test_ms = pct.MarketSegment(name="Test Market Segment")
    assert test_ms.name == "Test Market Segment"
    assert test_ms.get_accounts() == []

    del test_ms

    test_account = pct.Account(name="Test Account")
    test_ms = pct.MarketSegment(name="Test Market Segment", accounts=[test_account])
    assert test_account in test_ms.get_accounts()
    assert test_ms in test_account.get_market_segments()

    test_account_2 = pct.Account(name="Test Account 2")
    test_ms.add_account(test_account_2)
    assert test_account_2 in test_ms.get_accounts()
    assert test_ms in test_account.get_market_segments()

    test_ms.remove_account(test_account)
    assert test_account not in test_ms.get_accounts()
    assert test_ms not in test_account.get_market_segments()
    assert test_account_2 in test_ms.get_accounts()
    assert test_ms in test_account_2.get_market_segments()

    del test_ms
    del test_account
    del test_account_2


def test_accounts(setup_pct):
    pct = setup_pct
    test_account = pct.Account(name="Test Account")
    assert test_account.name == "Test Account"
    assert test_account.get_sales_rep() is None
    assert test_account.get_market_segments() == []

    del test_account

    test_account = pct.Account(name="Test Account", sales_rep="Daffy Duck")
    assert test_account.get_sales_rep() == "Daffy Duck"

    del test_account

    test_ms = pct.MarketSegment(name="Test Market Segment")
    test_account = pct.Account(name="Test Account", sales_rep="Daffy Duck", market_segments=[test_ms])
    assert test_ms in test_account.get_market_segments()
    assert test_account in test_ms.get_accounts()

    test_ms_2 = pct.MarketSegment(name="Test Market Segment 2")
    test_account.add_to_market_segment(test_ms_2)
    assert test_ms_2 in test_account.get_market_segments()
    assert test_account in test_ms_2.get_accounts()

    test_account.remove_from_market_segment(test_ms)
    assert test_ms not in test_account.get_market_segments()
    assert test_account not in test_ms.get_accounts()
    assert test_ms_2 in test_account.get_market_segments()
    assert test_account in test_ms_2.get_accounts()

    del test_account
    del test_ms
    del test_ms_2

    test_ms_1 = pct.MarketSegment(name="Test Market Segment 1")
    test_ms_2 = pct.MarketSegment(name="Test Market Segment 2")
    test_ms_3 = pct.MarketSegment(name="Test Market Segment 3")

    test_account = pct.Account(name="Test Account", market_segments=[test_ms_1, test_ms_2])
    test_account.set_market_segments([test_ms_2, test_ms_3])
    assert test_ms_1 not in test_account.get_market_segments()
    assert test_account not in test_ms_1.get_accounts()
    assert test_ms_2 in test_account.get_market_segments()
    assert test_account in test_ms_2.get_accounts()
    assert test_ms_3 in test_account.get_market_segments()
    assert test_account in test_ms_3.get_accounts()
