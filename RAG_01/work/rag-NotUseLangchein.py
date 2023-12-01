# Bedrock + Kendra を組み合わせる

import boto3
import json
import datetime

query = 'おばあさんの杖'  # クエリ
index_id = 'YOUR_INDEX_ID'  # KendraのインデックスID
modelId = "anthropic.claude-v2"  # BedrockのModel
region_name = 'us-east-1'  # リージョンの指定

# Kendraクライアントを作成
kendra = boto3.client('kendra', region_name=region_name)

# Boto3 セッションの作成
session = boto3.Session()

# Bedrock クライアントの作成
bedrock_client = session.client(service_name='bedrock')
bedrock_runtime_client = session.client(service_name='bedrock-runtime')

def search_kendra(indexId, query):
    kendra = boto3.client('kendra')

    response = kendra.retrieve(
        QueryText=query,
        IndexId=indexId,
        AttributeFilter={
            "EqualsTo": {
                "Key": "_language_code",
                "Value": {"StringValue": "ja"},
            },
        },
    )
    
    return response

def generate_response(modelId, documents):
    # モデルの同期的呼び出し（Anthropic Claude-v2 の場合）
    prompt = f"Human:『${documents}』の『から』までの内容を100文字程度に要約して\nAssistant:"

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 300,
        "temperature": 0.1,
        "top_k": 1,
        "stop_sequences": ["\n\nHuman"]
    })
    
    accept = "application/json"
    content_type = "application/json"
    
    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=modelId,
        accept=accept,
        contentType=content_type
    )
    
    response_body = json.loads(response.get('body').read())

    return response_body


def log(message):
    # 現在の日時を取得
    now = datetime.datetime.now()
    # メッセージと日時を表示
    print(f'{now}: {message}')


def rag(indexId, modelId, query):
    log(f"query = {query}")
    log(f"--- Kendra Start---")
    documents = search_kendra(indexId, query)  # Kendraの処理
    log(f"--- Kendra End---")
    log(f"Kendra Result : {documents}\n")
    targetString = documents['ResultItems'][0]['Content']  # Kendraからの応答結果から一部抜き取る
    log(f"--- Bedrock Start---")
    response = generate_response(modelId, targetString)  # Kendra応答結果(抜粋版)をBedrockで処理する
    log(f"--- Bedrock End---")
    log(f"Bedrock Result : {response}\n")

    return response

response = rag(indexId, modelId, query)
print(response)
