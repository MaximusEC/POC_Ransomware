print("""


 __  __            _                     _____ ____ 
|  \/  | __ ___  _(_)_ __ ___  _   _ ___| ____/ ___|
| |\/| |/ _` \ \/ / | '_ ` _ \| | | / __|  _|| |    
| |  | | (_| |>  <| | | | | | | |_| \__ \ |__| |___ 
|_|  |_|\__,_/_/\_\_|_| |_| |_|\__,_|___/_____\____|

\n
\n

Author: MAXIMUSEC
Description:
    Restores files modified by the SAFE ransomware simulator.
    Fully reversible pseudo-decryption.
""")

import os

# Selección automática según el sistema operativo
if os.name == "nt":
    TARGET = r"C:\RANSOM_SIM"
else:
    TARGET = os.path.expanduser("/home/maximus/POC_Ransomware")

LOCKED_EXT = ".locked"
KEY1 = 0x5A
KEY2 = 0xA7
BLOCK_SIZE = 64


def rotate_right(byte, amount):
    """Rotación inversa para revertir la transformación simulada."""
    return ((byte >> amount) | (byte << (8 - amount))) & 0xFF


def pseudo_decrypt_block(block):
    """Proceso inverso exacto al pseudo-encrypt."""
    out = bytearray()

    # 1. Deshacer rotación
    block = bytearray(rotate_right(b, 3) for b in block)

    # 2. Deshacer XOR doble
    for b in block:
        x = b ^ KEY2
        x ^= KEY1
        out.append(x)

    # 3. Deshacer permutación
    return bytes(out[::-1])


def decrypt_sim(path):
    with open(path, "rb") as f:
        data = f.read()

    decrypted = bytearray()

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        decrypted.extend(pseudo_decrypt_block(block))

    with open(path, "wb") as f:
        f.write(decrypted)


def main():
    print("[+] Restoring files...")

    for filename in os.listdir(TARGET):
        if filename.endswith(LOCKED_EXT):
            locked = os.path.join(TARGET, filename)
            orig = os.path.join(TARGET, filename.replace(LOCKED_EXT, ""))

            decrypt_sim(locked)
            os.rename(locked, orig)

            print(f"[+] Restored: {orig}")

    print("[✓] All files restored safely.")


if __name__ == "__main__":
    main()
