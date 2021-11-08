CONF_VPIONEER = {
    "fullnode": "https://vpioneer.infragrid.v.network",
    "event": "https://vpioneer.infragrid.v.network"
}

# Maintained by the official team
CONF_VTEST = {
    "fullnode": "https://vtest.infragrid.v.network",
    "event": "https://vtest.infragrid.v.network",
}

ALL = {
    "vpioneer": CONF_VPIONEER,
    "vtest": CONF_VTEST,
}


def conf_for_name(name: str) -> dict:
    return ALL.get(name, None)


DEFAULT_TIMEOUT = 10.0
DEFAULT_API_KEYS = [
    'f92221d5-7056-4366-b96f-65d3662ec2d9',
    '1e0a625f-cfa5-43ee-ba41-a09db1aae55f',
    'f399168e-2259-481c-90fc-6b3d984c5463',
    'da63253b-aa9c-46e7-a4e8-22d259a8026d',
    '88c10958-af7b-4d5a-8eef-6e84bf5fb809',
    '169bb4b3-cbe8-449a-984e-80e9adacac55',
]
