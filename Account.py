import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['slackCoinBot']
accounts = db['accounts']

class Account:
    def __init__(self, slack_id, slack_email, coin_balance):
        self.slack_id = slack_id
        self.slack_email = slack_email
        self.coin_balance = coin_balance
        self.is_admin = False
        
def bind_account(slack_id, slack_email):
    # Check if an account with the same slack_id already exists
    if accounts.count_documents({'slack_id': slack_id}) > 0:
        return "Your account has already been bound"

    # Check if an account with the same slack_email already exists
    query = {'slack_email': slack_email}
    result = accounts.find_one(query)
    if result is None:
        # If no account exists with the slack_email, create a new one
        new_account = {"slack_id": slack_id, "slack_email": slack_email, "coin_balance": 0, "is_admin": False}
        accounts.insert_one(new_account)
    else:
        # If an account with the same email exists, bind it to the slack_id
        accounts.update_one(query, {'$set': {'slack_id': slack_id}})
    return "Account binding successful"

def get_balance(slack_id):
    # Check if an account with the same slack_id exists
    if accounts.count_documents({'slack_id': slack_id}) == 0:
        return "Your account has not been bound yet"
    
    # If an account with the same slack_id exists, return its coin balance
    account = accounts.find_one({'slack_id': slack_id})
    return "Your coin balance is " + account['coin_balance']

def transfer_coin(slack_id, target_slack_email, amount):
    from_query = {'slack_id': slack_id}
    to_query = {'slack_email': target_slack_email}
    
    # Check if an account with the same slack_id exists
    if accounts.count_documents(from_query) == 0:
        return "Your account has not been bound yet"
    
    # If an account with the same slack_id exists, check if the target account exists
    if accounts.count_documents(to_query) == 0:
        return "The target account does not exist"
    
    # If both accounts exist, transfer the coin
    account = accounts.find_one(from_query)
    target_account = accounts.find_one(to_query)
    account['coin_balance'] -= amount
    target_account['coin_balance'] += amount
    accounts.update_one(from_query, {'$set': {'coin_balance': account['coin_balance']}})
    accounts.update_one(to_query, {'$set': {'coin_balance': target_account['coin_balance']}})
    return "Coin transfer successful, you now have " + str(account['coin_balance']) + " coins"

def admin_add_coin(slack_id, target_slack_email, amount):
    admin_query = {'slack_id': slack_id, 'is_admin': True}
    to_query = {'slack_email': target_slack_email}
    
    # Check if an account with the same slack_id exists and is an admin
    if accounts.count_documents(admin_query) == 0:
        return "Your account has not been bound yet or you are not an admin"
    
    # If an account with the same slack_id exists, check if the target account exists
    if accounts.count_documents(to_query) == 0:
        return "The target account does not exist"
    
    # If both accounts exist, transfer the coin
    target_account = accounts.find_one(to_query)
    target_account['coin_balance'] += amount
    accounts.update_one(to_query, {'$set': {'coin_balance': target_account['coin_balance']}})
    return "Coin added successfully"