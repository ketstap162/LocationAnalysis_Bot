# LocationAnalysis Telegram Bot

This Telegram bot forms a report asking questions to the user. 
The generated report is sent to ChatGPT for analysis, after which it gives appropriate advice.

The infrastructure of this bot is flexible to changes because 
it is enough to change the questions in settings like other parameters.

## How to start

1. Configure `.env` file by `.env.sample`.
2. Configure settings in `core/settings.py`
3. Build docker container using `docker-compose build` command in Terminal.
4. Run docker-compose using `docker-compose up`

## Additional features
The `docker-compose.yml` is the completed file 
that allow you to connect Postgres and Redis.
