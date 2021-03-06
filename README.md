
# OANDA-Broker Python

OANDA-Broker simple CLI With Python

## project setup
```bash
make bootstrap
source env/bin/activate
python setup.py develop
```

## application properties configuration
```
broker.url = $oanda_broker_url$
broker.account-primary = $your_primary_account$
broker.api-token = $your_broker_api_token$
```

## source code

| Source File | Entry Point | Description |
| ----------- | ----------- | ----------- |
| `src/account/account.py` | ob-accounts | Accounts List and Account Details |
| `src/account/instrument.py` | ob-instruments | Instruments Details |
| `src/account/trade.py` | ob-trades | Trade Details and Actions |
| `src/account/chart.py` | ob-charts | Print Charts in CSV or PNG File |

## CLI-commands (examples)
```
ob-accounts list
ob-accounts details-primary --account $account_id

ob-instruments list --account $account_id
ob-instruments candles --instrument EUR_USD --count 15 --granularity M15

ob-trades list --account $account_id
ob-trades stop --state LOSS

ob-charts print_chart --instrument EUR_USD,GBP_USD --count 50 --options data_visible

(....) and more

```

## todo

* **unit tests** - add test system

## versioning

* **0.0.3** - *multi-charts support*
* **0.0.2** - *charts support*
* **0.0.1** - *initial work*

## authors

**alberto massa**, [contact me](https://www.facebook.com/albertomassa.info)
