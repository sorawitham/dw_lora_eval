# Deaware LoRa Evaluation

A simulation and evaluation toolset for LoRaWAN communications using the ChirpStack protobuf format.


## Project Structure

```base
dw_lora_eval/
├── README.md                 # This documentation
├── requirements.txt          # Python dependencies
└── src/
    ├── conf.json             # Configuration file for simulations
    ├── main.py               # Entry point for running simulations
    ├── gateway_simulation.py # Simulate LoRaWAN gateway uplink
    ├── node_simulation.py    # Pack LoRaWAN node uplink payload
    └── proto/                # ChirpStack protobuf files (compiled & sources)

```

## Overview

This project is designed to simulate LoRaWAN uplink behavior and test integration with ChirpStack via MQTT. It uses the official ChirpStack Protobuf definitions and supports building your own encoded payloads.

### Features

* Generate phyPayload for LoRaWAN 1.0.3 (ABP)
* Simulate gateway uplink via MQTT
* Send Protobuf-formatted UplinkFrame messages
* Fully compatible with ChirpStack's MQTT API

## Usage

### Prerequisite

```bash
python -m venv env
source env/bin/activate
pip install requirements.txt
```

### main.py

Runs an integrated simulation combining node payload packing and gateway uplink sending via MQTT to ChirpStack.

```bash
cd src
PYTHONPATH=./proto python main.py
```

### node_simulation.py

Packs a LoRaWAN 1.0.3 ABP phyPayload.

```bash
cd src
PYTHONPATH=./proto python node_simulation.py \
    --dev_addr "016ef7c5" \
    --app_s_key "385e0c0e430826baea9a50124714709c" \
    --nwk_s_key "8d92a5a7fb510ed6a98faa072bc4a3a0" \
    --payload "01020304"
```

Outputs:
* hex string
* base64 string

### gateway_simulation.py

Packs a gw_pb2.UplinkFrame message for ChirpStack MQTT broker.

```bash
cd src
PYTHONPATH=./proto python gateway_simulation.py \
    --phy_payload "40c5f76e018001000183cd74687fe84d28" \
    --frequency 921400000 \
    --bandwidth 125000 \
    --spreading_factor 7 \
    --gateway_id "04454137388a616a" \
    --rssi -52 \
    --snr 13.75 \
    --context "01020304"
```

Outputs:
* hex string
* base64 string

## Compile Protobufs

ChirpStack uses Protobuf v3. The project includes .proto and pre-generated _pb2.py files, but you can recompile anytime.

### 1. Clone ChirpStack GitHub Repository

```bash
git clone https://github.com/chirpstack/chirpstack.git
```

### 2. Install Required Tools

```bash
sudo apt install protobuf-compiler
```

### 3. Compile All .proto Files

```bash
cd chirpstack/api
protoc -I. --python_out=. $(find . -name "*.proto")
```
