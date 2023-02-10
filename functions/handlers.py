import traceback
from datetime import datetime, timedelta

from boto3.dynamodb.conditions import Key
from helper import feed_currencies, fetch_from_table, response


def feed_currencies_handler(event, context):
    """
    This function is triggered via EventBridge Scheduled Event (cron expressions) whitch executes 16:00 AM (UTC) every day
        1. Downlaods the xml feed from the remote url
        2. Parses the data into a list of <currency_code, rate>
        3. Inserts the data into a dynamodb table avoiding the dupliction of data for same day
    """
    try:
        feed_currencies()
        return response(200, {"success": True})
    except Exception as error:
        trace = str(traceback.format_exc())
        print(f"exception: {str(error)}: {trace}")
        return response(500, {"error": "Something went wrong!"})


def get_currencies_handler(event, context):
    """
    This function is triggered via api gateway event (Rest Api)
    It loads the needed data from dynamodb table and prepares the json data to be retured to the client
    """
    formate = "%Y-%m-%d"
    try:
        """find the data for the most recent day starting from today and go back -1 day"""
        recent_date = datetime.today()
        counter = 0
        while True:
            currencies_today = fetch_from_table(
                Key("date").eq(recent_date.strftime(formate))
            )
            if len(currencies_today) > 0:
                break
            else:
                # go back -1 day and find the data
                recent_date -= timedelta(days=1)

            counter += 1
            if counter > 5:
                raise Exception("No recent data found")

        recent_previous_date = recent_date - timedelta(days=1)
        currencies_yesterday = fetch_from_table(
            Key("date").eq(recent_previous_date.strftime(formate))
        )

        # in case the data for only one day (for the first time only) then clone the new data for previous day as well
        if len(currencies_yesterday) == 0:
            print("only one day data found")
            currencies_yesterday = currencies_today.copy()

        yesterday_rate = {}
        for item in currencies_yesterday:
            yesterday_rate[item["currency_code"]] = item["rate"]

        all_rates = {}
        fluctuations = {}
        for item in currencies_today:
            all_rates[item["currency_code"]] = item["rate"]
            last_rate = yesterday_rate.get(item["currency_code"], item["rate"])
            diff = item["rate"] - last_rate
            fluctuations[item["currency_code"]] = f"+{diff}" if diff > 0 else diff
        result = {"rates": all_rates, "fluctuations": fluctuations}
        return response(200, result)
    except Exception as error:
        trace = str(traceback.format_exc())
        print(f"exception: {str(error)}: {trace}")
        return response(500, {"error": "Something went wrong!"})
