#!/usr/bin/env python3
"""Demo chat Azure OpenAI dengan autentikasi API key.

Pola ini mengikuti dokumentasi resmi Microsoft dan sampel publik Azure-Samples:
- URL: {endpoint}/openai/deployments/{deployment}/chat/completions?api-version={version}
- Auth: header `api-key` berisi key mentah, tanpa prefix Bearer.
- Key dan endpoint TIDAK ditulis di repo; semuanya dibaca dari environment.

Sumber pola:
- Azure-Samples/openai-chat-app-quickstart (chat app Python)
- Azure-Samples/app-service-rag-openai-ai-search-python
- Azure-Samples/function-python-ai-langchain
- learn.microsoft.com (Azure OpenAI + API Management auth docs)

Cara pakai:
    cp .env.example .env   # lalu isi .env dengan data resource kamu
    python3 chat.py "Halo, jelaskan apa itu compounding dalam satu kalimat"
    python3 chat.py --list-models   # cek key tanpa memanggil model (gratis)

Biaya: setiap chat completion dibayar per token dari langganan Azure kamu.
Tidak ada free tier untuk Azure OpenAI.
"""
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_API_VERSION = "2024-10-21"


def load_config():
    """Baca konfigurasi dari environment. Gagal jelas bila ada yang kosong."""
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", DEFAULT_API_VERSION)
    missing = [
        name
        for name, value in [
            ("AZURE_OPENAI_ENDPOINT", endpoint),
            ("AZURE_OPENAI_API_KEY", api_key),
            ("AZURE_OPENAI_DEPLOYMENT", deployment),
        ]
        if not value
    ]
    if missing:
        print("Konfigurasi kurang: " + ", ".join(missing), file=sys.stderr)
        print("Isi dari .env (lihat .env.example) atau export manual.", file=sys.stderr)
        sys.exit(2)
    return endpoint, api_key, deployment, api_version


def call_azure(path, api_key, method="GET", payload=None):
    """Satu panggilan REST ke Azure OpenAI dengan header api-key."""
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(path, data=data, method=method)
    request.add_header("Content-Type", "application/json")
    request.add_header("api-key", api_key)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"raw": raw}


def list_models(endpoint, api_key, api_version):
    """Daftar deployment di resource ini. Tidak memanggil model, jadi gratis."""
    status, body = call_azure(
        f"{endpoint}/openai/deployments?api-version={api_version}", api_key
    )
    if status != 200:
        print(f"Gagal ({status}): {json.dumps(body, indent=2)}", file=sys.stderr)
        return 1
    for item in body.get("data", []):
        print(f"- {item.get('id')}  (model: {item.get('model')}, status: {item.get('status')})")
    return 0


def chat(endpoint, api_key, deployment, api_version, prompt, system=None):
    """Kirim satu prompt ke deployment dan cetak jawabannya."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    status, body = call_azure(
        f"{endpoint}/openai/deployments/{deployment}/chat/completions"
        f"?api-version={api_version}",
        api_key,
        method="POST",
        payload={"messages": messages, "temperature": 0.7, "max_tokens": 800},
    )
    if status != 200:
        print(f"Gagal ({status}): {json.dumps(body, indent=2)}", file=sys.stderr)
        return 1
    choice = body["choices"][0]["message"]["content"]
    usage = body.get("usage", {})
    print(choice)
    print()
    print(
        f"[token: prompt {usage.get('prompt_tokens')}, "
        f"jawaban {usage.get('completion_tokens')}, "
        f"total {usage.get('total_tokens')}]"
    )
    return 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    endpoint, api_key, deployment, api_version = load_config()
    if "--list-models" in flags:
        return list_models(endpoint, api_key, api_version)
    if not args:
        print('Pakai: python3 chat.py "pesan kamu"  atau  python3 chat.py --list-models',
              file=sys.stderr)
        return 2
    system = None
    if "--system" in flags:
        idx = sys.argv.index("--system")
        system = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
    return chat(endpoint, api_key, deployment, api_version, " ".join(args), system)


if __name__ == "__main__":
    sys.exit(main())
