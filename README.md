

This is a Python application that runs a Telegram bot and utilizes OpenAI's GPT-3 API. It is built on top of the `python:slim` Docker image and uses the PDM package manager for Python dependencies.

## Usage

Before you can run the application, you need to have the following environment variables set:

- `ADMIN_USER_IDS`: a comma-separated list of Telegram user IDs that have administrative access to the bot
- `TELEGRAM_TOKEN`: the Telegram bot token
- `OPENAI_TOKEN`: the OpenAI API token
- `FERNET_KEY`: a secret key used for Fernet encryption
- `POLL_TYPE`: the type of poll to use (either `WEBHOOK` or `POLLING`)
- `DOMAIN`: the public domain name of the server where the bot will be hosted
- `PORT`: the port number to use for the web server

To build and run the application, you can use the following commands:

```bash
# Build the Docker image
docker build -t my-telegram-bot .

# Run the Docker container
docker run -e ADMIN_USER_IDS=<user_ids> \
           -e TELEGRAM_TOKEN=<telegram_token> \
           -e OPENAI_TOKEN=<openai_token> \
           -e FERNET_KEY=<fernet_key> \
           -e POLL_TYPE=<poll_type> \
           -e DOMAIN=<domain> \
           -e PORT=<port> \
           -p <expose_port>:<port> \
           my-telegram-bot
```
### Database Migrations

You need to make changes to the database schema, you can use Alembic to manage database migrations. 


To apply the migrations, you can use the `alembic upgrade` command:

```bash
DATABASE_URL=<database_url> alembic upgrade head
```

This will apply all of the pending migrations to the database.

Note that you will need to include the `DATABASE_URL` environment variable when running Alembic commands, just like you do when running the main application container.

## Usage

Once the application is running, you can interact with the Telegram bot by searching for it in the Telegram app and sending it messages. The bot will respond to certain commands and messages based on the code in the `app` directory.

If you need to modify the code or add new dependencies, you can do so in the `pyproject.toml` file, and then run `pdm install` to install the updated dependencies.