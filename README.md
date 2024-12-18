# Secret Santa CLI

This is a Secret Santa gane CLI tool. It takes a `.yaml` file to configure the game, setting up the participants and the exclusions.

Then, uses [Mailgun API](https://documentation.mailgun.com/docs/mailgun/user-manual/get-started/) to send the results of the draw via email.

## Game config

```yaml
# Secret Santa game configuration
secret-santa:
  name: "Secret Santa Game 2024"
  notification:
    subject: "Secret Santa result!"  # Subject of the email
    template: "notification.html"  # Jinja2 template name from templates folder. Optional.
  participants:
    - name: Alice
      email: alice@example.com
    - name: Bob
      email: bob@example.com
    - name: Carol
      email: carol@example.com
    - name: Frank
      email: frank@example.com
    - name: Dan
      email: dan@example.com
  exclusions:
    - from: Alice
      to: Bob
      reverse: true  # If true, the exclusion to -> from is also added. False by default.
      comment: "They are a married"
```

## Environment variables

Some environment variables have to be set in order to use Mailgun API. YOu can also create a local `.env` file with the variables.

```
# Mailgun configuration
SANTA_MAILGUN_API_URL=
SANTA_MAILGUN_API_KEY=
```

## Usage

This package uses `uv` to handle the dependencies and virtual environment. The script can be executed by running:

```bash
uv run secretsanta <config_yaml_file> [--dry]
```

- `<config_yaml_file>`:
    Path to the YAML file with the game configuration.

- `--dry`:
    Optional argument, to simulate the draw and not sending the results via
    email.

- `--seed`:
    Optional argument, to define a string as the seed for the random module.
