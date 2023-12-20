import datetime


def get_last_week_date():

    # Get current date
    cur = datetime.datetime.now() - datetime.timedelta(days=7)

    # Format current date
    curd = f"{cur.year}-{cur.month}-{cur.day}"

    return curd