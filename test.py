import datetime 

days_ago = 5
today = datetime.datetime.now()
target_date = today - datetime.timedelta(days = days_ago)
day = target_date.day
month = target_date.strftime('%b')
year = target_date.year
date_string = str(day) + "-" + month + "-" + str(year)
print(date_string)