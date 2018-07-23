import pytest


@pytest.fixture
def setup_pct():
    import python_coding_test as pct
    return pct


def test_q1_1_a(setup_pct):
    pct = setup_pct
    test_ms_1 = pct.MarketSegment(name="ms 1")
    test_ms_2 = pct.MarketSegment(name="ms 2")
    test_account = pct.Account(name="test account",
                               market_segments=[test_ms_1, test_ms_2])
    assert test_account is not None


def test_q1_1_b(setup_pct):
    pct = setup_pct
    test_ms_1 = pct.MarketSegment(name="ms 1")
    test_ms_2 = pct.MarketSegment(name="ms 2")
    test_account = pct.Account(name="test account",
                               market_segments=[test_ms_1, test_ms_2])

    market_segments = test_account.get_market_segments()

    assert isinstance(market_segments, list)
    # assert market_segments == [x.name for x in [test_ms_1, test_ms_2]]
    assert market_segments == [test_ms_1, test_ms_2]


def test_q1_1_c(setup_pct):
    pct = setup_pct
    test_account = pct.Account(name="test account")
    test_account.add_market_segment(pct.MarketSegment(name="new segment"))

    test_segment = None
    for segment in pct.dm_market_segments:
        if segment.name == 'new segment':
            test_segment = segment
            assert True
            break

    assert test_segment and test_segment in test_account.get_market_segments()


def test_q1_1_d(setup_pct):
    pct = setup_pct
    test_ms_1 = pct.MarketSegment(name="ms 1")
    test_ms_2 = pct.MarketSegment(name="ms 2")
    test_account = pct.Account(name='test account',
                               market_segments=[test_ms_1, test_ms_2])
    test_ms_1.remove_account(test_account)

    assert test_ms_1.name not in test_account.get_market_segments()


def test_q1_1_e(setup_pct):
    pct = setup_pct
    test_ms_1 = pct.MarketSegment(name="ms 1")
    test_ms_2 = pct.MarketSegment(name="ms 2")
    test_account_1 = pct.Account(name="acc 1")
    test_account_2 = pct.Account(name="acc 2")

    test_ms_1.add_account(test_account_1)
    test_ms_1.add_account(test_account_2)
    test_ms_2.add_account(test_account_1)
    test_ms_2.add_account(test_account_2)

    assert test_ms_1 in test_account_1.get_market_segments()
    assert test_ms_2 in test_account_1.get_market_segments()
    assert test_account_1.name in [x.name for x in test_ms_1.__dict__['_accounts']]
    assert test_account_2.name in [x.name for x in test_ms_1.__dict__['_accounts']]
    assert test_ms_1 in test_account_2.get_market_segments()
    assert test_ms_2 in test_account_2.get_market_segments()
    assert test_account_1.name in [x.name for x in test_ms_2.__dict__['_accounts']]
    assert test_account_2.name in [x.name for x in test_ms_2.__dict__['_accounts']]


def test_q2_1(setup_pct):
    pct = setup_pct
    test_ms = pct.MarketSegment(name="test ms")
    test_acc = pct.Account(name="test acc")
    test_ms.add_account(test_acc)
    with pytest.raises(ValueError) as val_err:
        test_ms.add_account(test_acc)
    assert "test acc already associated to test ms" in str(val_err.value)

    with pytest.raises(ValueError) as val_err:
        test_acc.add_market_segment(test_ms)
    assert "test acc already associated to test ms" in str(val_err.value)


def test_print_tree(setup_pct, capsys):
    pct = setup_pct
    account = pct.Account(name="GE", sales_rep="Daniel Testperson",
                          market_segments=[pct.MarketSegment(name='Manufacturing'), pct.MarketSegment(name='R&D')])
    child1 = pct.ChildAccount(name='Jet Engines', parent=account)
    child1.add_market_segment(pct.MarketSegment(name='Aerospace'))
    child2 = pct.ChildAccount(name='DoD Contracts', parent=child1, sales_rep="William Testperson")
    manu_ms = pct.dm_market_segments[0]
    child2.remove_from_market_segment(manu_ms)
    child2.add_market_segment(pct.MarketSegment(name="Defense"))
    child3 = pct.ChildAccount(name='Appliances', parent=account, sales_rep="Janet Testperson",
                              market_segments=[manu_ms, pct.MarketSegment(name='Consumer Goods')])
    child4 = pct.ChildAccount(name="Washing Machines", parent=child3)
    child4.remove_from_market_segment(manu_ms)
    pct.print_tree(account)
    out, _ = capsys.readouterr()

    print("jjb dbg out: \n{}".format(out))

    assert out == "> GE (R&D, Aerospace, Defense): Daniel Testperson\n--> Jet Engines (R&D, Aerospace, Defense): Daniel Testperson\n----> DoD Contracts (R&D, Aerospace, Defense): William Testperson\n--> Appliances (Consumer Goods): Janet Testperson\n----> Washing Machines (Consumer Goods): Janet Testperson"
