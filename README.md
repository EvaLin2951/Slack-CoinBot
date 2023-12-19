# Slack-CoinBot

During my Fall 2022 semester, my professor, Professor Campbell developed a virtual coin application on Slack to motivate student learning in the COMP202 course. Students will receive varying amounts of virtual coin rewards from the coin application for certain positive behaviours, as well as messages and leaderboards in the course's Slack workspace. I found this application created by the professor very interesting, so I have decided to replicate a similar one in my own Slack application.

Users can send Slash Commands to interact with CoinBot, executing actions such as balance inquiries and transfers. Account administrators have the additional capability to add coins to any account. Below is a simple diagram that illustrates the logic behind the commands:<br><br>
<img width="1680" alt="SlackCoinBot_CommandLogic_Diagram" src="https://github.com/EvaLin2951/slack-coinbot/assets/132865370/48322fc7-3173-4d58-80a3-b160ad924d94"><br>

CoinBot responds to commands sent via the Slack API to perform corresponding actions and utilizes MongoDB to keep track of account information. Additionally, CoinBot will push a leaderboard notification to a dedicated Slack channel at a fixed time every day. Here is a sequence diagram that shows the functioning of _/bind_ and _/transfer_ commands and the scheduled job:<br><br>
<img width="1464" alt="SlackCoinBot_Sequence_Diagram" src="https://github.com/EvaLin2951/slack-coinbot/assets/132865370/b553aebd-5258-4d59-ae1b-b0e57152a88c"><br>

