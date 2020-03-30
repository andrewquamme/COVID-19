import csv
import config
import mysql.connector
from datetime import datetime

def parse_data(filename):
    infile = open(filename, 'r')
    csvreader = csv.reader(infile)
    result = []
    for entry in csvreader:
        if entry[0][0].isdigit():
            result.append(entry)
    return result
    
    infile.close()

def calc_usa_numbers(entries):
    curr = entries[0][0]
    case_count = 0
    death_count = 0
    result = []
    for entry in entries:
        if entry[0] == curr:
            case_count += int(entry[3])
            death_count += int(entry[4])
        else:
            result.append([curr, case_count, death_count])
            curr = entry[0]
            case_count = 0
            death_count = 0
    result.append([curr, case_count, death_count])
    return result

def add_to_db(table, entries, log):
    mydb = mysql.connector.connect(**config.mysql)
    cursor = mydb.cursor()

    sql = f"TRUNCATE TABLE {table}"
    cursor.execute(sql)

    if table == "usa":
        sql = ("INSERT INTO usa "
        "(date, cases, deaths) "
        "VALUES (%s, %s, %s)")
        for entry in entries:
            val = (entry[0], entry[1], entry[2])
            try:
                cursor.execute(sql, val)
                mydb.commit()
            except:
                log.write(f"Error on: {entry}\n")
    
    elif table == "states":
        sql = ("INSERT INTO states "
        "(date, state, cases, deaths) "
        "VALUES (%s, %s, %s, %s)")
        for entry in entries:
            val = (entry[0], entry[1], int(entry[3]), int(entry[4]))
            try:
                cursor.execute(sql, val)
                mydb.commit()
            except:
                log.write(f"Error on: {entry}\n")

    elif table == "counties":
        sql = ("INSERT INTO counties "
        "(date, county, state, cases, deaths) "
        "VALUES (%s, %s, %s, %s, %s)")
        for entry in entries:
            val = (entry[0], entry[1], entry[2], int(entry[4]), int(entry[5]))
            try:
                cursor.execute(sql, val)
                mydb.commit()
            except:
                log.write(f"Error on: {entry}\n")

    cursor.close()
    mydb.close()

def main():
    log = open('/home/andrew/dev/covid/log.txt', 'a+')
    log.write(f"Started at {datetime.now()}\n")

    start = datetime.now()
    states = parse_data("/home/andrew/dev/covid/us-states.csv")
    add_to_db("states", states, log)
    usa = calc_usa_numbers(states)
    add_to_db("usa", usa, log)
    stop = datetime.now()
    log.write(f"US/States: {len(states)} records processed in {(stop-start).seconds} seconds\n")

    start = datetime.now()
    counties = parse_data("/home/andrew/dev/covid/us-counties.csv")
    add_to_db("counties", counties, log)
    stop = datetime.now()
    log.write(f"Counties: {len(counties)} records processed in {(stop-start).seconds} seconds\n")

    log.write(f"Finished: {datetime.now()}\n\n")
    log.close()

if __name__ == "__main__":
    main()
