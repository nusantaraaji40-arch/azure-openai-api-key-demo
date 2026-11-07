# azure-openai-api-key-demo

Demo kecil memanggil Azure OpenAI pakai **API key** — dirakit dari sampel open source
publik Microsoft (Azure-Samples) dan dokumentasi resmi learn.microsoft.com.

Satu file Python, tanpa dependency di luar standard library. Cocok buat ngetes
key + endpoint Azure OpenAI kamu sebelum dipakai di project yang lebih besar.

## Yang dilakukan repo ini

- `chat.py` — kirim satu prompt ke deployment Azure OpenAI dan cetak jawabannya.
- `--list-models` — daftar deployment di resource kamu, tanpa memanggil model
  (jadi tidak makan token).
- Auth memakai header `api-key` berisi key mentah, tanpa prefix `Bearer`,
  ke URL `{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=...`.

## Cara pakai

```bash
cp .env.example .env
# isi .env dengan data resource Azure OpenAI kamu
python3 chat.py --list-models
python3 chat.py "Halo, jelaskan compounding dalam satu kalimat"
```

Isi `.env`:

| Variabel | Contoh | Diambil dari |
|---|---|---|
| `AZURE_OPENAI_ENDPOINT` | `https://namamu.openai.azure.com` | Portal Azure → resource Azure OpenAI → Keys and Endpoint |
| `AZURE_OPENAI_API_KEY` | Key 1 / Key 2 | Portal Azure → resource Azure OpenAI → Keys and Endpoint |
| `AZURE_OPENAI_DEPLOYMENT` | `gpt-4o-mini` | Nama deployment yang kamu buat di AI Foundry |
| `AZURE_OPENAI_API_VERSION` | `2024-10-21` | Opsional, sudah ada default |

## Keamanan

- **Jangan pernah commit file `.env` atau key ke repo.** `.env` sudah masuk
  `.gitignore`. Key hanya dibaca dari environment.
- Key yang bocor di repo publik hampir pasti dicabut atau disalahgunakan.
  Kalau key pernah tampil di chat atau ter-commit, rotasi di portal Azure
  (Keys and Endpoint → Regenerate Key).

## Biaya

Azure OpenAI **berbayar per token, tidak ada free tier**. Setiap `chat.py`
memakai token dari langganan Azure kamu. Cek pemakaian di portal Azure →
Cost Management, dan pakai `--list-models` untuk tes key tanpa biaya token.

## Sumber

Lihat `SOURCES.md` untuk daftar repo dan dokumen publik yang dipakai sebagai
acuan pola kode ini.

## Lisensi

MIT — lihat `LICENSE`.
