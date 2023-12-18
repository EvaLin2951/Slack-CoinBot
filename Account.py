import pymongo
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['slackCoinBot']
coin_accounts = db['coin_accounts']
coin_flows = db['coin_flows']

class Account:
    def __init__(self, slack_user_id, email, coin_balance, created_at, updated_at):
        self.slack_user_id = slack_user_id
        self.email = email
        self.coin_balance = coin_balance
        self.is_admin = False
        self.created_at = created_at
        self.updated_at = updated_at
        
def bind_account(slack_user_id, email):
    # Check if an account with the same slack_user_id already exists
    if coin_accounts.count_documents({'slack_user_id': slack_user_id}) > 0:
        return "Your account has already been bound"

    # Check if an account with the same email already exists
    query = {'email': email}
    result = coin_accounts.find_one(query)
    if result is None:
        # If no account exists with the email, create a new one
        created_at = int(datetime.now().timestamp())
        new_account = Account(slack_user_id, email, 100, created_at, created_at)
        coin_accounts.insert_one(new_account.__dict__)
    else:
        # If an account with the same email exists, bind it to the slack_user_id
        coin_accounts.update_one(query, {'$set': {'slack_user_id': slack_user_id}})
    return "Account binding successful"

def get_balance(slack_user_id):
    # Check if an account with the same slack_user_id exists
    if coin_accounts.count_documents({'slack_user_id': slack_user_id}) == 0:
        return "Your account has not been bound yet"
    
    # If an account with the same slack_user_id exists, return its coin balance
    account_balance = coin_accounts.find_one({'slack_user_id': slack_user_id})['coin_balance']
    return "Your coin balance is " + str(account_balance)

def transfer_coin(slack_user_id, email, to_email, amount):
    from_query = {'slack_user_id': slack_user_id}
    to_query = {'email': to_email}
    
    # Check if an account with the same slack_user_id exists
    if coin_accounts.count_documents(from_query) == 0:
        return "Your account has not been bound yet"
    
    # Check if the target account exists
    if coin_accounts.count_documents(to_query) == 0:
        return "The target account does not exist"
    
    # If both coin_accounts exist, transfer the coin if the account's balance is sufficient
    with client.start_session() as session:
        with session.start_transaction():

            updated_at = int(datetime.now().timestamp())
            from_query['coin_balance'] = {'$gte': amount}
            result = coin_accounts.update_one(from_query, {'$inc': {'coin_balance': -amount}, '$set': {'updated_at': updated_at}})
            if result.modified_count == 0:
                return "Insufficient coin balance"
            coin_accounts.update_one(to_query, {'$inc': {'coin_balance': amount}, '$set': {'updated_at': updated_at}})
            
            coin_flows.insert_one({'email': email, 'to_email': to_email, 'change_amount': -amount, 'date_time': updated_at})
            coin_flows.insert_one({'email': to_email, 'from_email': email, 'change_amount': amount, 'date_time': updated_at})

    return "Coin transfer successful, you now have " + str(coin_accounts.find_one(from_query)['coin_balance']) + " coins"

def admin_add_coin(slack_user_id, to_email, amount):
    admin_query = {'slack_user_id': slack_user_id, 'is_admin': True}
    to_query = {'email': to_email}
    
    # Check if an account with the same slack_user_id exists and is an admin
    if coin_accounts.count_documents(admin_query) == 0:
        return "Your account has not been bound yet or you are not an admin"
    
    # If an account with the same slack_user_id exists, check if the target account exists
    if coin_accounts.count_documents(to_query) == 0:
        return "The target account does not exist"
    
    # If both coin_accounts exist, transfer the coin
    updated_at = int(datetime.now().timestamp())
    coin_accounts.update_one(to_query, {'$inc': {'coin_balance': amount}, '$set': {'updated_at': updated_at}})
    
    coin_flows.insert_one({'email': to_email, 'change_amount': amount, 'date_time': updated_at})

    return "Coin added successfully"
