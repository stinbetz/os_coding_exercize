import pytest


@pytest.fixture
def setup_pct():
    import python_coding_test_2 as pct
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
    print(dir(pct))
    test_account.add_to_market_segment(pct.MarketSegment(name="new segment"))
    print(dir(pct))

    # new_segment_ms

    assert pct.new_segment_ms and pct.new_segment_ms in test_account.get_market_segments()


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
        test_acc.add_to_market_segment(test_ms)
    assert "test acc already part of test ms" in str(val_err.value)


def test_print_tree(setup_pct, capsys):
    pct = setup_pct
    manufacturing_ms = pct.MarketSegment(name='Manufacturing')
    rd_ms = pct.MarketSegment(name='R&D')
    aero_ms = pct.MarketSegment(name='Aerospace')
    defense_ms = pct.MarketSegment(name='Defense')
    cons_goods_ms = pct.MarketSegment(name='Consumer Goods')
    account = pct.Account(name="GE", sales_rep="Daniel Testperson",
                          market_segments=[manufacturing_ms, rd_ms])
    child1 = pct.ChildAccount(name='Jet Engines', parent=account)
    child1.add_to_market_segment(aero_ms)
    child2 = pct.ChildAccount(name='DoD Contracts', parent=child1, sales_rep="William Testperson")
    manufacturing_ms.remove_account(child2)
    child2.add_to_market_segment(defense_ms)
    child3 = pct.ChildAccount(name='Appliances', parent=account, sales_rep="Janet Testperson",
                              market_segments=[manufacturing_ms, cons_goods_ms])
    child4 = pct.ChildAccount(name="Washing Machines", parent=child3)
    child4.remove_from_market_segment(manufacturing_ms)
    pct.print_tree(account)
    out, _ = capsys.readouterr()

    print("jjb dbg out:\n{}".format(out))
    print("jjb dbg test:\n{}".format("""> GE (Manufacturing, R&D): Daniel Testperson
--> Jet Engines (Manufacturing, R&D, Aerospace): Daniel Testperson
----> DoD Contracts (R&D, Aerospace, Defense): William Testperson
--> Appliances (Manufacturing, Consumer Goods): Janet Testperson
----> Washing Machines (Consumer Goods): Janet Testperson"""))


    assert """> GE (Manufacturing, R&D): Daniel Testperson
--> Jet Engines (Manufacturing, R&D, Aerospace): Daniel Testperson
----> DoD Contracts (R&D, Aerospace, Defense): William Testperson
--> Appliances (Manufacturing, Consumer Goods): Janet Testperson
----> Washing Machines (Consumer Goods): Janet Testperson""" in out
