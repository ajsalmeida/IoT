import random
import serial #conda install pyserial ou pip install pyserial
import time
from paho.mqtt import client as mqtt_client #conda install paho-mqtt ou pip install paho-mqtt

#definição conexão serial
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(5)

#definição dados do broker
broker = 'localhost'
port = 1883
topic1 = 'SB/umid'
topic2 = 'SB/temp'
client_id = f'python-mqtt-{random.randint(0,1000)}'
username = 'test'
password = 'public'

def init():
    try:
        
        client = connect_mqtt()
        client.loop_start()

        while True:
            line = ser.readline()
            if line:
                string=line.decode('utf-8')  # convert the byte string to a unicode string
                umid=(string[0:5])
                print('umid',umid)
                temp=(string[6:11])
                print('temp:',temp)
                mqtt_publish(client,umid,temp)
    except:
        raise Exception('Um erro ocorreu!')
    finally:
        ser.close()

def connect_mqtt():
    def on_connect(client,userdata, flags,rc):
        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('Failed to connect: return code %d\n',rc)
    #conncetando com client id
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker,port)
    return client
        

def mqtt_publish(client,umid,temp):
    if (len(umid)==5 and len(temp)==5):
        msg_count = 0
        time.sleep(5)
        result_umid = client.publish(topic1,umid)
        result_temp = client.publish(topic2,temp)
        status_umid = result_umid[0]
        status_temp = result_temp[0]
        
        if status_temp == 0:
            print(f'Sent `{umid}` to topic `{topic1}`')
        else:
            print('Failed to send umidity to broker')
        if status_umid == 0:
            print(f'Sent `{temp}` to topic `{topic2}`')
        else:
                print('Failed to send temperature to broker')
    else:
        print('Formato inválido','umid:',umid,'temp:',temp)

if __name__ == '__main__':
    init()
