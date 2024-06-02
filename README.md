<p align="center">
  <img alt="My Crypto Gem" src="https://github.com/TimTrademark/cryptogem-bot/raw/main/control_panel/static/images/logo.png">
</p>

## Your companion that automatically buys new crypto gems 💎

<a href="https://www.mycryptogem.com" target="_blank">MyCryptoGem</a> is an open-source bot that scans exchanges and
automatically buys new crypto listings.

## Exchanges that are currently supported 📈

- MEXC
- Kucoin
- Gate.io

## Configuration

Configure the bot with ease using the web control panel.

<p align="center">
  <img alt="My Crypto Gem" src="https://github.com/TimTrademark/cryptogem-bot/raw/main/control_panel/static/images/control_panel_config_preview.png">
</p>

> Disclaimer: It is not recommended to host the control panel on a public facing machine, as it is not production-ready.
> You can disable the web control panel by inserting `ENABLE_CONTROL_PANEL=FALSE` in the `.env` file.

Alternatively, the config.json file can be edited manually according to your needs:

```json
{
  "exchanges": {
    "mexc": {
      "api_key": "MY_API_KEY",
      "api_secret": "MY_API_SECRET",
      "funds": 6,
      "active": true
    }
  },
  "scheduling_timeout_seconds": 5
}
```

## Running the bot

It is recommended to run the bot using Docker:

```commandline
docker build -t mycryptogem .
docker run -d -p 0.0.0.0:5000:5000 mycryptogem
```

You can also provide a config.json to the Docker container:

```commandline
docker run -v C:/config_custom.json:/app/config.json mycryptogem
```

## Development

You are free to open pull requests or create issues, I will try to get to them as soon as possible. The bot is in active
development, so expect more features and changes soon!

Planned features are:

* Monthly/weekly/daily Budget limits 📅
* More exchange integrations 📈
* Integrating trade history in control panel 📜

