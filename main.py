import time
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_sentiment import AISentimentEngine
from blockchain_guard import BlockchainGuard
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NexusQuantumAI")

app = FastAPI(title="Nexus Quantum AI & Blockchain Core", version="2.0.0")

sentiment_engine = AISentimentEngine()
blockchain_guard = BlockchainGuard(settings.RPC_URL_EVM)

class TradeRequest(BaseModel):
    asset: str
    amount: float
    contract_address: str = None
    action: str  # 'BUY' lub 'SELL'

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "system": "Nexus Quantum AI Trading Engine",
        "modules": ["AI Sentiment LLM", "Blockchain Mempool Guard", "Smart Contract Auditor"]
    }

@app.post("/api/v1/execute-trade")
def execute_trade(trade: TradeRequest):
    logger.info(f"Otrzymano żądanie handlowe: {trade.action} | Aktywo: {trade.asset} | Ilość: {trade.amount}")

    # 1. Warstwa Blockchain: Weryfikacja inteligentnego kontraktu (dla tokenów DeFi / Altcoinów)
    if trade.contract_address:
        is_safe = blockchain_guard.verify_smart_contract_security(trade.contract_address)
        if not is_safe:
            raise HTTPException(status_code=400, detail="Transakcja odrzucona: Smart kontrakt nie przeszła weryfikacji bezpieczeństwa (Ryzyko RugPull).")

    # 2. Warstwa AI: Analiza sentymentu rynkowego
    sentiment_score = sentiment_engine.analyze_market_sentiment(trade.asset)
    
    # Automatyczny regulator AI
    if trade.action == "BUY" and sentiment_score < -0.4:
        logger.warning("Transakcja zakupu wstrzymana przez AI: Sentyment rynkowy wskazuje na silną panikę.")
        return {
            "status": "REJECTED_BY_AI",
            "reason": "Skrajnie negatywny sentyment rynkowy (Bearish Panic)",
            "ai_sentiment_score": sentiment_score
        }

    # 3. Symulacja realizacji zlecenia
    logger.info(f"Transakcja pomyślnie zrealizowana dla {trade.asset}. Wynik analizy AI: {sentiment_score}")
    return {
        "status": "SUCCESS",
        "asset": trade.asset,
        "amount": trade.amount,
        "action": trade.action,
        "ai_sentiment_score": sentiment_score,
        "blockchain_verified": True if trade.contract_address else False,
        "execution_timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
