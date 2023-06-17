# Calendar sync bot for Telegram

This bot synchronizes one or more `.ical` feeds to a telegram group.

## Settings

1. Copy `.env.example` to `.env`, and modify as needed.
2. Edit [brony_meetup_bot](brony_meetup_bot)/[settings.py](brony_meetup_bot/settings.py) as needed.


## Database setup
- use a postgres container
- Create user and database
  ```shell
   docker compose exec postgres psql -h postgres_container_name -U postgres_admin_account
    # optionally: DROP DATABASE IF EXISTS calendar_sync;
    CREATE USER calendar_sync WITH PASSWORD '>!!!--- INSERT YOUR SHIT HERE ---!!!!<';
    # ALTER USER calendar_sync WITH PASSWORD '>!!!--- INSERT YOUR SHIT HERE ---!!!!<';
    CREATE DATABASE calendar_sync;
    GRANT ALL ON DATABASE calendar_sync TO calendar_sync;
    \q
   ```
- Get table definitions needed.
  ```shell
  docker compose build calendar_sync
  docker compose run --rm --name calendar_sync_models  calendar_sync  python models.py
  ```
- Put that definitions into the database
  ```shell
  docker compose exec postgres psql -h postgres_container_name -U calendar_sync
  
  # paste stuff from the models.py
  ```
