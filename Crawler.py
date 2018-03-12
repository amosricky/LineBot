import Crawler_nbshopping
import schedule
import time

def job(message='stuff'):
    print("I'm working on:", message)


if __name__ == '__main__':
    schedule.every(10).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
# schedule.every(10).seconds.do(job)
#
# while True:
#      schedule.run_pending()
#      time.sleep(1)