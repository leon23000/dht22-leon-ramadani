# 4. Harjoitus: DHT22 ja MQTT
import network
import time
import dht
import machine

from umqtt.simple import MQTTClient
from config import SSID, PASSWORD, OPISKELIJATUNNUS

# MQTT-broker ja aiheet
BROKER = "iot.research.hamk.fi"

TOPIC_LAMPOTILA = ("HAMK/Fo/DHT22/" + OPISKELIJATUNNUS + "/lampotila").encode()
TOPIC_KOSTEUS = ("HAMK/Fo/DHT22/" + OPISKELIJATUNNUS + "/kosteus").encode()

# Otetaan DHT22-anturi käyttöön
sensor = dht.DHT22(machine.Pin(21))

# Yhdistetään hotspot-verkkoon
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Yhdistetään verkkoon...")

while not wlan.isconnected():
    time.sleep(1)

print("Yhdistetty verkkoon!")
print("IP-osoite:", wlan.ifconfig()[0])

# Luodaan MQTT-asiakas
client = MQTTClient(
    ("dht22-" + OPISKELIJATUNNUS).encode(),
    BROKER,
    keepalive=60
)

# Edelliset mittaustulokset
edellinenLampotila = ""
edellinenKosteus = ""

# Mitataan 10 sekunnin välein
while True:
    sensor.measure()
    lampotila = sensor.temperature()
    kosteus = sensor.humidity()
    print("-------------------------")
    print("Lämpötila:", lampotila, "°C")
    print("Kosteus:", kosteus, "%")

    # Tarkistetaan lämpötilan muutos
    if lampotila != edellinenLampotila:
        client.connect()
        client.publish(TOPIC_LAMPOTILA, str(lampotila).encode())
        client.disconnect()

        print("MQTT: Lämpötila lähetetty")
        edellinenLampotila = lampotila
    else:
        print("MQTT: Lämpötilaa ei lähetetty")

    # Tarkistetaan kosteuden muutos
    if kosteus != edellinenKosteus:
        client.connect()
        client.publish(TOPIC_KOSTEUS, str(kosteus).encode())
        client.disconnect()

        print("MQTT: Kosteus lähetetty")
        edellinenKosteus = kosteus
    else:
        print("MQTT: Kosteutta ei lähetetty")

    # Odotetaan 10 sekuntia ennen seuraavaa mittausta
    time.sleep(10)