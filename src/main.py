#!/usr/bin/env python3
import json
import base64
import paho.mqtt.client as mqtt
from node_simulation import pack_lorawan_1_0_3_ca_abp
from gateway_simulation import pack_chirpstack_gw_protobuf


# Payload as raw hex string
hex_payload = "01020304"
hex_context = "01020304"

# Read configuration
with open("conf.json") as f:
    config = json.load(f)

gateway_id = config["gateway"]["id"]
ip_addr = config["gateway"]["ip_addr"]

dev_addr = config["dev"]["addr"]
app_s_key = config["dev"]["app_s_key"]
nwk_s_key = config["dev"]["nwk_s_key"]
tx_freq = config["dev"]["tx_freq"]
tx_bw = config["dev"]["tx_bw"]
tx_sf = config["dev"]["tx_sf"]

mqtt_host = config["mqtt"]["host"]
mqtt_port = config["mqtt"]["port"]
mqtt_username = config["mqtt"]["username"]
mqtt_password = config["mqtt"]["password"]
mqtt_topic = config["mqtt"]["topic_up"]

# Step 1: Create LoRaWAN PHYPayload (hex)
phy_payload_bytes = pack_lorawan_1_0_3_ca_abp(
    dev_addr=dev_addr, app_s_key=app_s_key, nwk_s_key=nwk_s_key, payload=hex_payload
)
phy_payload_hex = phy_payload_bytes.hex()

# Step 2: Pack to ChirpStack UplinkFrame Protobuf
protobuf_bytes = pack_chirpstack_gw_protobuf(
    phy_payload_hex=phy_payload_hex,
    frequency=tx_freq,
    bandwidth=tx_bw,
    spreading_factor=tx_sf,
    gateway_id_hex=gateway_id,
    rssi=-52,
    snr=13.75,
    context_hex=hex_context,  # Example context
)


# Step 3: Publish to MQTT
def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code {rc}")
    client.publish(mqtt_topic, protobuf_bytes)
    print(f"[MQTT] Published to {mqtt_topic}: {protobuf_bytes.hex()}")
    client.disconnect()


client = mqtt.Client()
if mqtt_username or mqtt_password:
    client.username_pw_set(mqtt_username, mqtt_password)

client.on_connect = on_connect
client.connect(mqtt_host, mqtt_port, 60)
client.loop_forever()
