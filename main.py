import sdm_modbus, configparser
from time import sleep
from influxdb import InfluxDBClient

config = configparser.ConfigParser()
config.read_file(open('./token.config', mode='r'))
host = config.get('config', 'host')
user = config.get('config', 'user')
password = config.get('config', 'password')
dbname = config.get('config', 'dbname')

client = InfluxDBClient(host, 8086, user, password, dbname)

meter = sdm_modbus.SDM120(
    device='/dev/ttyUSB0',
    stopbits=1,
    parity='N',
    baud=9600,
    timeout=2,
    unit=1
    )

def write(data):
    write_data = {}
    write_data['measurement'] = "energy"
    write_data['tags'] = {}
    write_data['fields'] = data
    write_data['tags']['name'] = "SDM120"
    if client.write_points([write_data]):
        return
    else:
        print("Daten konnten nicht gesendet werden.")

if __name__ == '__main__':
    while True:
        data = meter.read_all(sdm_modbus.registerType.INPUT)
        write(data)
        sleep(1)