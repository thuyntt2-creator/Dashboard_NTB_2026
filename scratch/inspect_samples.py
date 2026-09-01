import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== GAN SAMPLE ===")
print(d['gan']['am'][0])

print("=== ODR SAMPLE ===")
print("AM:", d['odr']['am'][0])
print("TINH:", d['odr']['tinh'][0])

print("=== LTC SAMPLE ===")
print("AM:", d['ltc']['am'][0])
print("TINH:", d['ltc']['tinh'][0])

print("=== OPR TTS SAMPLE ===")
print("AM:", d['opr_tts']['am'][0])
print("TINH:", d['opr_tts']['tinh'][0])

print("=== ROT LC SAMPLE ===")
print("AM:", d['rot_lc']['am'][0])
print("TINH:", d['rot_lc']['tinh'][0])
print("TOP BC:", d['rot_lc']['top_bc'][0])
