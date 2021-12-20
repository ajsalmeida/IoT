import csv
import schedule
from datetime import datetime
import time
import dns.resolver

dns_servers = {
    'Google':['8.8.8.8','8.8.4.4'],
    'Quad9':['9.9.9.9','149.112.112.112'],
    'OpenDNS Home':['208.67.222.222','208.67.220.220'],
    'CloudFlare':['1.1.1.1','1.0.0.1'],
    'CleanBrowsing':['185.228.168.9','185.228.169.9'],
    'AdGuard DNS':['94.140.14.14','94.140.15.15']
    }

my_resolver = dns.resolver.Resolver()
my_resolver.timeout = 40
my_resolver.lifetime = 40

#measure_latency(host='52.26.14.11', port=80, runs=10, timeout=2.5)
def write_csv(data):
  with open('wikipedia.csv', 'a', encoding='UTF8',newline='\n') as f:
      writer = csv.writer(f)
      writer.writerow(data)

def latency(dict, key,position):
    #latency = measure_latency(host=dict[key][position],timeout=10)
    print('testando resolução para: ',key,'-: ',dict[key][position])
    my_resolver.nameservers = [dict[key][position]]
    dns_start = time.time()
    my_resolver.query('wikipedia.org')
    #my_resolver.query('facebook.com')
    #my_resolver.query('yahoo.com')
    dns_end = time.time()
    dns_latency = (dns_end - dns_start) * 1000
    if position == 0:
        tp = 'Primary'
    else:
        tp = 'Secondary'

    date = datetime.now().date()
    time_clock = str(datetime.now().hour)+':'+str(datetime.now().minute)


    data = [date,time_clock,key,tp,dns_latency]

    write_csv(data)

def run():
  for i in range(2):
    for key in dns_servers:
      latency(dns_servers,key,i)

schedule.every().hour.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)