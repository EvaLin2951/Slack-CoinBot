import os
from slack_bolt import App
import Account
import random
import daily_leaderboard
import consts
from apscheduler.schedulers.blocking import BlockingScheduler


app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


@app.command("/bind")
def handle_command_bind(ack, say, client, command):
    ack()

    user_id = command['user_id']
    user_email = client.users_info(user=user_id)['user']['profile']['email']

    say(f"{Account.bind_account(user_id, user_email)}")

@app.command("/balance")
def handle_command_balance(ack, say, command):
    ack()

    user_id = command['user_id']

    say(f"{Account.get_balance(user_id)}")

@app.command("/transfer")
def handle_command_transfer(ack, say, client, command):
    ack()

    user_id = command['user_id']
    transfer_info = command['text'].split()
    if len(transfer_info) != 2:
        say("Invalid transfer format. Please use /transfer <to_email> <amount>")
        return
    to_email = transfer_info[0]
    amount = int(transfer_info[1])
    
    say(f"{Account.transfer_coin(user_id, to_email, amount)}")

    user_email = client.users_info(user=user_id)['user']['profile']['email']
    to_id = Account.coin_accounts.find_one({'email': to_email})["slack_user_id"]
    if to_id:
        message = "You have received " + str(amount) + " coins from " + user_email + ", you now have " + str(Account.coin_accounts.find_one({'email': to_email})["coin_balance"]) + " coins"
        client.chat_postMessage(channel=to_id, text=message)

@app.command("/add")
def handle_command_add(ack, say, client, command):
    ack()

    user_id = command['user_id']
    add_info = command['text'].split()
    if len(add_info) != 2:
        say("Invalid add format. Please use /add <to_email> <amount>")
        return
    to_email = add_info[0]
    amount = int(add_info[1])

    say(f"{Account.admin_add_coin(user_id, to_email, amount)}")

    to_id = Account.coin_accounts.find_one({'email': to_email})["slack_user_id"]
    if to_id:
        message = "You have received " + str(amount) + " coins, you now have " + str(Account.coin_accounts.find_one({'email': to_email})["coin_balance"]) + " coins"
        client.chat_postMessage(channel=to_id, text=message)


@app.event("message")
def handle_message_events(say):
    responses = ["Hello there!", "Hi!", "Greetings!"]
    random_response = random.choice(responses)

    say(random_response)


daily_job = daily_leaderboard.send(consts.access_token, consts.channel_id, daily_leaderboard.leaderboard())
def daily_job():
    scheduler = BlockingScheduler()
    scheduler.add_job(daily_job, 'cron', hour=9, minute=0)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 80)))
