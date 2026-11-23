from pathlib import Path
import hashlib

rom = Path("rom.n64")
data = rom.read_bytes()

if len(data) % 4 != 0:
    raise ValueError("Ungültige ROM-Größe")

if data[:4] != bytes.fromhex("40123780"):
    raise ValueError("Datei ist keine gültige .n64-ROM")

converted = bytearray()

for i in range(0, len(data), 4):
    converted.extend(data[i:i+4][::-1])

output = Path("rom.z64")
output.write_bytes(converted)

# Hashes der konvertierten ROM berechnen
sha256 = hashlib.sha256(converted).hexdigest()
md5 = hashlib.md5(converted).hexdigest()
sha1 = hashlib.sha1(converted).hexdigest()

print("Konvertierung abgeschlossen!")
print(f"Datei:   {output}")
print(f"Größe:   {len(converted):,} Bytes")
print(f"MD5:     {md5}")
print(f"SHA-1:   {sha1}")
print(f"SHA-256: {sha256}")