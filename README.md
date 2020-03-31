# COVID-19 Data Visualization

## Deployed URL
http://k7asq.ham-radio-op.net/covid/

## Data Sources
https://github.com/nytimes/covid-19-data 
https://www.publichealth.va.gov/n-coronavirus/

## Purpose
### Background
As a personal interest during this worldwide pandemic, I was looking for a way to visualize local COVID-19 data for Pima County, Arizona. Current numbers can be found in every newspaper across the world, but it was hard to find time-series data to visualize the growth in cases (and sadly deaths). I finally found a website ran by the county government that was updated by a human every morning. Because cases in the county were relatively new, it was no problem to enter the information into a spreadsheet and then graph it.
### A Growing Desire
After one week, I soon realized I wanted more information. After talking with a few friends, I found that they wanted more information as well. I moved my hand-entered data to a MySQL database on my Raspberry Pi, did a quick brain refresh on JavaScript and PHP (hey, it's been a while) and made a quick front end for my data hosted on the Pi's Apache Web Server. Once that was running, I began searching for raw data and finally came across a GitHub project with state-by-state and county-by-county information for cases in the US, updated daily, with a daily history back to the first reported cases.
### Fun with Computer Science
I downloaded the data, built a larger database, wrote scripts to parse the raw data into the database, and worked on the front end to display it all (after I finished my homework, of course). After a few hours of work over the weekend, everything is now automated and up and running.

## How it Works
### The Back End
Data is downloaded from https://github.com/nytimes/covid-19-data with `curl` to the Raspberry Pi daily at 0700 and 1900 MST using `crontab`. At 0705 and 1905, a `Python` script runs that goes through each file and updates the data in the `MySQL` database. The daily state data is used to calculate the data for the United States as a whole. Veterans Affairs data is not easily found, so I hand enter it when I can. Historical VA data was found using the Wayback Machine and so is missing some reported information.
*NOTE: This data does vary from day-to-day comapred to other sources.*
### The Front End
Using `PHP` on the Raspberry Pi's *LAMP* server, requests are handled and processed to return a `JSON` object with the requested information.  
*NOTE: This endpoint on the server can also function as a pseudo API for your own personal project! (more below)* 

Using `HTML`, `CSS`, `JS`, `JQuery` and `Chart.js` queries are sent to the `PHP` server to populate the states, counties, and visuals with user selections.  
*NOTE: Because the actual data is used to populate the State/County select elements, there is a potential that a state/county will not be in the list when there are no reported cases.*

## REST API
Endpoint: `http://k7asq.ham-radio-op.net/covid/data/data.php`

### Get List of States
#### Request
`GET ?query=getStates`
#### Response
```
[
    {
        "state": "Alabama"
    },
    {
        "state": "Alaska"
    },
    {
        "state": "Arizona"
    },
    { ...
    },
    {
        "state": "Wyoming"
    }
]
```

### Get List of Counties for State
#### Request
`GET ?query=getCounties&state='State'`
#### Response
```
[
    {
        "county": "Apache"
    },
    {
        "county": "Cochise"
    },
    { ... 
    }.
    {
        "county": "Yuma"
    }
]
```

### Get COVID-19 Data for State, United States, or Veterans Affairs
#### Request
`GET ?query=getData&state='State'` or `GET ?query=getData&state=United States` or `GET ?query=getData&state=Veterans Affairs`
#### Response
```
[
    {
        "date": "2020-01-26",
        "cases": "1",
        "deaths": "0"
    },
    { ...
    },
    {
        "date": "2020-03-28",
        "cases": "773",
        "deaths": "15"
    }
]
```

### Get COVID-19 Data for County
#### Request
`getData&state='State'&county='County'`
#### Response
```
[
    {
        "date": "2020-03-09",
        "cases": "1",
        "deaths": "0"
    },
    { ...
    },
    {
        "date": "2020-03-28",
        "cases": "120",
        "deaths": "5"
    }
]
```
