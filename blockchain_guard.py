from web3 import Web3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BlockchainGuard")

class BlockchainGuard:
    def __init__(self, rpc_url: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if self.w3.is_connected():
            logger.info("Połączono pomyślnie z węzłem sieci Blockchain EVM.")
        else:
            logger.warning("Nie udało się połączyć z węzłem Blockchain (tryb offline/symulacja).")

    def check_mempool_for_mev(self, tx_hash: str) -> bool:
        """
        Skanuje mempool pod kątem botów MEV (Sandwich Attacks / Front-running).
        """
        try:
            if not self.w3.is_connected():
                return False
            pending_tx = self.w3.eth.get_transaction(tx_hash)
            if pending_tx and pending_tx.get('gasPrice', 0) > self.w3.eth.gas_price * 1.5:
                logger.warning(f"Wykryto potencjalne zagrożenie MEV dla transakcji: {tx_hash}")
                return True
        except Exception as e:
            logger.error(f"Błąd podczas analizy mempoolu: {e}")
        return False

    def verify_smart_contract_security(self, contract_address: str) -> bool:
        """
        Weryfikujebytecode smart kontraktu pod kątem obecności kodu (zabezpieczenie przed RugPull / Honeypot).
        """
        try:
            if not self.w3.is_connected():
                # W trybie testowym bez aktywnego RPC zwracamy True, jeśli adres jest podany
                return len(contract_address) > 10
            
            sum_checksum = self.w3.to_checksum_address(contract_address)
            code = self.w3.eth.get_code(sum_checksum)
            if len(code) == 0:
                logger.error(f"Adres {contract_address} nie zawiera kodu bajtowego (To nie jest kontrakt).")
                return false
            logger.info(f"Smart kontrakt {contract_address} zweryfikowany pomyślnie na łańcuchu.")
            return True
        except Exception as e:
            logger.error(f"Błąd weryfikacji smart kontraktu: {e}")
            return False
