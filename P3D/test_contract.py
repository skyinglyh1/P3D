from mycontracts.libs.SafeMath import Sub, Pwr, Sqrt, Add, Mul, Div
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash
from boa.builtins import ToScriptHash, concat
from boa.interop.System.Runtime import CheckWitness, Notify
from boa.interop.System.Storage import Get, GetContext, Put, Delete
from boa.interop.Ontology.Native import Invoke

from mycontracts.libs.SafeCheck import Require, RequireScriptHash


name_ = "Proof of Weak Hands"
symbol_ = "P3D"

decimal_ = 8
dividendFee_ = 10
referralFee_ = 33
# 0.01 ONG
tokenPriceInitial_ = 10000000
tokenPriceIncremental_ = 10000000
# Ong decimal is 9
ongMagnitude_ = Pwr(10, 9)
tokenMagnitude_ = Pwr(10, decimal_)
# proof of stake (defaults at 100 P3D tokens)
statingRequirement_ = Mul(100, tokenMagnitude_)

# ongContractAddress_ = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
ONGContractAddress_ = ToScriptHash("AFmseVrdL9f9oyCzZefL9tG6UbvhfRZMHJ")
selfContractAddr_ = GetExecutingScriptHash()
admin_ = ToScriptHash("AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p")


ADMIN_SUFFIX = "admin"
MANAGER_SUFFIX = "manager"
CUSTOMER_SUFFIX = "customer"
TOKENBALANCE_SUFFIX = bytearray(b'\x01')
DIVIDENDS_SUFFIX = bytearray(b'\x02')
REFERRALBALANCE_SUFFIX = bytearray(b'\x03')
PAYOUTSTO_SUFFIX = bytearray(b'\0x04')

ANTI_EARLY_WHALE_KEY = "anti_early_whale"
TOTAL_SUPPLY_KEY = "P3D_total_supply"
PROFIT_PER_TOKEN_KEY = "profit_per_token"

AntiEarlyWhale_ = True


# 20000 ONG, when the total ONG balance is smaller than this, manager can buy 200 at maximum
AntiEarlyWhaleQuota_ = Mul(20000, ongMagnitude_)
adminQuota_ = Mul(500, ongMagnitude_)
# once a manager has bought 200 ong worth token, he cannot buy more
managerQuota_ = Mul(200, ongMagnitude_)
customerQuota_ = Mul(5, ongMagnitude_)


totalEarlyQuota_ = 0
profitPerToken_ = 0
noneAdmin_ = True


def main():
    a = 3
    b = 4
    c = Pwr(a, b)
    return c

def deploy():
    Require(CheckWitness(admin_))

    # Set admin
    admin_key = concatKey(admin_, ADMIN_SUFFIX)
    Put(GetContext(), admin_key, True)

    # Set managers
    manager1 = ToScriptHash("AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p")
    key = concatKey(manager1, MANAGER_SUFFIX)
    Put(GetContext(), key, True)
    #  can add manager2, 3, 4, 5, 6

    # set anti early whale key as true for the early stage
    Put(GetContext(), ANTI_EARLY_WHALE_KEY, True)
    # initiate totalSupply
    Put(GetContext(), TOTAL_SUPPLY_KEY, 0)

    # initiate profitPerToken
    Put(GetContext(), PROFIT_PER_TOKEN_KEY, 0)

    return True

def checkAdmin(addr):
    """
    To make sure that
    1. the msg.sender is addr
    2. addr_ ADMIN_PREFIX  <-> True : means addr is the admin
    :param addr:
    :return:
    """
    # Make sure the invocation comes from addr
    Require(CheckWitness(addr))
    key = concatKey(addr, ADMIN_SUFFIX)
    value = Get(GetContext(), key)
    if value is True:
        return True
    else:
        return False


def checkManager(addr):
    """
        To make sure that
        1. the msg.sender is addr
        2. addr_ MANAGER_SUFFIX  <-> True : means addr is one of the managers
        :param addr:
        :return:
        """
    # Make sure the invocation comes from addr
    Require(CheckWitness(addr))
    key = concatKey(addr, MANAGER_SUFFIX)
    value = Get(GetContext(), key)
    if value is True:
        return True
    else:
        return False

def _checkStatingRequirement(addr):
    if balanceOf(addr) >= statingRequirement_:
        return True
    else:
        return False

def _antiEarlyWhale(_account, _ongAmount):
    """

    :param _account:
    :param _ongAmount:
    :return:
    """
    Require(CheckWitness(_account))
    _AntiEarlyWhale = Get(GetContext(), ANTI_EARLY_WHALE_KEY)
    # Still in the early stage
    if _AntiEarlyWhale:
        # total ONG is less than 20000
        if totalOngBalance()  <= AntiEarlyWhaleQuota_:
            # if _account is admin
            if Get(GetContext(), concatKey(_account, ADMIN_SUFFIX)):
                key = concatKey(_account, TOKENBALANCE_SUFFIX)
                admin_balance = Get(GetContext(), key)
                if Add(admin_balance, _ongAmount) < adminQuota_:
                    return True
                else:
                    Notify(["Idiot admin, you've bought enough tokens"])
                    return False
            #  _account is manager
            elif Get(GetContext(), concatKey(_account, MANAGER_SUFFIX)):
                key = concatKey(_account, TOKENBALANCE_SUFFIX)
                manager_balance = Get(GetContext(), key)
                if Add(manager_balance, _ongAmount) < managerQuota_:
                    return True
                else:
                    Notify(["Big head manager, you've bought enough tokens"])
                    return False
            # _account is customer
            else:
                key = concatKey(_account, TOKENBALANCE_SUFFIX)
                manager_balance = Get(GetContext(), key)
                Require(Add(manager_balance, _ongAmount) < customerQuota_)
                return True
        else:
            Put(GetContext(), ANTI_EARLY_WHALE_KEY, False)
            return True
    return True


def buy(account, ongAmount, referredBy):
    """
    Converts all incoming ong to tokens for the caller,
    and passes down the referral addr (if any)
    """




def reinvest():
    """
    Converts all the caller's dividends to tokens
    """


def exit():
    """
    Get the P3D balance of caller and sell the his P3D
    """


def withdraw():
    """
    Withdraw all the caller earning
    """


def sell():
    """

    """


# setup data
# burn the sold tokens
# update dividends tracker
# update the amount of dividends per P3D
# emit the onTokenSell event

def transfer():
    # setup data
    # forbit whale
    # withdraw all outstanding dividends first
    # liquify 10% of the tokens that are transferred
    # burn the fee token
    # exchange tokens
    # update dividend trackers
    # disperse dividends among holders
    # emit the transfer event
    i = 0






# ------------- Admin only functions begin ---------
def disableInitialStage(addr):
    """
    In case the amassador quota is not met,
    the administrator can manually disable the ambassador phase.

    """
    Require(checkAdmin(addr))


# def _addAdmin(fromAdmin, newAdmin):
#     """
#
#     :param fromAdmin: admin who wants to add new one
#     :param newAdmin: the new one that will be added as admin
#     :return:
#     """
#     # Make sure only admin can invoke this method, otherwise, raise exception
#     Require(checkAdmin(fromAdmin))
#     # Add new admin
#     key = concatKey( ADMIN_SUFFIX, newAdmin)
#     Put(GetContext(), key, True)
#     # Broad this event
#     Notify(["addAdmin", fromAdmin, newAdmin])
#     return True

#
# def deleteAdmin(fromAdmin, deletedAdmin):
#     """
#     fromAdmin will delete deletedAdmin from the admin list
#     :param fromAdmin:
#     :param deletedAdmin:
#     :return:
#     """
#     # Make sure only admin can invoke this method, and  otherwise, raise exception
#     Require(checkAdmin(fromAdmin) and checkAdmin(deletedAdmin))
#     # admin_ cannot be deleted, top level
#     Require(deletedAdmin != admin_)
#     # Delete the deletedAdmin
#     key = concatKey(deletedAdmin, ADMIN_SUFFIX)
#     Delete(GetContext(), key)
#     Notify(["deleteAdmin", fromAdmin, deletedAdmin])
#     return True


def setStakingRequirement(admin, _amountOfTokens):
    Require(checkAdmin(admin))
    statingRequirement_ = _amountOfTokens
    Notify("statingRequirement", statingRequirement_)
    return True


def setName(admin, _name):
    Require(checkAdmin(admin))
    name = _name
    return True


def setSymbol(admin, _symbol):
    Require(checkAdmin(admin))
    symbol = _symbol
    return True


# ------------- Admin only functions end ---------

def totalOngBalance():
    # how to return the Ong balance of this contract
    # ?????????
    i = 0

def totalSupply():
    return Get(GetContext(), TOTAL_SUPPLY_KEY)

def balanceOf(addr):
    key = concatKey(addr, TOKENBALANCE_SUFFIX)
    return Get(GetContext(), key)

def totalOngBalance():
    return Invoke(0, ONGContractAddress_, "balanceOf", selfContractAddr_)

def referralBalanceOf(addr):
    key = concatKey(addr, REFERRALBALANCE_SUFFIX)
    return Get(GetContext(), key)


def payOutToBalanceOf(addr):
    key = concatKey(addr, PAYOUTSTO_SUFFIX)
    return Get(GetContext(), key)



def dividendsOf(addr):
    return Get(GetContext(), concat(addr, DIVIDENDS_SUFFIX))

def sellPrice():
    """
    Return the price per P3D token
    """
    if (totalSupply() == 0):
        return tokenPriceInitial_ - tokenPriceIncremental_
    else:
        # ??????
        i = 0

def buyPrice():
    """
    Return the sell price of 1 individual token.
    """

def calculateTokensReceived(_ongToSpend):
    """
    Function for the frontend to dynamically
    retrieve the price scaling of buy orders.
    """

def calculateOngReceived(_tokenToSell):
    """
    Function for the frontend to dynamically
    retrieve the price scaling of sell orders.
    """

def _purchaseToken(_account, _ongAmount, _referredBy = None):
    """

    :param _account:
    :param _ongAmount:
    :param _referredBy:
    :return:
    """
    # avoid early whale
    Require(_antiEarlyWhale(_account, _ongAmount));
    _dividends = Div(Mul(_ongAmount, dividendFee_), 100)
    # _pureOngAmount will be used to purchase token
    _pureOngAmount = Sub(_ongAmount, _dividends)
    _purchaseTokenAmount = _ongToToken(_pureOngAmount)
    _oldTotalTokenSupply = totalSupply()
    _newTotalTokenSupply = Add(_pureOngAmount, _oldTotalTokenSupply)

    # Update the new total Supply
    Require(_newTotalTokenSupply > _oldTotalTokenSupply)
    Put(GetContext(), TOTAL_SUPPLY_KEY, _newTotalTokenSupply)

    # if the user referred by a master node
    if RequireScriptHash(_referredBy) and _referredBy != _account and _checkStatingRequirement(_referredBy):
        # referral bonus
        _referralBonus = Div(Mul(_dividends, referralFee_), 100)
        _dividends = Sub(_dividends, _referralBonus)
        Put(GetContext(), concatKey(_referredBy, REFERRALBALANCE_SUFFIX), Add(referralBalanceOf(_referredBy), _referralBonus))
    # if there is no referral, the _dividends will not change
    if _oldTotalTokenSupply > 0:
        _profitPerToken = Get(GetContext(), PROFIT_PER_TOKEN_KEY)
        _profitPerToken = Add(_profitPerToken, Div(Mul(_dividends, ongMagnitude_), _newTotalTokenSupply))
        Put(GetContext(), PROFIT_PER_TOKEN_KEY, _profitPerToken)
        # calculate the amount of tokens the customer receives over his purchase

    # Update the token balance of _account
    Put(GetContext(), concatKey(_account, TOKENBALANCE_SUFFIX), Add(balanceOf(_account), _purchaseTokenAmount))








    i = 0




def _ongToToken(_ongAmount):
    """
    Internal function to calculate token price based on an amount of incoming ong
    """
    # p -- tokenPriceInitial_
    # s -- totalSupply_
    # q -- tokenPriceIncremental_
    # b -- _ongAmount
    # sqrt(p^2 + 2bq + q^2s^2 + 2pqs) - p
    # -----------------------------------  - s
    #				q
    sum1 = Add(Pwr(tokenPriceInitial_, 2), Mul(Mul(_ongAmount, tokenPriceIncremental_), 2))
    sum2 = Add(Mul(Pwr(tokenPriceIncremental_, 2), Pwr(totalSupply_, 2)),
               Mul(Mul(2, tokenPriceInitial_), Mul(tokenPriceIncremental_, totalSupply_)))
    sum = Add(sum1, sum2)
    res1 = Sub(sum, tokenPriceInitial_)
    div = Div(res1, tokenPriceIncremental_)
    res2 = Sub(div, totalSupply_)
    return res2

def _tokenToOng( _tokenAmount):
    """
    internal function to calculate token sell price
    :param _tokenAmount: amount of token
    :return: sell price
    """
    unitToken = Pwr(10, decimal_)
    _tokenAmount = Add(_tokenAmount, unitToken)
    _totalSupply = Add(totalSupply_ + unitToken)
    # p -- tokenPriceInitial_
    # s -- totalSupply_
    # q -- tokenPriceIncremental_
    # b -- _tokenAmount
    #             s
    # ( p + q * -----  - q ) * ( b - 10^8 ) - q * { ( b^2 - b) / 10^8  }/ 2
    #            10^8
    # ------------------------------------------------------------------------
    #                             10^8
    mul1 = Sub(Add(tokenPriceInitial_, Div(Mul(tokenPriceIncremental_, _totalSupply), unitToken)), tokenPriceIncremental_)
    mul2 = Sub(_tokenAmount, unitToken)
    sub1 = Mul(mul1, mul2)
    sub2 = Div(Mul(tokenPriceIncremental_, Div(Sub(Pwr(_tokenAmount, 2), _tokenAmount), unitToken)), 2)
    div1 = Sub(sub1, sub2)
    res = Div(div1, unitToken)
    return res



def concatKey(str1,str2):
    return concat(concat(str1, '_'), str2)