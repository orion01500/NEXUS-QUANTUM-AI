import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RPC_URL_EVM = os.getenv("RPC_URL_EVM", "https://eth-mainnet.g.alchemy.com/v2/YOUR-API-KEY")
    RPC_URL_SOLANA = os.getenv("RPC_URL_SOLANA", "https://api.mainnet-beta.solana.com")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "your_private_key_here")
    RISK_MAX_DRAWDOWN = float(os.getenv("RISK_MAX_DRAWDOWN", "0.05"))

settings = Settings()
