
import datetime
import pytz


def now():
    month = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
             7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    now_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    manila = pytz.timezone('Hongkong')
    manila_time = manila.normalize(now_utc.astimezone(manila))

    mn = month[manila_time.month]
    d = manila_time.day
    y = manila_time.year
    h = manila_time.hour
    m = manila_time.minute
    s = manila_time.second
    time = [mn]
    for t in [d, h, m, s]:
        if len(str(t)) == 1:
               t = '0'+str(t)
               time.append(t)
        else:
            time.append(t)

    return '{} {}, {} {}:{}:{}'.format(mn, time[1], y, time[2], time[3], time[4])
