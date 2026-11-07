# Sumber

Pola kode di repo ini dirakit dari sampel open source publik berikut
(dicari di internet dan di situs Microsoft sendiri) dan ditulis ulang
menjadi satu file mandiri tanpa dependency.

## Repo sampel (github.com/Azure-Samples)

- `Azure-Samples/openai-chat-app-quickstart` — chat app Python (Quart) ke
  Azure OpenAI; pola `chat.completions.create` dan struktur deployment.
  https://github.com/Azure-Samples/openai-chat-app-quickstart
- `Azure-Samples/app-service-rag-openai-ai-search-python` — pola pemanggilan
  chat completion Azure OpenAI + AI Search dari tutorial App Service.
  https://github.com/Azure-Samples/app-service-rag-openai-ai-search-python
- `Azure-Samples/function-python-ai-langchain` — pola deployment-based
  (`AzureChatOpenAI` dengan `deployment_name`) dan template prompt.
  https://github.com/Azure-Samples/function-python-ai-langchain
- `Azure-Samples/deepseek-python` — pola chat/stream via OpenAI SDK ke
  endpoint Azure.
  https://github.com/Azure-Samples/deepseek-python

## Dokumentasi Microsoft (learn.microsoft.com)

- Authenticate and Authorize to LLM APIs (Azure API Management) — Azure
  OpenAI memakai header `api-key`, bukan `Authorization: Bearer`.
- Get started with the Azure OpenAI security building blocks — arsitektur
  chat app + provisioning resource Azure OpenAI.
- Tutorial RAG di App Service dengan Azure OpenAI dan Azure AI Search.

## Catatan

Repo ini BUKAN salinan dari salah satu sampel di atas. Kodenya ditulis
sendiri (stdlib Python saja, tanpa SDK OpenAI) mengikuti pola URL dan
header autentikasi yang didokumentasikan di sumber-sumber tersebut.
