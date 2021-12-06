import requests

data = {'req_rate_app1': "2" ,
'req_rate_app2': "4" 
}
result =  requests.post("http://localhost:5004/renew_db", json=data, timeout=45)