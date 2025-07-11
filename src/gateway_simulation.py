import gw.gw_pb2 as gw_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
import base64
import argparse


def pack_chirpstack_gw_protobuf(
    phy_payload_hex: str,
    frequency: int,
    bandwidth: int,
    spreading_factor: int,
    gateway_id_hex: str,
    rssi: int,
    snr: float,
    context_hex: str
) -> bytes:
    """
    Pack the input data into a ChirpStack gw_pb2.UplinkFrame protobuf message.

    Args:
        phy_payload_hex (str): Hex string of the LoRaWAN phyPayload.
        frequency (int): Frequency in Hz.
        bandwidth (int): LoRa bandwidth in Hz.
        spreading_factor (int): LoRa spreading factor.
        gateway_id_hex (str): Gateway ID as a hex string.
        rssi (int): RSSI value.
        snr (float): SNR value.
        context_hex (str): Context as hex string.

    Returns:
        bytes: Serialized protobuf message.
    """
    frame = gw_pb2.UplinkFrame()
    frame.phy_payload = bytes.fromhex(phy_payload_hex)

    frame.tx_info.frequency = frequency
    frame.tx_info.modulation.lora.bandwidth = bandwidth
    frame.tx_info.modulation.lora.spreading_factor = spreading_factor
    frame.tx_info.modulation.lora.code_rate = gw_pb2.CR_4_5

    rx_info = frame.rx_info
    rx_info.gateway_id = gateway_id_hex
    rx_info.rssi = rssi
    rx_info.snr = snr
    rx_info.context = bytes.fromhex(context_hex)
    rx_info.crc_status = gw_pb2.CRC_OK

    ts = Timestamp()
    ts.FromDatetime(datetime.utcnow())
    rx_info.gw_time.CopyFrom(ts)

    return frame.SerializeToString()


def main():
    parser = argparse.ArgumentParser(description="Pack ChirpStack UplinkFrame as Protobuf")
    parser.add_argument("--phy_payload", required=True, help="LoRaWAN phyPayload (hex string)")
    parser.add_argument("--frequency", type=int, required=True, help="Frequency in Hz")
    parser.add_argument("--bandwidth", type=int, required=True, help="LoRa bandwidth in Hz")
    parser.add_argument("--spreading_factor", type=int, required=True, help="LoRa spreading factor")
    parser.add_argument("--gateway_id", required=True, help="Gateway ID (hex string, 16 chars for 8 bytes)")
    parser.add_argument("--rssi", type=int, required=True, help="RSSI value")
    parser.add_argument("--snr", type=float, required=True, help="SNR value")
    parser.add_argument("--context", required=True, help="Context (hex string)")

    args = parser.parse_args()

    data = pack_chirpstack_gw_protobuf(
        phy_payload_hex=args.phy_payload,
        frequency=args.frequency,
        bandwidth=args.bandwidth,
        spreading_factor=args.spreading_factor,
        gateway_id_hex=args.gateway_id,
        rssi=args.rssi,
        snr=args.snr,
        context_hex=args.context
    )

    print("Protobuf (hex):", data.hex())
    print("Protobuf (base64):", base64.b64encode(data).decode())


if __name__ == "__main__":
    main()
