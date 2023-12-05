# How to Deploy the Bot to Heroku or Locally

## Running Locally

To run locally, use:
```python3 app.py```

*To run in production*
`python3 app.py --deploy` or `python3 app.py -d`

Make sure you have the environment variables and all dependencies are installed.

## Set environment Variables on Heroku

Once the app has been deployed, you will need to set the following environment variables on Heroku:

Navigate to:

`Heroku > Settings > Config Vars > Add`

Add the environmental variables.