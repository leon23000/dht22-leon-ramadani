# 4. Harjoitus: DHT22 ja MQTT

## Mitä tekee?

Ohjelma lukee FoCariin kytketyn DHT22-anturin lämpötila- ja kosteusarvot 10 sekunnin välein.

Ohjelma vertaa mittaustuloksia edellisiin mittaustuloksiin ja lähettää MQTT-brokerille viestin vain silloin, kun mittaustulos muuttuu.

Konsoliin tulostetaan lämpötila, kosteus (en tiedä miksi lisää "%"-merkin) ja tieto siitä, lähetettiinkö MQTT-viesti.