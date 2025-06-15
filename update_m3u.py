import asyncio
import json
import logging
import websockets
from lib.config import settings
from lib.utils import parse_memo  # à adapter selon ton projet
from lib.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

SERVER_ADDRESS = settings.XRP_SERVER_WALLET_ADDR
XRP_WS_URI = settings.XRP_TESTNET_ADDR_WS
IPFS_GATEWAY_URL = settings.IPFS_GATEWAY_URL

logger.info(SERVER_ADDRESS)
logger.info(XRP_WS_URI)
logger.info(IPFS_GATEWAY_URL)


ipfs_gateway_root = IPFS_GATEWAY_URL.rstrip('/') + "/ipfs/"
wisdoms_file_path = "/opt/eaim/radio/wisdoms_ipfs.m3u"

logger.info(f"IPFS Gateway Root: {ipfs_gateway_root}")

async def xrp_wisdom_listener():
    if not SERVER_ADDRESS or not XRP_WS_URI:
        logger.error("❌ SERVER_ADDRESS ou XRP_WS_URI missing in .env")
        return

    try:
        async with websockets.connect(XRP_WS_URI) as websocket:
            subscribe_message = {
                "id": 1,
                "command": "subscribe",
                "accounts": [SERVER_ADDRESS]
            }
            await websocket.send(json.dumps(subscribe_message))
            logger.info(f"🛜 Listening to xrp transactions from {SERVER_ADDRESS}")

            while True:
                message = await websocket.recv()
                data = json.loads(message)

                if data.get("type") == "transaction":
                    tx_hash = data.get("transaction", {}).get("hash")
                    logger.info(f"✅ Transaction detected: {tx_hash[:21]}[...]")

                    parsed_memos = parse_memo(data["transaction"]["Memos"])
                    logger.info(f"📝 Parsed memo: {parsed_memos}")

                    # Lire les lignes déjà existantes dans le fichier
                    try:
                        with open(wisdoms_file_path, "r") as f:
                            existing_cids = set(line.strip() for line in f)
                    except FileNotFoundError:
                        existing_cids = set()

                    new_cids = []

                    for i in range(3):
                        key = f"wisdom_{i}_hash"
                        if parsed_memos.get(key):
                            hash_value = parsed_memos[key]
                            ipfs_cid = f"{ipfs_gateway_root}{hash_value}"
                            if ipfs_cid not in existing_cids:
                                logger.info(f"*** NEW WISDOM {i} IPFS_CID: {ipfs_cid} ***")
                                new_cids.append(ipfs_cid)
                            else:
                                logger.info(f"⏭️ WISDOM {i} already in file: {ipfs_cid}")

                    if new_cids:
                        with open(wisdoms_file_path, "a") as f:
                            for cid in new_cids:
                                f.write(f"{cid}\n")

    except Exception as e:
        logger.error(f"❌ Error in XRP Listener : {e}")

async def main():
    await xrp_wisdom_listener()

if __name__ == "__main__":
    asyncio.run(main())

