from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from solders.transaction import Transaction, VersionedTransaction
from solders.system_program import ID as SYSTEM_PROGRAM_ID
from solders.message import Message, MessageV0
import base64
import hashlib
import time, json
from pathlib import Path
import struct


# === Setup ===
# client = Client("https://solana-devnet.g.alchemy.com/v2/yFvVrsfjsZPRaU9X2Du0T")
client = Client("https://api.devnet.solana.com")
program_id = Pubkey.from_string("DrhtoDhPFqsZZFGdyFQxoSYmiAYx8hWxM8DMXvM3R278")

keypair_path = Path("/Users/chenxu/.config/solana/id.json")

with open(keypair_path, 'r') as f:
    secret_key_json = json.load(f)

secret_key_bytes = bytes(secret_key_json)
payer = Keypair.from_bytes(secret_key_bytes)


seed = b'message'
message_pda, _ = Pubkey.find_program_address([seed], program_id)


content = 'Hello from Python!'

discriminator = hashlib.sha256(b'global:create_message').digest()[:8]
content_byptes = content.encode('utf-8')
encoded_data = discriminator + struct.pack('<I', len(content_byptes)) + content_byptes


# === Build Instruction ===
message_account = Keypair()

ix = Instruction(
    program_id=program_id,
    data=encoded_data,
    accounts=[
        AccountMeta(pubkey=message_account.pubkey(), is_signer=True, is_writable=True),
        AccountMeta(pubkey=payer.pubkey(), is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYSTEM_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
)


# === Send Transaction ===
latest_blockhash = client.get_latest_blockhash().value.blockhash

msg = MessageV0.try_compile(
    payer=payer.pubkey(),
    instructions=[ix],
    address_lookup_table_accounts=[],
    recent_blockhash=latest_blockhash,
)

tx = VersionedTransaction(msg, [payer, message_account])

# msg = Message.new_with_blockhash([ix], payer.pubkey(), latest_blockhash)
# tx = Transaction([payer], msg, latest_blockhash)

resp = client.send_transaction(tx)
print(f'Transaction signature: {resp.value}')
time.sleep(30)


from solana.rpc.api import Client
import base64, struct
from solders.pubkey import Pubkey

client = Client("https://api.devnet.solana.com")

message_account_pubkey = message_account.pubkey()

# Fetch raw account data
account_info = client.get_account_info(message_account_pubkey)
# print(account_info)
data: bytes = account_info.value.data


author = Pubkey.from_bytes(data[8:40])
timestamp = struct.unpack('<q', data[40:48])[0]
content_len = struct.unpack('<I', data[48:52])[0]
content = data[52:52 + content_len].decode('utf-8')

print("📦 Decoded Message Account:")
print("Author:", str(author))
print("Timestamp:", timestamp)
print("Content:", content)


import hashlib
import struct
from solders.instruction import Instruction, AccountMeta

# Define new content
new_content = "Updated from Python!"

# Anchor discriminator for update_message
discriminator = hashlib.sha256(b"global:update_message").digest()[:8]

# Encode as Anchor-style: discriminator + <u32 length> + UTF-8 bytes
new_content_bytes = new_content.encode("utf-8")
encoded_data = discriminator + struct.pack("<I", len(new_content_bytes)) + new_content_bytes

# Reuse message_account from previous test
ix = Instruction(
    program_id=program_id,
    data=encoded_data,
    accounts=[
        AccountMeta(pubkey=message_account.pubkey(), is_signer=False, is_writable=True),
        AccountMeta(pubkey=payer.pubkey(), is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYSTEM_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
)



from solders.transaction import VersionedTransaction
from solders.message import MessageV0

latest_blockhash = client.get_latest_blockhash().value.blockhash

msg = MessageV0.try_compile(
    payer=payer.pubkey(),
    instructions=[ix],
    address_lookup_table_accounts=[],
    recent_blockhash=latest_blockhash,
)

tx = VersionedTransaction(msg, [payer])

resp = client.send_transaction(tx)
print(f"✅ update_message tx: {resp.value}")
time.sleep(30)

account_info = client.get_account_info(message_account.pubkey())
data: bytes = account_info.value.data

author = Pubkey.from_bytes(data[8:40])
timestamp = struct.unpack("<q", data[40:48])[0]
content_len = struct.unpack("<I", data[48:52])[0]
content = data[52:52 + content_len].decode("utf-8")

print("📦 Decoded Updated Message:")
print("Author:", str(author))
print("Timestamp:", timestamp)
print("Content:", content)

assert content == new_content, "update_message failed!"
