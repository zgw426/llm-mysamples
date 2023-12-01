import boto3

def search_kendra(index_id, query):
    kendra = boto3.client('kendra')

    response = kendra.retrieve(
        QueryText=query,
        IndexId=index_id,
        AttributeFilter={
            "EqualsTo": {
                "Key": "_language_code",
                "Value": {"StringValue": "ja"},
            },
        },
    )
    
    return response

# KendraのインデックスIDと検索クエリを指定
## index_idの確認コマンド
## $ aws kendra list-indices --query 'IndexConfigurationSummaryItems[].{ID:Id, Name:Name}' --output table

index_id = 'YOUR_INDEX_ID'  # KendraのインデックスID
query = 'おじいさんの杖'

response = search_kendra(index_id, query)

print("Query results:")
print(response)
print("----")
for item in response['ResultItems']:
    #print(item['DocumentExcerpt']['Text'])
    documentid = item['DocumentId']
    print(f"documentid = ${documentid}")
    print(item['DocumentTitle'])
    print(item['Content'])
    #print(item['DocumentUrl'])
    #print(item['DocumentAttributes'])
    print("===")
