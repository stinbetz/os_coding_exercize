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


# +---------------------------------------------------------------------------+
# |                                                                           |
# |Q1-1. Management has determined that it would be useful to organize        |
# |      Accounts by market segments, so that SalesReps can specialize        |
# |      in selling to particular segments and thus improve the number        |
# |      of sales opportunities they generate.                                |
# |                                                                           |
# |      Implement the MarketSegment class. A MarketSegment must be           |
# |      instantiated with a name, but it may also receive an iterable of     |
# |      Accounts which will be associated with it. MarketSegments must       |
# |      keep track of which Accounts they're associated with. Additionally,  |
# |      the MarketSegment class must know how to add and remove Accounts     |
# |      from itself.                                                         |
# |                                                                           |
# |      Additionally, modify the Account class so that it supports the       |
# |      following MarketSegment-related use cases:                           |
# |      - An Account may be instantiated with an iterable of MarketSegments  |
# |        to which it's related.                                             |
# |      - An Account can provide an iterable of the MarketSegments it's      |
# |        related to.                                                        |
# |      - An Account can be related to a new MarketSegment.                  |
# |      - An Account can be removed from one of the MarketSegments it's      |
# |        related to.                                                        |
# |                                                                           |
# |      A MarketSegment may be associated with more than one Account, and    |
# |      and Account may be associated with more than one MarketSegment.      |
# |                                                                           |
# +---------------------------------------------------------------------------+

class MarketSegment(object):
    """
    Models a MarketSegment. MarketSegments know their name and contain an
    iterable of the Accounts they're related to.
    """
    def __init__(self, name, accounts=None):
        """
        initialize the MarketSegment instance
        :param name: string
        :param accounts: List[Account]
        """
        self.name = name
        if accounts:
            self._accounts = accounts
            for account in accounts:
                # add_account_to_ms is False because we've already added the
                # account to this segment, don't want to do it again
                account.add_to_market_segment(self, add_account_to_ms=False)
        else:
            self._accounts = []
        check_for_existing_market_segment(self)

    def __str__(self):
        return "{self.name}".format(self=self)

    def __repr__(self):
        return "{self.name}: {self._accounts}".format(self=self)

    def add_account(self, account, add_ms_to_account=True):
        """
        provide functionality to associate an account with the market segment
        Raises ValueError if the market segment already knows about the
        account

        :param account: Account object that should be associated
        :param add_ms_to_account: Boolean, False if the Account already knows
                                  the market segment, True if it needs to be
                                  added -- defaulting to True allows for
                                  direct calling of this function, calling this
                                  from within the Account class should ALWAYS
                                  set this to False
        :return: None
        """
        # check if name already exists and throw ValueError if it does
        # it doesn't make sense to add an account twice -- this could be
        # refactored to use a set instead
        # check for accounts by name per Q2 bonus below
        if account.name in [account.name for account in self._accounts]:
            raise ValueError("{} already associated to {}".format(account.name,
                                                                  self.name))
        self._accounts.append(account)
        if add_ms_to_account:
            # add_account_to_ms is False because we've already added the
            # account to this segment, don't want to do it again
            account.add_to_market_segment(self, add_account_to_ms=False)

    def remove_account(self, account, remove_ms_from_account=True):
        """
        disassociate the account from this MarketSegment
        :param account: Account
        :param remove_ms_from_account: Boolean, False if the segment has
                                       already been removed from the account,
                                       otherwise True which allows for calling
                                       this from outside of an Account instance
        :return: None
        """
        # check for accounts by name per Q2 bonus below
        if account.name in [account.name for account in self._accounts]:
            self._accounts.remove(account)
            if remove_ms_from_account:
                account.remove_from_market_segment(self)
        else:
            # nothing to do, the account wasn't part of the market
            #  segment so we're done
            pass

    def get_accounts(self):
        """
        get the accounts associated with this MarketSegment
        :return: List[Account]
        """
        return self._accounts


class Account(object):
    """
    Models an account. Accounts know their name, the sales rep they're
    assigned to, and the market segments they're a part of.
    """
    def __init__(self, name, sales_rep=None, market_segments=None):
        """
        setup this instance of Account
        :param name: string
        :param sales_rep: SalesRep
        :param market_segments: List[MarketSegment]
        """
        self.name = name
        self._sales_rep = sales_rep
        self._children = []
        if market_segments:
            self._market_segments = market_segments
            for market_segment in market_segments:
                # add_ms_to_account needs to be False so we don't try to add
                # the market segment to the account again
                market_segment.add_account(self, add_ms_to_account=False)
        else:
            self._market_segments = []

    def __str__(self):
        return "{self.name}".format(self=self)

    def get_sales_rep(self):
        """
        get the sales rep assocated to this Account
        :return: SalesRep
        """
        return self._sales_rep

    def set_sales_rep(self, sales_rep):
        """
        set the sales rep for this Account
        :param sales_rep: SalesRep
        :return: None
        """
        self._sales_rep = sales_rep

    def set_market_segments(self, segments):
        """
        replaces the list of market segments for this Account
        :param segments: List[MarketSegment]
        :return:
        """
        """
        Q1-2. Implement this method, which takes an iterable of MarketSegments
              to which this Account will be attached. This method REPLACES all
              MarketSegment associations, so be sure to update each
              MarketSegment's internal representation of associated Accounts
              appropriately.
        """
        for existing_segment in self._market_segments:
            # only need to remove the ones that aren't in the new list
            if existing_segment not in segments:
                existing_segment.remove_account(self)
        for segment in segments:
            # add segments, catch ValueErrors which means the segment was
            # already part of this account, therefor no followup action is
            # needed
            try:
                self._market_segments.append(segment)
                # add_ms_to_account needs to be False because we've already
                # added the segment to this account
                segment.add_account(self, add_ms_to_account=False)
            except ValueError:
                # this account was already associated to that segment,
                # continue on
                continue

    def add_to_market_segment(self, market_segment, add_account_to_ms=True):
        """
        add a market segment to this account
        :param market_segment: MarketSegment
        :param add_account_to_ms: Boolean, False if the market segment already
                                  knows about this account, otherwise True.
                                  This allows for calling from within the
                                  MarketSegment class (False) or outside (True)
        :return: None
        """
        if market_segment in self._market_segments:
            raise ValueError("{name} already part of {ms_name}"
                             .format(name=self.name,
                                     ms_name=market_segment.name))
        self._market_segments.append(market_segment)
        if add_account_to_ms:
            # add_ms_to_account needs to be False since this account already
            # knows about the market segment
            market_segment.add_account(self, add_ms_to_account=False)

    def remove_from_market_segment(self, market_segment):
        """
        remove the market segment from this account
        :param market_segment: MarketSegment
        :return:
        """
        if market_segment in self._market_segments:
            self._market_segments.remove(market_segment)
            market_segment.remove_account(self)
        else:
            # nothing to do, the market segment was already
            # not in the account market segments
            pass

    def get_market_segments(self):
        """
        helper function that returns market segments in a list
        :return: List[MarketSegment]
        """
        return self._market_segments

    def add_child(self, child_account):
        """
        associates an instance of ChildAccount to this Account
        :param child_account: ChildAccount
        :return:
        """
        self._children.append(child_account)

    def get_children(self):
        """
        get the list of children (if any) for this account
        :return: List[ChildAccount]
        """
        return self._children


# +---------------------------------------------------------------------------+
# |                                                                           |
# |Q2-1. After reviewing your work on Q1, your manager provides you with      |
# |      a new requirement: Account-MarketSegment relations must be unique.   |
# |      An informative ValueError should be raised if a user tries to relate |
# |      an Account to a MarketSegment it is already a part of.               |
# |                                                                           |
# |      Write a test suite that validates that this requirement is           |
# |      enforced correctly (or not).                                         |
# |                                                                           |
# |Q2-2. If necessary, modify the MarketSegment and Account classes so        |
# |      that the the tests you wrote in Q2-1 pass.                           |
# |                                                                           |
# |Q2-Bonus. If necessary, modify your solution to Q2-2 so that it            |
# |          uses the Account's name as the basis for determining             |
# |          whether a particular Account-MarketSegment relation is           |
# |          unique.                                                          |
# |                                                                           |
# +---------------------------------------------------------------------------+


# +---------------------------------------------------------------------------+
# |                                                                           |
# |Q3. Create a new kind of Account, called a ChildAccount. A ChildAccount    |
# |    behaves exactly like an Account, but its constructor takes an          |
# |    additional "parent" argument, which represents the Account which       |
# |    this ChildAccount is a child of.                                       |
# |                                                                           |
# |    During initialization, A ChildAccount should be assigned to its        |
# |    parent's SalesRep if no SalesRep is provided. Likewise, a ChildAccount |
# |    should be added to its parent's MarketSegments if no MarketSegments    |
# |    are provided.                                                          |
# |                                                                           |
# |    It is permissible for a ChildAccount to have another ChildAccount as   |
# |    its parent.                                                            |
# |                                                                           |
# +---------------------------------------------------------------------------+
class ChildAccount(Account):
    """
    A ChildAccount is the same as a regular Account except that it accepts a
    parent Account (or ChildAccount) and inherits the sales_rep and
    market_segments if there are any.  Only need to override the init
    because after setup, this behaves like a normal Account.
    """
    def __init__(self, name, parent, sales_rep=None, market_segments=None):
        """
        setup the ChildAccount
        :param name: string
        :param parent: Account/ChildAccount
        :param sales_rep: SalesRep
        :param market_segments: List[MarketSegments]
        """
        super().__init__(name, sales_rep, market_segments)
        self.name = name
        self._children = []
        if not sales_rep:
            # inherit the parents sales rep since none was given
            self._sales_rep = parent.get_sales_rep()
        else:
            self._sales_rep = sales_rep
        if market_segments:
            # add market segments to this account and tell those market
            # segments this account is a member
            self._market_segments = market_segments
            for market_segment in self._market_segments:
                market_segment.add_account(self, add_ms_to_account=False)
        else:
            # make a copy of the parents market segments (so the parents
            # market segments don't change with this child) and add the
            # segments then inform the segments to add this account
            self._market_segments = copy.copy(parent.get_market_segments())
            for market_segment in self._market_segments:
                market_segment.add_account(self, add_ms_to_account=False)

        # the parent is the only one maintaining this association, so inform
        # the parent that they are, in fact, a parent
        parent.add_child(self)


# ---------------------------------------------------------------------------+
#                                                                            |
#  Q4. Implement the following function "print_tree".  This function must    |
#      take an Account as input, though you may modify its signature to      |
#      take other parameters as well. This function prints the Account's     |
#      name, SalesRep and MarketSegments, as well as each of its children,   |
#      their name, SalesReps and MarketSegments (and their children, etc.)   |
#                                                                            |
#      The output should visually indicate the parent/child relationships.   |
#                                                                            |
# ---------------------------------------------------------------------------+

def print_tree(account, level=0):
    """
    print a hierarchical structure representing an account and all child
    accounts associated to it to the console
    :param account: Account
    :param level: int (used for recursive calls only)
    :return: None
    """
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
    markets_output = ""
    # work a little magic to properly format the names of the market segments
    # specifically strip off the leading and trailing quotes and add a
    # separating comma
    for market in account.get_market_segments():
        markets_output += market.name.strip("\'") + ", "
    markets_output = markets_output.strip("\'")

    # print a row to console
    print("{arrow}> {ac_name} ({markets}): {rep}"
          .format(arrow=2*level*"-",
                  ac_name=account.name,
                  markets=markets_output[:-2],
                  rep=account.get_sales_rep()))

    # recursively call print on the children (if any) Base Case: no children
    for child in account.get_children():
        print_tree(child, level=level+1)


def print_account(account):
    """
    not functionaly needed, but was used for debugging purposes, prints a
    simple one line representation of an account, but no children
    :param account: Account
    :return:
    """
    markets_output = ""
    for market in account.get_market_segments():
        markets_output += market.name.strip("\'") + ", "
    markets_output = markets_output.strip("\'")
    print(f'{account.name} ({markets_output[:-2]}): {account.get_sales_rep()}')


def check_for_existing_market_segment(segment):
    """
    utility function that checks the global scope for an object that matches
    the one passed in, if it doesn't exist create the reference in the global
    scope, this allows for "anonymous" object creation and to still get the
    object back later
    Note, the new object name will be the name property with special characters
    removed and spaces turned to _ and appended with "_ms" so a name of
    "My Awesome Video Games!" becomes "My_Awesome_Video_Games_ms"
    This is only called from the MarketSegment constructor
    :param segment: MarketSegment
    :return: None (side effect of adding to the global scope)
    """
    for var in list(globals().keys()):
        if isinstance(eval("{var}".format(var=var)), MarketSegment):
            if eval("{var}.name".format(var=var)) == segment.name:
                return

    # no matching segment found in globals, create it!
    var_name = "{}_ms".format(segment.name.replace(" ", "_"))
    regex = re.compile('[^a-zA-Z0-9_]')
    var_name = regex.sub("", var_name)
    globals()[var_name] = segment


# +---------------------------------------------------------------------------+
# |                                                                           |
# | Q5-1. Devise a SQL schema that could be used to persist the data          |
# |       represented by the SalesRep, MarketSegment, and Account classes     |
# |       above. Do not consider the ChildAccount class for this exercise.    |
# |       Make sure to preserve relationships between the classes as well as  |
# |       the data contained within each class.                               |
# |                                                                           |
# | Q5-2. Write a SQL statement that uses the schema you devised in Q5-1 to   |
# |       fetch the name and SalesRep name for all of the accounts that are   |
# |       related to the "Consumer Goods" market segment.                     |
# |                                                                           |
# +---------------------------------------------------------------------------+
#
# Q5-1
# SALESREP_TBL (PRIMARY KEY repid INT,
#               firstname VARCHAR(50),
#               lastname VARCHAR(50))
# CREATE TABLE salesrep_tbl (repid int PRIMARY KEY,
#                            firstname varchar(50),
#                            lastname varchar(50));
#
# MARKETSEGMENT_TBL (PRIMARY KEY segmentid INT,
#                    name VARCHAR(50))
# CREATE TABLE marketsegment_tbl (segmentid int PRIMARY KEY,
#                                 name varchar(50));
#
# ACCOUNT_TBL (PRIMARY KEY accountid INT,
#              name VARCHAR(50),
#              FOREIGN KEY repid (SALESREP_TBL.repid))
# CREATE TABLE account_tbl (accountid int PRIMARY KEY,
#                           name varchar(50),
#                           repid int,
#                           FOREIGN KEY (repid)
#                               REFERENCES salesrep_tbl (repid);
#
# JNCTION_TBL (accountid INT,
#              segmentid INT)
# CREATE TABLE jnction_tbl (accountid int,
#                           segmentid int);
#
#
# Q5-2
#
# insert into marketsegment_tbl (segmentid, name) values (1234, "biomedical");
# insert into marketsegment_tbl (segmentid, name) values (1235, "industrial");
# insert into marketsegment_tbl (segmentid, name) values (1236, "electronics");
# insert into account_tbl (accountid, name, repid) values (2222, "Apple", 456);
# insert into account_tbl (accountid, name, repid)
#                          values (3333, "Nintendo", 123);
# insert into account_tbl (accountid, name, repid)
#                          values (4444, "Best Buy", 123);
# insert into account_tbl (accountid, name, repid) values (5555, "Case", 456);
# insert into account_tbl (accountid, name, repid)
#                          values (6666, "Caterpillar", 456);
# insert into account_tbl (accountid, name, repid)
#                          values (7777, "John Deere", 456);
# insert into account_tbl (accountid, name, repid)
#                          values (8888, "Medtronic", 123);
# insert into account_tbl (accountid, name, repid)
#                          values (9999, "Boston Sci", 456);
# insert into jnction_tbl (accountid, segmentid) values (2222, 1236);
# insert into jnction_tbl (accountid, segmentid) values (3333, 1236);
# insert into jnction_tbl (accountid, segmentid) values (4444, 1236);
# insert into jnction_tbl (accountid, segmentid) values (5555, 1235);
# insert into jnction_tbl (accountid, segmentid) values (6666, 1235);
# insert into jnction_tbl (accountid, segmentid) values (7777, 1235);
# insert into jnction_tbl (accountid, segmentid) values (9999, 1234);
# insert into jnction_tbl (accountid, segmentid) values (8888, 1234);
#
# SELECT account.name, rep.firstname, rep.lastname FROM account_tbl AS account
# INNER JOIN salesrep_tbl AS rep ON account.repid=rep.repid
# INNER JOIN jnction_tbl as junction ON junction.accountid=account.accountid
# INNER JOIN
#     (SELECT segmentid FROM marketsegment_tbl WHERE name="electronics")
#           AS segment ON segment.segmentid=junction.segmentid;
