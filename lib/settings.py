import os
from pathlib import Path
from dotenv import load_dotenv 

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    def __init__(self):
        self.XRP_SERVER_WALLET_ADDR = os.getenv("XRP_SERVER_WALLET_ADDR")
        self.XRP_TESTNET_ADDR_WS = os.getenv("XRP_TESTNET_ADDR_WS")
        self.IPFS_API_URL = os.getenv("IPFS_API_URL")
        self.IPFS_GATEWAY_URL = os.getenv("IPFS_GATEWAY_URL")
        self.IPFS_TIMEOUT = os.getenv("IPFS_TIMEOUT")
        self.IPFS_IP = os.getenv("IPFS_IP")
        self.IPFS_PORT = os.getenv("IPFS_PORT")

settings = Settings()
