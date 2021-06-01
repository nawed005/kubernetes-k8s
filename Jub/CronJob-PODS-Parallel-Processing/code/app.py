import time
from datetime import date

def main():
    while True:
        today = date.today().strftime('%d-%m-%Y')
        print(today)
        time.sleep(60)

if __name__ == "__main__":
    main()      