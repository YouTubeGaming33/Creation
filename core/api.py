import requests

urlBase = "http://YOUR_ORACLE_VM_PUBLIC_IP:8000/"
headers = {
    "X-API-Key": "your_super_secret_portfolio_token_here"
}

response = requests.get(urlBase, headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"Server Memory Usage: {data['memory']['percent_used']}%")
else:
    print(f"Error: {response.status_code} - {response.text}")


def pullMetrics(requestedMetric:str, urlBase, headers=headers):
    try:
        response = requests.get(urlBase+"metrics", headers=headers)
        data = response.json()
        print(f"Requested Metric {data['requestedMetric']}")
    except:
        print(f"Error: {response.status_code} - {response.text}")


def pull_metric(requestedMetric:str, urlBase, headers=headers):
    try:
        response = requests.get(urlBase+"metrics", headers=headers)
        data = response.json()

        requestedMetric = requestedMetric.lower()

        if requestedMetric == "cpu":
            percentageOverall = (f"{data["cpu"]["percent_overall"]}")
            coresCount = (f"{data["cpu"]["cores_count"]}")
            loadAverage = ()