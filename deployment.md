# How to Deploy the Bot to Heroku or Locally

## Running Locally

To run locally, use:
```python3 main.py```

*To run in production*
`python3 main.py --deploy` or `python3 main.py -d`

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