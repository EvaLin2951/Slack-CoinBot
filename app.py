import os
from slack_bolt import App
import Account

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("message")
def handle_message_events(event, say, client):
    # Ignore messages from bots or without text content
    if 'subtype' in event and event['subtype'] == 'bot_message':
        return
    
    print(event)
    
    user_id = event['user']
    try:
        # Fetch user information
        result = client.users_info(user=user_id)
        # Check if user info is available and email is present
        if result and result['user'] and 'email' in result['user']['profile']:
            user_email = result['user']['profile']['email']
            print("Hi there! Your email is: ", user_email)
            
        else:
            say("Email not found or access denied.")
    except Exception as e:
        print(f"Error retrieving user information: {e}")




# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 80)))

