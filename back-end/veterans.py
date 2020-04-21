# from bs4 import BeautifulSoup
# import requests
import config
import mysql.connector
from datetime import datetime
import time
import csv

# def get_soup(url):
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, features='html.parser')

#     html = open(f"{config.cwd}/VA/{time.strftime('%Y%m%d-%H%M')}.html", 'wb')
#     html.write(page.content)
#     html.close()

#     return soup


# def get_data(soup):
#     result = []
#     content = soup.find('div', attrs = {'id':'innerContentWrapper'})
#     findDate = 'ul ~ h3 ~ p'
#     findCases = 'h3 ~ p ~ p'
#     findDeaths = 'ul ~ p'

#     found = content.select(findDate)
#     for item in found:
#         if item.text[:10] == "Nationally":
#             result.append(get_date(item.text))
#             break

#     found = content.select(findCases)
#     for item in found:
#         if item.text[-22:] == "Positive Veteran Cases":
#             result.append(get_cases(item.text))
#             break

#     found = content.select(findDeaths)
#     for item in found:
#         if item.text[0:6] == "Deaths":
#             result.append(get_deaths(item.text))
#             break

#     return result


# def get_date(text):
#     i = 0
#     words = text.split(' ')
#     for word in words:
#         if is_month(word):
#             break
#         i+=1
#     return cleanup_date(words[i], words[i+1], words[i+2])


# def is_month(month):
#     months = [
#         'January',
#         'February',
#         'March',
#         'April',
#         'May',
#         'June',
#         'July',
#         'August',
#         'September',
#         'October',
#         'November',
#         'December'
#     ]

#     return month in months


# def cleanup_date(month, day, year):
#     months = {
#         "January": "01",
#         "February": "02",
#         "March": "03",
#         "April": "04",
#         "May": "05",
#         "June": "06",
#         "July": "07",
#         "August": "08",
#         "September": "09",
#         "October": "10",
#         "November": "11",
#         "December": "12",
#     }

#     mm = months[month]
#     dd = day.replace(',', '')
#     if (len(dd) < 2):
#         dd = '0'+dd
#     yyyy = year.replace(',', '')
    
#     return f"{yyyy}/{mm}/{dd}"


# def get_cases(text):
#     return int(text.split(' ')[0].replace(',', ''))


# def get_deaths(text):
#     return int(text.split(' ')[1])


def parse_data(filename):
    infile = open(filename, 'r')
    csvreader = csv.reader(infile)
    date = time.strftime('%Y/%m/%d')
    cases = 0
    deaths = 0
    for entry in csvreader:
        if entry[0][0].isdigit():
            cases += int(entry[2])
            deaths += int(entry[3])
    return [date, cases, deaths]


def check_if_in_db(entry):
    mydb = mysql.connector.connect(**config.mysql)
    cursor = mydb.cursor()

    sql = ("SELECT date "
        "FROM veterans "
        f"WHERE date = '{entry[0]}'")
    
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    mydb.close()
    if len(results) == 0:
        return False
    return True
    

def add_to_db(entry):
    mydb = mysql.connector.connect(**config.mysql)
    cursor = mydb.cursor()

    sql = ("INSERT INTO veterans "
        "(date, cases, deaths) "
        "VALUES (%s, %s, %s)")
    val = (entry[0], entry[1], entry[2])

    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()


def update_record(entry):
    mydb = mysql.connector.connect(**config.mysql)
    cursor = mydb.cursor()

    sql = ("UPDATE veterans "
        "SET cases = %s, deaths = %s "
        f"WHERE date = '{entry[0]}'")
    val = (entry[1], entry[2])

    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()


def main():
    log = open(f"{config.cwd}/log.txt", 'a+')
    log.write(f"Veterans started at {datetime.now()}\n")

    # url = 'https://www.publichealth.va.gov/n-coronavirus/'
    # soup = get_soup(url)
    # data = get_data(soup)

    data = parse_data(f"{config.cwd}/va.csv")
    print(data)

    try:
        if not check_if_in_db(data):
            add_to_db(data)
            log.write(f"Record added: {data}\n")
        else:
            update_record(data)
            log.write(f"Record updated: {data}\n")
    except:
        log.write(f"DB error on: {data}\n")

    log.write(f"Finished: {datetime.now()}\n\n")
    log.close()
    

if __name__ == "__main__":
    main()
