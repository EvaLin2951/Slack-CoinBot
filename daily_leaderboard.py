import datetime
import Account
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def leaderboard():
    date = datetime.now().strftime("%Y-%m-%d")
    leaderboard = "Coin Leaderboard (" + date + "):\n\n"

    sorted_accounts = Account.coin_accounts.find().sort('coin_balance', -1)
    order = 1
    for account in sorted_accounts:
        leaderboard += str(order) + ". {}: {}\n".format(account['email'], account['coin_balance'])
        order += 1
    leaderboard += "\n\n🎉 🎉 🎉"

    return leaderboard

def send(token, channel, message):
    client = WebClient(token=token)

    try:
        client.chat_postMessage(channel=channel, text=message)
        print(f"Message sent to channel {channel}")
    except SlackApiError as e:
        print(f"Error sending message: {e}")
