# How to Deploy the Bot to Heroku or Locally

## Running Locally

If you want to see the magic of the telegram bot happen on your computer, just go to the `main.py` and set deploy to `False` and run the file `deploy=False`.

Then run the file `main.py` and you should see the bot running on your terminal.

Make sure you have the environment variables and all dependencies are installed.

*Please note that if the bot is running in production this will not work as the bot will be running on Heroku.*

## Deploying the Bot subfolder to Heroku Git without deploying the whole repo


*The following steps have already been performed and do not need to be run again, this is just for future reference*

To deploy only the bot subfolder, specify the subtree path and the remote branch to push to:

```git subtree push --prefix bot heroku <local_branch>:master```

## Set environment Variables on Heroku

Once the app has been deployed, you will need to set the following environment variables on Heroku:

Navigate to:

`Heroku > Settings > Config Vars > Add`

Add the environmental variables.