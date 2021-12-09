import csv
import schedule
from datetime import datetime
from tcp_latency import  measure_latency
import time

dns_servers = {
    'Google':['8.8.8.8','8.8.4.4'],
    'Quad9':['9.9.9.9','149.112.112.112'],
    'OpenDNS Home':['208.67.222.222','208.67.220.220'],
    'CloudFlare':['1.1.1.1','1.0.0.1'],
    'CleanBrowsing':['185.228.168.9','185.228.169.9'],
    'Alternate DNS':['76.76.19.19','76.223.122.150'],
    'AdGuard DNS':['94.140.14.14','94.140.15.15']
    }

#measure_latency(host='52.26.14.11', port=80, runs=10, timeout=2.5)
def write_csv(data):
  with open('dns_latency.csv', 'a', encoding='UTF8',newline='\n') as f:
      writer = csv.writer(f)
      writer.writerow(data)

def latency(dict, key,position):
    latency = measure_latency(host=dict[key][position],timeout=10)
    if position == 0:
        tp = 'Primary'
    else:
        tp = 'Secondary'
    data = [datetime.now(),key,tp,latency]
    write_csv(data)

def run():
  for i in range(2):
    for key in dns_servers:
      latency(dns_servers,key,i)

schedule.every().hour.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)