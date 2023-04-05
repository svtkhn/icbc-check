import requests
import json 
import datetime
import os
from twilio.rest import Client

def lambda_handler(event, context):
    url = "https://onlinebusiness.icbc.com/deas-api/v1/webLogin/webLogin"
    payload = "{\"drvrLastName\":\"LAST\",\"licenceNumber\":\"LICENSE\",\"keyword\":\"KEYWORD\"}"
    headers={
        "Host":"onlinebusiness.icbc.com",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Content-Type":"application/json",
        "Content-Length":"74",
    }

    response = requests.put(url, headers=headers, data=payload)
    booked_string_date = json.loads(response.text)['webAappointments'][0]['appointmentDt']['date']
    booked_date = datetime.datetime.strptime(booked_string_date, "%Y-%m-%d").date()

    auth = response.headers['Authorization']

    url = "https://onlinebusiness.icbc.com/deas-api/v1/web/getAvailableAppointments"
    payload = "{\"aPosID\":9,\"examType\":\"7-R-1\",\"examDate\":\"2023-03-10\",\"ignoreReserveTime\":false,\"prfDaysOfWeek\":\"[0,1,2,3,4,5,6]\",\"prfPartsOfDay\":\"[0,1]\",\"lastName\":\"LAST\",\"licenseNumber\":\"LICENSE\"}"
    headers = {
        'Host': 'onlinebusiness.icbc.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Content-Type': 'application/json',
        'Content-Length': '188',
        'Authorization': auth,
    }

    response = requests.post(url, headers=headers, data=payload)
    jsonresp = json.loads(response.text)

    threshold_date = datetime.datetime.strptime('2023-05-29', "%Y-%m-%d").date()


    print("booked date:", booked_date)
    for item in jsonresp:
        string_date = item['appointmentDt']['date']
        date = datetime.datetime.strptime(string_date, "%Y-%m-%d").date()
        print("appointment date:", date)
        if (date <= booked_date):
            print("found earlier:", date)
            client = Client("AC5809cfac6305f120f2f1eb95fbd550d8", "32d843d5252494b7ba9da9c7336249f7")
            message = client.messages.create(
                body="ICBC | Earlier booking available: " + str(date),
                from_="+12765288151",
                to="phone_number"
            )
            break
        
        if (date <= threshold_date):
            print("found below threshold:", date)
            # client = Client("AC5809cfac6305f120f2f1eb95fbd550d8", "32d843d5252494b7ba9da9c7336249f7")
            # message = client.messages.create(
            #     body="ICBC | Threshold crossed appointment: " + str(date),
            #     from_="+12765288151",
            #     to="+16043382134"
            # )


# lambda_handler(None, None)