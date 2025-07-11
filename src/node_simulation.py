#!/usr/bin/env python3
import argparse
import base64
import pylorawan


def pack_lorawan_1_0_3_ca_abp(dev_addr, app_s_key, nwk_s_key, payload):
    """
    Pack a LoRaWAN 1.0.3 uplink message for Class A device using ABP activation.

    Parameters:
        dev_addr (str): Device address in hex string format (e.g., '26011BDA').
        app_s_key (str): Application session key as hex string (16 bytes).
        nwk_s_key (str): Network session key as hex string (16 bytes).
        payload (str): FRMPayload as hex string.

    Returns:
        bytes: Raw bytes of the encoded uplink message (PHYPayload).
    """
    dev_addr = int(dev_addr, 16)
    app_s_key = bytes.fromhex(app_s_key)
    nwk_s_key = bytes.fromhex(nwk_s_key)
    frm_payload = bytes.fromhex(payload)

    f_cnt = 1
    f_port = 1
    f_opts = b""
    direction = 0

    mtype = pylorawan.message.MType.UnconfirmedDataUp
    mhdr = pylorawan.message.MHDR(mtype=mtype, major=0)

    encrypted_frm_payload = pylorawan.common.encrypt_frm_payload(
        frm_payload, app_s_key, dev_addr, f_cnt, direction
    )

    f_ctrl = pylorawan.message.FCtrlUplink(
        adr=True, adr_ack_req=False, ack=False, class_b=False, f_opts_len=0
    )
    fhdr = pylorawan.message.FHDRUplink(
        dev_addr=dev_addr, f_ctrl=f_ctrl, f_cnt=f_cnt, f_opts=f_opts
    )

    mac_payload = pylorawan.message.MACPayloadUplink(
        fhdr=fhdr, f_port=f_port, frm_payload=encrypted_frm_payload
    )

    mic = pylorawan.common.generate_mic_mac_payload(mhdr, mac_payload, nwk_s_key)

    phy_payload = pylorawan.message.PHYPayload(mhdr=mhdr, payload=mac_payload, mic=mic)
    raw_bytes_uplink_msg = phy_payload.generate()
    return raw_bytes_uplink_msg


def main():
    parser = argparse.ArgumentParser(description="LoRaWAN 1.0.3 Tool (Class A ABP Uplink)")
    parser.add_argument("--dev_addr", type=str, required=True, help="Device address (hex string)")
    parser.add_argument("--app_s_key", type=str, required=True, help="App session key (hex string)")
    parser.add_argument("--nwk_s_key", type=str, required=True, help="Network session key (hex string)")
    parser.add_argument("--payload", type=str, required=True, help="Payload (hex string)")

    args = parser.parse_args()

    raw_bytes = pack_lorawan_1_0_3_ca_abp(
        args.dev_addr,
        args.app_s_key,
        args.nwk_s_key,
        args.payload
    )
    hex_str = raw_bytes.hex()
    b64_str = base64.b64encode(raw_bytes).decode()
    print("Hex:", hex_str)
    print("Base64:", b64_str)


if __name__ == "__main__":
    main()
