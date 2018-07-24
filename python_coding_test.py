# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@oppsource.com'
__doc__ = """
OppSource Python programming test v0.1.2 2018-05-30.

Consider the following classes, which make up the foundation of a
(very) simple account-based marketing platform. This programming 
test will require you to modify and extend its behavior to meet
certain business goals.

If you find any of the questions below to be ambiguous, use your
best judgement to decide how to proceed, then explain why you
made that choice in comments.

Your final submissions should:
- Be syntactically valid Python 3.6.5 code.
- Follow the PEP 8 style guide.
- Be PEP 20 compliant.
- Be reasonably free from errors.
- Contain lots of comments and docstrings.
- Employ a DRY programming style.
"""

import copy
import re


class SalesRep(object):
    """
    Models a sales representative. Sales representatives know
    their own names and which accounts are assigned to them.
    """
    def __init__(self, first_name, last_name, accounts=None):
        self.first_name = first_name
        self.last_name = last_name
        self._accounts = []

        if accounts:
            self._accounts.extend(accounts)

    def __str__(self):
        return "{self.first_name} {self.last_name}".format(self=self)

    def get_accounts(self):
        return self._accounts

    def add_account(self, account):
        self._accounts.append(account)
        account.set_sales_rep(self)

    def remove_account(self, account):
        self._accounts.remove(account)
        account.set_sales_rep(None)

        
# +----------------------------------------------------------------------------+
# |                                                                            |
# | Q1-1. Management has determined that it would be useful to organize        |
# |       Accounts by market segments, so that SalesReps can specialize        |
# |       in selling to particular segments and thus improve the number        |
# |       of sales opportunities they generate.                                |
# |                                                                            |
# |       Implement the MarketSegment class. A MarketSegment must be           |
# |       instantiated with a name, but it may also receive an iterable of     |
# |       Accounts which will be associated with it. MarketSegments must       |
# |       keep track of which Accounts they're associated with. Additionally,  |
# |       the MarketSegment class must know how to add and remove Accounts     |
# |       from itself.                                                         |
# |                                                                            |
# |       Additionally, modify the Account class so that it supports the       |
# |       following MarketSegment-related use cases:                           |
# |       - An Account may be instantiated with an iterable of MarketSegments  |
# |         to which it's related.                                             |
# |       - An Account can provide an iterable of the MarketSegments it's      |
# |         related to.                                                        |
# |       - An Account can be related to a new MarketSegment.                  |
# |       - An Account can be removed from one of the MarketSegments it's      |
# |         related to.                                                        |
# |                                                                            |
# |       A MarketSegment may be associated with more than one Account, and    |
# |       and Account may be associated with more than one MarketSegment.      |
# |                                                                            |
# +----------------------------------------------------------------------------+
       
class MarketSegment(object):
    """
    Models a MarketSegment. MarketSegments know their name and contain an
    iterable of the Accounts they're related to.
    """
    def __init__(self, name, accounts=None):
        self.name = name
        if accounts:
            self._accounts = accounts
            for account in accounts:
                account.add_to_market_segment(self, add_account_to_ms=False)
        else:
            self._accounts = []
        check_for_existing_market_segment(self)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}: {self._accounts}"

    def add_account(self, account, add_ms_to_account=True):
        if account.name in [account.name for account in self._accounts]:
            raise ValueError("{} already associated to {}".format(account.name, self.name))
        self._accounts.append(account)
        if add_ms_to_account:
            account.add_to_market_segment(self, add_account_to_ms=False)

    def remove_account(self, account, remove_ms_from_account=True):
        if account.name in [account.name for account in self._accounts]:
            self._accounts.remove(account)
            if remove_ms_from_account:
                account.remove_from_market_segment(self)
        else:
            # nothing to do, the account wasn't part of the market segment so we're done
            pass

    def get_accounts(self):
        return self._accounts


class Account(object):
    """
    Models an account. Accounts know their name, the sales rep they're
    assigned to, and the market segments they're a part of.
    """
    def __init__(self, name, sales_rep=None, market_segments=None):
        self.name = name
        self._sales_rep = sales_rep
        self._children = []
        if market_segments:
            self._market_segments = market_segments
            for market_segment in market_segments:
                market_segment.add_account(self, add_ms_to_account=False)
        else:
            self._market_segments = []

    def __str__(self):
        return "{self.name}".format(self=self)

    def get_sales_rep(self):
        return self._sales_rep
    
    def set_sales_rep(self, sales_rep):
        self._sales_rep = sales_rep

    def set_market_segments(self, segments):
        """
        Q1-2. Implement this method, which takes an iterable of MarketSegments to
              which this Account will be attached. This method REPLACES all
              MarketSegment associations, so be sure to update each MarketSegment's
              internal representation of associated Accounts appropriately.
        """
        for existing_segment in self._market_segments:
            if existing_segment not in segments:
                existing_segment.remove_account(self)
        for segment in segments:
            try:
                self._market_segments.append(segment)
                segment.add_account(self, add_ms_to_account=False)
            except ValueError:
                # this account was already associated to that segment, continue on
                continue

    def add_to_market_segment(self, market_segment, add_account_to_ms=True):
        if market_segment in self._market_segments:
            raise ValueError(f"{self.name} already part of {market_segment.name}")
        self._market_segments.append(market_segment)
        if add_account_to_ms:
            market_segment.add_account(self, add_ms_to_account=False)

    def remove_from_market_segment(self, market_segment):
        if market_segment in self._market_segments:
            self._market_segments.remove(market_segment)
            market_segment.remove_account(self)
        else:
            # nothing to do, the market segment was already not in the account market segments
            pass

    def get_market_segments(self):
        return self._market_segments

    def add_child(self, child_account):
        self._children.append(child_account)

    def get_children(self):
        return self._children


# +----------------------------------------------------------------------------+
# |                                                                            |
# | Q2-1. After reviewing your work on Q1, your manager provides you with      |
# |       a new requirement: Account-MarketSegment relations must be unique.   |
# |       An informative ValueError should be raised if a user tries to relate |
# |       an Account to a MarketSegment it is already a part of.               |
# |                                                                            |
# |       Write a test suite that validates that this requirement is           |
# |       enforced correctly (or not).                                         |
# |                                                                            |
# | Q2-2. If necessary, modify the MarketSegment and Account classes so        |
# |       that the the tests you wrote in Q2-1 pass.                           |
# |                                                                            |
# | Q2-Bonus. If necessary, modify your solution to Q2-2 so that it            |
# |           uses the Account's name as the basis for determining             |
# |           whether a particular Account-MarketSegment relation is           |
# |           unique.                                                          |
# |                                                                            |
# +----------------------------------------------------------------------------+


# +----------------------------------------------------------------------------+
# |                                                                            |
# | Q3. Create a new kind of Account, called a ChildAccount. A ChildAccount    |
# |     behaves exactly like an Account, but its constructor takes an          |
# |     additional "parent" argument, which represents the Account which       |
# |     this ChildAccount is a child of.                                       |
# |                                                                            |
# |     During initialization, A ChildAccount should be assigned to its        |
# |     parent's SalesRep if no SalesRep is provided. Likewise, a ChildAccount |
# |     should be added to its parent's MarketSegments if no MarketSegments    |
# |     are provided.                                                          |
# |                                                                            |
# |     It is permissible for a ChildAccount to have another ChildAccount as   |
# |     its parent.                                                            |
# |                                                                            |
# +----------------------------------------------------------------------------+
class ChildAccount(Account):
    def __init__(self, name, parent, sales_rep=None, market_segments=None):
        self.name = name
        self._children = []
        if not sales_rep:
            self._sales_rep = parent.get_sales_rep()
        else:
            self._sales_rep = sales_rep
        if market_segments:
            self._market_segments = market_segments
            for market_segment in self._market_segments:
                market_segment.add_account(self, add_ms_to_account=False)
        else:
            self._market_segments = copy.copy(parent.get_market_segments())
            for market_segment in self._market_segments:
                market_segment.add_account(self, add_ms_to_account=False)

        parent.add_child(self)


# +----------------------------------------------------------------------------+
# |                                                                            |
# |  Q4. Implement the following function "print_tree".  This function must    |
# |      take an Account as input, though you may modify its signature to      |
# |      take other parameters as well. This function prints the Account's     |
# |      name, SalesRep and MarketSegments, as well as each of its children,   |
# |      their name, SalesReps and MarketSegments (and their children, etc.)   |
# |                                                                            |
# |      The output should visually indicate the parent/child relationships.   |
# |                                                                            |
# +----------------------------------------------------------------------------+

def print_tree(account, level=0):
    """ In the example output below, "GE" is the root account, "Jet Engines"
        and "Appliances" are first-degree ChildAccounts, and "DoD Contracts"
        and "Washing Machines" are second-degree ChildAccounts.

    > print_tree(general_electric)
    GE (Manufacturing, R&D): Daniel Testperson
        Jet Engines (Manufacturing, R&D, Aerospace): Daniel Testperson
            DoD Contracts (Defense, R&D, Aerospace): William Testperson
        Appliances (Manufacturing, Consumer Goods): Janet Testperson
            Washing Machines (Consumer Goods): Janet Testperson
    """
    # raise NotImplementedError()
    markets_output = ""
    for market in account.get_market_segments():
        markets_output += market.name.strip("\'") + ", "
    markets_output = markets_output.strip("\'")
    print(f'{2*level*"-"}> {account.name} ({markets_output[:-2]}): {account.get_sales_rep()}')
    for child in account.get_children():
        print_tree(child, level=level+1)


def print_account(account):
    markets_output = ""
    for market in account.get_market_segments():
        markets_output += market.name.strip("\'") + ", "
    markets_output = markets_output.strip("\'")
    print(f'{account.name} ({markets_output[:-2]}): {account.get_sales_rep()}')


def check_for_existing_market_segment(segment):
    for var in list(globals().keys()):
        if isinstance(eval(f"{var}"), MarketSegment):
            if eval(f"{var}.name") == segment.name:
                print("jjb dbg found the thing in {}".format(var))
                return

    # no matching segment found in session, create it!
    # print("jjb dbg hope this works soon")
    var_name = "{}_ms".format(segment.name.replace(" ", "_"))
    regex = re.compile('[^a-zA-Z0-9_]')
    var_name = regex.sub("", var_name)
    # exec("global {name}; {name} = segment".format(name=var_name))
    # print("jjb dbg adding {}".format(var_name))
    globals()[var_name] = segment
    # globals().update({"{}".format(var_name): segment})


# +----------------------------------------------------------------------------+
# |                                                                            |
# |  Q5-1. Devise a SQL schema that could be used to persist the data          |
# |        represented by the SalesRep, MarketSegment, and Account classes     |
# |        above. Do not consider the ChildAccount class for this exercise.    |
# |        Make sure to preserve relationships between the classes as well as  |
# |        the data contained within each class.                               |
# |                                                                            |
# |  Q5-2. Write a SQL statement that uses the schema you devised in Q5-1 to   |
# |        fetch the name and SalesRep name for all of the accounts that are   |
# |        related to the "Consumer Goods" market segment.                     |
# |                                                                            |
# +----------------------------------------------------------------------------+
