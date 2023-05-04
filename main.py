import json
from pathlib import Path
from multiversx_sdk_wallet import UserPEM, UserSigner
from multiversx_sdk_network_providers import ProxyNetworkProvider
from multiversx_sdk_core import Transaction, Address, TokenPayment, AccountNonceHolder

# Replace these values with your own
pem_file_path = "wallet.pem"

def main():
    # Read wallet from .pem file
    pem = UserSigner.from_pem_file(Path(pem_file_path))

    # Set the MultiversX Mainnet Network
    # Get the Chain ID
    provider = ProxyNetworkProvider("https://gateway.multiversx.com")
    config = provider.get_network_config();
    print("Chain ID", config.chain_id);

    # Get the Nonce
    account = Address.from_bech32("erd sender address")
    account_on_network = provider.get_account(account)
    new_nonce = account_on_network.nonce

    # Create Transaction
    tx = Transaction(
    nonce=new_nonce,
    sender=Address.from_bech32("erd sender address"),
    receiver=Address.from_bech32("erd recipient address"),
    value=TokenPayment.egld_from_amount("0"),
    gas_limit=50000,
    gas_price=1000000000,
    chain_id=config.chain_id,
    version=1
    )

    # Sign and Send Transaction
    tx.signature = pem.sign(tx)
    hash = provider.send_transaction(tx)
    print("Transaction hash:", hash)

if __name__ == "__main__":
    main()
