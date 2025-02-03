import json

data = [

    {
    "Hostname": "nico",
    "ip": "192.168.100.10",
    "port": 80,
    },
    {
    "Hostname": "nico",
    "ip": "192.168.100.10",
    "port": 80
}
]
with open("D:/cours/B3/mspr/scan.json", "w") as f:
    json.dump(data, f)