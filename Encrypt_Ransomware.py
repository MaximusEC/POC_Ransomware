print("""
\n
\n


 __  __            _                     _____ ____ 
|  \/  | __ ___  _(_)_ __ ___  _   _ ___| ____/ ___|
| |\/| |/ _` \ \/ / | '_ ` _ \| | | / __|  _|| |    
| |  | | (_| |>  <| | | | | | | |_| \__ \ |__| |___ 
|_|  |_|\__,_/_/\_\_|_| |_| |_|\__,_|___/_____\____|

\n
\n
                                                                                                              
""")



print("""
Author: MAXIMUSEC
Description:
    SAFE & REVERSIBLE RANSOMWARE BEHAVIOR SIMULATOR.
    - Simula "cifrado" de archivos usando pseudo-cripto reversible.
    - Cambia extensiones a .locked
    - Escribe ruido (alta entropía) para activar EDR/SOC
    - Genera una nota falsa de rescate.
    - 100% SEGURO y REVERSIBLE.
""")

import os
import time

# ------------------------------
# CONFIGURACIÓN POR SISTEMA
# ------------------------------

# WINDOWS — descomenta esta línea:
# TARGET = r"C:\RANSOM_SIM"

# LINUX — descomenta esta línea:
#TARGET = os.path.expanduser("/home/maximus/POC_Ransomware") #(Change this with your path)

# Selección automática por sistema:
if os.name == "nt":  # Windows
    TARGET = r"C:\RANSOM_SIM" #Change for your path #
else:  # Linux / macOS
    TARGET = os.path.expanduser("/home/maximus/POC_Ransomware")

EXT = ".dummy"
LOCKED_EXT = ".locked"

# Claves para la pseudo-cripto (REVERIBLE)
KEY1 = 0x5A
KEY2 = 0xA7

# Tamaño de bloque (no criptográfico)
BLOCK_SIZE = 64


def rotate_left(byte, amount):
    """Rotación izquierda de bits — confusión simulada."""
    return ((byte << amount) | (byte >> (8 - amount))) & 0xFF


def pseudo_encrypt_block(block):
    """
    Aplica una pseudo-criptografía en un bloque.
    NO es criptografía real. Es completamente reversible.
    """
    out = bytearray()

    # 1. Permutación (invertir el orden)
    block = block[::-1]

    # 2. XOR doble con claves simples
    for b in block:
        x = b ^ KEY1
        x ^= KEY2
        out.append(x)

    # 3. Rotación de bits (más confusión)
    out = bytearray(rotate_left(b, 3) for b in out)

    return bytes(out)


def encrypt_sim(path):
    """Lee un archivo, aplica pseudo-cripto por bloques y lo sobrescribe."""
    with open(path, "rb") as f:
        data = f.read()

    encrypted = bytearray()

    # Procesamiento por bloques tipo AES (pero falso)
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        encrypted.extend(pseudo_encrypt_block(block))

    with open(path, "wb") as f:
        f.write(encrypted)


def main():
    print("[+] Starting SAFE ransomware behavior simulation...")

    for filename in os.listdir(TARGET):
        if filename.endswith(EXT):
            original = os.path.join(TARGET, filename)
            locked = os.path.join(TARGET, filename + LOCKED_EXT)

            # Crear alta entropía (para EDR)
            with open(original, "ab") as f:
                f.write(os.urandom(2048))

            # Aplicar pseudo cifrado seguro
            encrypt_sim(original)

            # Renombrar archivo (comportamiento típico ransomware)
            os.rename(original, locked)

            print(f"[+] Locked (simulated): {filename}")

            # Pequeña pausa para simular actividad continua
            time.sleep(0.05)

    # Nota falsa de rescate
    with open(os.path.join(TARGET, "README_RECOVERY.txt"), "w") as f:
        f.write("YOUR FILES ARE SAFE.\nTHIS IS ONLY A TRAINING SIMULATION.\n")

    print("[✓] Simulation complete. Files appear locked but are 100% reversible.")
    print("[✓] Your SOC/EDR should detect this behavior.")


if __name__ == "__main__":
    main()
