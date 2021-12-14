import requests

data = {'req_rate_app1': "7" ,
'req_rate_app2': "0", 
'time_passed_since_last_event' : "0" 
}
result =  requests.post("http://localhost:5004/renew_db", json=data, timeout=45)