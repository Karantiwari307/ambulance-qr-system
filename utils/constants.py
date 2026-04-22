# Mapping between full keys and short keys to optimize QR Code payload size
# The smaller the payload, the easier it is for cameras to scan the QR code.

KEY_MAPPING = {
    "Name": "n",
    "Number": "num",
    "Type": "t",
    "Cost": "c"
}

# Reverse mapping for decoding
REVERSE_KEY_MAPPING = {v: k for k, v in KEY_MAPPING.items()}
