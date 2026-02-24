# GitBot.

This will post to your twt profile if you follow these directions~

1. Make a twitter/x account if you dont have one
2. go to the this [twitter dev portal](https://console.x.com/) (to actually post you must have credits, i typically buy $5 USD in credits a few times a month because 1 post = $0.01 USD gone out of the credits.)
3. clone this repository into your github org/profile by forking.
4. Get Your twitter API/CLIENT keys, You will not need your bearer token so ignore that. API = Consumer in this instance, so if you see CONSUMER instead of API on twitter please keep that in mind.
5. Make sure your keys have READ & WRITE PERMISSIONS for twitter.
6. Add your API keys to the github repository secrets.
7. make a github App with the following config:

   - Repo Permissions: Metadata (read ONLY)
   - Select 1 repo: the gitbot repo
   - Webhook: uncheck active
   - generate a private key (github will download a `.pem` file.)
   - create app

  8. in your gitbot repo you will paste the APP_ID of your github app into a variable called `APP_ID`
  9. in the gitbot repo you will paste all of your github app private key into a variable called `APP_PRIVATE_KEY`
  10. In your desired project repos paste the script below into `.github/workflows/ping_bot.yml`
  11. make a test commit and check your twitter account!

## ping_bot.yml script

```yml
name: Ping Twitter Bot
on: [push]

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Send signal to GitBot Brain
        run: |
          curl -X POST \
          -H "Authorization: token ${{ secrets.BOT_TOKEN }}" \
          -H "Accept: application/vnd.github.v3+json" \
          https://api.github.com/repos/penne-not-pasta/GitBot/dispatches \
          -d '{"event_type": "tweet_trigger", "client_payload": { "repository": "'"$GITHUB_REPOSITORY"'" }}'
```
