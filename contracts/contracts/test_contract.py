from contracts.libs.SafeMath import Sub, Pwr, Sqrt, Add, Mul, Div
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash
from boa.builtins import ToScriptHash, concat
from boa.interop.System.Runtime import CheckWitness, Notify
from boa.interop.System.Storage import Get, GetContext, Put, Delete


from contracts.libs.SafeCheck import Require


name = "Proof of Weak Hands"
symbol = "P3D"
tokenSupply_ = 0
decimal = 8
dividendFee_ = 10
referralFee_ = 3
# 0.01 ONG
tokenPriceInitial_ = 10000000
tokenPriceIncremental_ = 10000000
# Ong decimal is 9
magnitude = Pwr(10, 9)

# proof of stake (defaults at 100 P3D tokens)
statingRequirement_ = Mul(100, magnitude)

ongContractAddress_ = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
selfAddr_ = GetExecutingScriptHash()
initial_admin_ = ToScriptHash("AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p")
ADMIN_PREFIX = "admin"
noneAdmin_ = True
TOKENBALANCE_PREFIX = bytearray(b'\x01')
DIVIDENDS_PREFIX = bytearray(b'\x02')
REFERRALBALANCE_PREFIX = bytearray(b'\x03')
PAYOUTSTO_PREFIX = bytearray(b'\0x04')

profitPerShare_ = 0


def main():
    a = 3
    b = 4
    c = Pwr(a, b)
    return c

def deploy():
    if not noneAdmin_:
        key = concatKey(ADMIN_PREFIX, initial_admin_)
        Put(GetContext(), key, True)
        return True
    return False


def buy(account, ongAmount, referredBy):
    """
    Converts all incoming ethereum to tokens for the caller,
    and passes down the referral addy (if any)
    """
    CheckWitness(account)
    _undividedDividends = Div(Mul(ongAmount, dividendFee_), 100)
    _referralBonus = Div(Mul(ongAmount, referralFee_), 100)
    _dividends = Sub(_undividedDividends, _referralBonus)
    _taxedOng = Sub(ongAmount - _undividedDividends)
    _amountOfTokens = OngToToken(_taxedOng)
    Require(_amountOfTokens > 0 & Add(_amountOfTokens, tokenSupply_) > tokenSupply_)
    if(referredBy != 0 &
    referredBy != account &
    tokenBalanceOf(referredBy) >= statingRequirement_
    ){
        i = 0
    }


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

def onlyAdmin(addr):
    key = concatKey(ADMIN_PREFIX, addr)
    value = Get(GetContext(), key)
    if value is True:
        return True
    else:
        return False


# ------------- Admin only functions begin ---------
def disableInitialStage(addr):
    """
    In case the amassador quota is not met,
    the administrator can manually disable the ambassador phase.

    """
    Require(onlyAdmin(addr))


def addAdmin(fromAdmin, newAdmin):
    Require(onlyAdmin(fromAdmin))
    key = concatKey(ADMIN_PREFIX, newAdmin)
    Put(GetContext(), key, True)
    Notify(["addAdmin", fromAdmin, newAdmin])
    return True


def deleteAdmin(fromAdmin, deletedAdmin):
    Require(onlyAdmin(fromAdmin, deletedAdmin))
    key = concatKey(ADMIN_PREFIX, deletedAdmin)
    Delete(GetContext(), key)
    Notify(["deleteAdmin", fromAdmin, deletedAdmin])


def setStakingRequirement(admin, _amountOfTokens):
    Require(onlyAdmin(admin))
    statingRequirement_ = _amountOfTokens
    Notify("statingRequirement", statingRequirement_)
    return True


def setName(admin, _name):
    Require(onlyAdmin(admin))
    name = _name
    return True


def setSymbol(admin, _symbol):
    Require(onlyAdmin(admin))
    symbol = _symbol
    return True


# ------------- Admin only functions end ---------

def totalOngBalance():
    # how to return the Ong balance of this contract
    # ?????????
    i = 0

def totalSupply():
    return tokenSupply_

def tokenBalanceOf(addr):
    key = concatKey(TOKENBALANCE_PREFIX, addr)
    return Get(GetContext(), key)

def ReferralBalanceOf(addr):
    key = concatKey(REFERRALBALANCE_PREFIX, addr)
    return Get(GetContext(), key)

def payOutToBalanceOf(addr):
    key = concatKey(PAYOUTSTO_PREFIX, addr)
    return Get(GetContext(), key)

def dividendsOf(addr):
    return Get(GetContext(), concat(DIVIDENDS_PREFIX, addr))

def sellPrice():
    """
    Return the price per P3D token
    """
    if (tokenSupply_ == 0):
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

def purchaseToken():
    i = 0

def OngToToken(ong):
    """
    Calculate Token price based on an amount of incoming ong
    """
    # p -- tokenPriceInitial_
    # s -- totalSupply_
    # q -- tokenPriceIncremental_
    # b -- ong
    # sqrt(p^2 + 2bq + q^2s^2 + 2pqs) - p
    # -----------------------------------  - s
    #				q
    sum1 = Add(Pwr(tokenPriceInitial_, 2), Mul(Mul(ong, tokenPriceIncremental_), 2))
    sum2 = Add(Mul(Pwr(tokenPriceIncremental_, 2), Pwr(tokenSupply_, 2)),
               Mul(Mul(2, tokenPriceInitial_), Mul(tokenPriceIncremental_, tokenSupply_)))
    sum = Add(sum1, sum2)
    res1 = Sub(sum, tokenPriceInitial_)
    div = Div(res1, tokenPriceIncremental_)
    res2 = Sub(div, tokenSupply_)
    return res2

def tokenToOng():
    # calculate token sell price
    i = 0

def concatKey(str1,str2):
    return concat(concat(str1, '_'), str2)