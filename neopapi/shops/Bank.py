from neopapi.core.browse import register_page
from neopapi.core.browse.Browser import BROWSER
import re
from neopapi.shops.Exceptions import BankException, WrongPINException
from neopapi.main import Account
from neopapi.main.Exceptions import OutOfMoneyException

register_page('bank.phtml',
              [],
              True)

bank_account_types = [{'name': 'Junior Saver', 'amount': 0},
                      {'name': 'Neopian Student', 'amount': 1000},
                      {'name': 'Bronze Saver', 'amount': 2500},
                      {'name': 'Silver Saver', 'amount': 5000},
                      {'name': 'Super Gold Plus', 'amount': 10000},
                      {'name': 'Platinum Extra', 'amount': 25000},
                      {'name': 'Double Platinum', 'amount': 50000},
                      {'name': 'Triple Platinum', 'amount': 75000},
                      {'name': 'Diamond Deposit', 'amount': 100000},
                      {'name': 'Diamond Deposit Plus', 'amount': 250000},
                      {'name': 'Diamond Deposit Gold', 'amount': 500000},
                      {'name': 'Millionaire Platinum', 'amount': 1000000},
                      {'name': 'Millionaire Double Platinum', 'amount': 2000000},
                      {'name': 'Millionaire Mega-Platinum', 'amount': 5000000},
                      {'name': 'Neopian Mega-Riches', 'amount': 7500000},
                      {'name': 'Ultimate Riches!', 'amount': 10000000}]
def _get_account_index(account_name):
    for i in range(len(bank_account_types)):
        if bank_account_types[i]['name'] == account_name:
            return i
    raise KeyError('Account type \'' + account_name + '\' does not exist')
    
def get_current_balance():
    """
    This function returns the amount of neopets the currently logged in user
    has on his bank account
    
    """
    bank_page = BROWSER.goto('bank.phtml')
    
    bank_balance_tag = bank_page.find('td', text='Current Balance:')
    
    return int(re.sub('\D', '', bank_balance_tag.find_next_sibling().text))

def get_account_type():
    """
    This function returns the account type the currently logged in user
    has on his bank account
    
    """
    bank_page = BROWSER.goto('bank.phtml')
    
    return bank_page.find('td', text='Account Type:').find_next_sibling().text.strip()

def withdraw(amount, pin=None):
    """
    This function withdraws the given amount from the currently logged in users
    bank account.
    The 'pin' parameter is only required and used if it is required by the neopian bank
    
    """
    bank_page = BROWSER.goto('bank.phtml')
    
    if get_current_balance() < amount:
        raise BankException('Not enough money on bank account to withdraw that amount')
    
    if 'Enter your PIN:' in bank_page.text:
        if pin is None:
            # A pin number is required
            raise WrongPINException('PIN is required to acces bank account')
   
        post_dict = {'amount': amount,
                     'pin': pin,
                     'type': 'withdraw'}
    else:
        post_dict = {'amount': 1,
                     'type': 'withdraw'}
    
    bank_page = BROWSER.post('process_bank.phtml', post_dict)
        
    if 'Sorry, but the PIN we have stored is not matching the one you entered' in bank_page.text:
        info = bank_page.find('div', class_='errormess')
        raise WrongPINException('Sorry, but the PIN neopets has stored is not matching the one you entered')
    if 'You do not have enough Neopoints' in bank_page.text:
        raise BankException('Not enought money on bank account to withdraw that amount')
    
    return get_current_balance()
        
def deposit(amount):
    """
    This function deposits the given amount on the currently logged in users bank
    
    """
    BROWSER.goto('bank.phtml')
    
    if Account.cash_on_hand() < amount:
        raise OutOfMoneyException('Depositing ' + amount + 'np on bank account')
    
    post_dict = {'amount': amount,
                 'type': 'deposit'}
    bank_page = BROWSER.post('process_bank.phtml', post_dict)
        
    if 'You do not have enough Neopoints to deposit that amount' in bank_page.text:
        raise OutOfMoneyException('Depositing ' + amount + 'np on bank account')
        
    return get_current_balance()
    
def collect_interest():
    """
    This method will collect the users' interest for the day.
        
    """
    bank_page = BROWSER.goto('bank.phtml')
    
    if 'You have already collected your interest today.' in bank_page.text:
        raise BankException('Interest already collected today')
    elif 'Sorry! You have deposited and/or withdrawn Neopoints today.' in bank_page.text:
        raise BankException('Couldn\'t collect interest today. Previous actions were taken')
    
    post_dict = {'type': 'interest'}
    bank_page = BROWSER.post('process_bank.phtml', post_dict)
    
    return get_current_balance()
    
def upgrade_account(extra_amount_to_deposit=1):
    """
    This method will upgrade the users' account to the highest level that is
    possible with the current amount on the account + the given extra amount.
    If no extra amount was given, 1 np will be deposited. If the user does
    not have enough money on hand to deposit the given amount, and 
    OutOfMoneyException will be raised.
    
    """
    BROWSER.goto('bank.phtml')
    
    current_account_type_index = _get_account_index(get_account_type())
    if current_account_type_index >= len(bank_account_types) - 1:
        # Already got best account type
        return get_current_balance()
    
    if (get_current_balance() + extra_amount_to_deposit) < bank_account_types[current_account_type_index + 1]['amount']:
        # Not enough money on bank account to upgrade
        return get_current_balance()
    
    if extra_amount_to_deposit > Account.cash_on_hand():
        raise OutOfMoneyException('Depositing ' + extra_amount_to_deposit + 'np while upgrading bank account')
    
    new_account_type_index = current_account_type_index
    while new_account_type_index < len(bank_account_types) - 1 and (get_current_balance() + extra_amount_to_deposit) >= bank_account_types[new_account_type_index + 1]['amount']:
        new_account_type_index += 1
        
    post_dict = {'account_type': new_account_type_index,
                 'amount': extra_amount_to_deposit,
                 'type': 'upgrade'}
    bank_page = BROWSER.post('process_bank.phtml', post_dict)
            
    if 'You do not have enough Neopoints to deposit that amount' in bank_page.text:
        raise OutOfMoneyException('Depositing ' + extra_amount_to_deposit + 'np while upgrading bank account')
            
    return get_current_balance()

def money_needed_for_upgrade(account_type_name=None):
    """
    This function returns the extra money needed on your bank account to upgrade
    your account type to the given account. If no account_type is given, the
    account type following your current account type will be used.
    
    """
    if account_type_name is None:
        account_type_name = min(len(bank_account_types) -1, _get_account_index(get_account_type()) + 1)
    
    wanted_index = _get_account_index(account_type_name)
    
    return max(0, bank_account_types[wanted_index]['amount'] - get_current_balance())
        
