import boto3
import json

# Boto3 セッションの作成
session = boto3.Session()

# Bedrock クライアントの作成
bedrock_client = session.client(service_name='bedrock')
bedrock_runtime_client = session.client(service_name='bedrock-runtime')

# モデルの同期的呼び出し（Anthropic Claude-v2 の場合）
prompt = """
Human: コード作成の制限事項とCDKコードの作成規則に準拠し、EFSを作成するコードを書いて下さい。
念押ししますが、作成するのはAmazon EFSをデプロイするコードです。

コード作成の制限事項<restriction></restriction>
CDKコードの作成規則は<rule></rule>

<restriction>
・aws cdk v2 スクリプト
・プログラム言語はTypeScript
・cdkコマンドは東京リージョンの環境で実行
</restriction>


<rule>
## コードの規則
- 原則AWSリソースの種類ごとにクラス(class)を作る
- 複数のAWSリソースを1つのクラスにまとめた方が利点がある場合はまとめてOKとする
- 同じ種類のAWSリソースを作成する場合でも、指定するパラメータが大幅に違うなどあれば別にクラスを作る
- 1度作ったクラスを改変する際に、影響範囲が大きい or 不明 の場合はクラスを分割する
  - 例
    - `./lib/Origin/iam.ts`が既に複数の組合せで使用されているとする
    - `組合せ` `com1`の要件変更により`./lib/Origin/iam.ts`の改変が必要になった
    - `./lib/Origin/iam.ts`改変の影響が不明
    - `./lib/Origin/iam.ts`をコピーし`./lib/Origin/iam-com1.ts`を作成し`./lib/Origin/iam-com1.ts`を改変する
- クラス(class)ごとにxxx.tsを作り`./lib/`配下に格納する
- lib配下はxxx.tsの区分けによってディレクトリを分ける
  - `./lib/Combination/`
    - `組合せ`の`xxx.ts`を格納
  - `./lib/Origin/`
    - AWSリソースを作成する`xxx.ts`を格納
- `./lib/Origin/`配下のxxx.tsファイルの命名規則
    - {AWSリソース名}.ts
        - 例
            - `./lib/Origin/s3.ts`
    - {AWSリソース名}-{中身がわかる文字列}.ts
        - 例
            - `./lib/Origin/s3-setLifeCycle.ts`
            - `./lib/Origin/s3-setCrossRegion.ts`
- `./lib/Origin/xxx.ts`には以下を含める
    - クラス(class)
    - インタフェース(interface): (extends props)
        - クラスに渡す引数
    - インタフェース(interface): (extends set)
        - リソースを作るパラメータ
- クラス(class)について
    - リソースをN個作成できるようにする(※別途説明)
    - 作ったリソースはクロススタック参照できるようにする(`public readonly ・・・`)
    - 作ったリソースは(念のため)CfnOutputでエクスポートする
    - constructorに書くコードはできるだけ少なくする
- インターフェース(set)について
    - インターフェース(set)は、1つのAWSリソースを作成するに必要なパラメータのセットを定義する
    - この定義の各要素(変数)に何を設定するかわかるようにコメントで説明する
- クラス外で作成したリソースへのアクセスについて
    - クラス外で作成したAWSリソースへのアクセスは、原則クロススタック参照を使用する
    - 手動作成のAWSリソースへのアクセスは `formXXX` が使えればそれを使う
        - `formXXX`の例を(*1)にかく
    - 上記のどちらでもアクセスできない場合は、臨機応変に考える(知らん)
- 組合せ
    - リソース作るときにセットで作るリソースがある。
    - そのセットのことを`組合せ`と呼称することにした。
    - 変数の接頭辞には組合せで決めた接頭辞をつける
    - スタック名にも組合せの接頭辞を付ける
    - 他の組合せとの依存関係は最小限にする
- 外だしのデータについて
  - Lambdaのスクリプトやポリシーの設定などを別ファイルにしたい場合がある
  - それら外だしのデータは `./data/{pjName}-{pjEnv}/` ディレクトリ配下に格納とする
    - `./data/`は`./bin/`,`./lib/`と同じ階層
  - 例えば、Lambdaのスクリプトは以下のように格納する
    - `./data/{pjName}-{pjEnv}/Lambda/a01/a01-sample.py`
    - `./data/{pjName}-{pjEnv}/Lambda/a02/a02-sample.py`
- デプロイについて
  - デプロイの最小実行単位は`組合せ`単位とする
  - `組合せ`ごとに複数のスタックが含まれることがあるため`make`コマンドを使う
  - 以下のサンプルコードの場合、組合せごとのデプロイは以下になる
    - `組合せ` `com1`
      - make deploy-com01
    - `組合せ` `com2`
      - make deploy-com02
- リソースをN個作成できるようにする(※別途説明)について
  - `クラス(class)について`で記載したN個作成についてここで説明する
  - AWSリソースを作成するクラス(class)に渡す値はJSON形式とする
  - JSON形式のデータは、1つのAWSリソースを作成するパラメータセットごとにまとめる
  - JSON形式のデータには、1以上(N個)のAWSリソースを作成するようパラメータセットを書けるようにする
    - `[{パラメータセット１}, {パラメータセット２}, {パラメータセット３}・・・]`
  - クラス(class)では、パラメータセットごとにAWSリソースを作成する処理を行う
  - パラメータセットは1以上(N個)あるのでリソース作成処理はループ処理が必要
- `./bin/xxx.ts`について
  - このファイルにはできるだけ情報を書かない
    - コード開発のときにコンフリクト起きやすいから
  - 命名規則はこれ
    - `./bin/root-{pjName}-{pjEnv}.ts`
      - `{pjName}`,`{pjEnv}`は無変換
- 変数`{pjName}`,`{pjEnv}`について
  - 値を変更する場合は、以下ファイルを更新する
    - `cdk.json`の `"app"` 要素のパス情報
    - `Makefile`の変数`JSON_FILE`のパス情報
  - 設定する文字列は英小文字,数字のみとする
    - `-` (ハイフン) のような記号は使わない（連結文字列と混同するため）
    - リソースなどの命名に使用する際は、"パスカルケース変換/キャメルケース変換/無変換" を選択する
      - ファイルパスは無変換、スタック名はパスカルケース変換 など

## ディレクトリ構成

サンプルコード `./02` の主なディレクトリ構成

```console
│ Makefile ※makeコマンド用ファイル
├─bin
│      root-pj01-stg.ts ※pjName,pjEnvごとにxxx.ts作成
│      root-pj05-dev.ts
├─data
│  ├─pj01-stg ※パラメータは {pjName}-{pjEnv} ディレクトリごとに分ける
│  │  │  rootSet.json
│  │  ├─Combination ※`組合せ`のパラメータファイル格納ディレクトリ
│  │  │      Cmb00Set.json
│  │  │      Cmb01Set.json
│  │  │      Cmb02Set.json
│  │  └─lambda
│  │      ├─a03
│  │      │      a01-sample.py
│  │      └─a04
│  │             a02-sample.py
│  └─pj05-dev
│      │  rootSet.json
│      ├─Combination
│      │      Cmb00Set.json
│      │      Cmb01Set.json
│      │      Cmb02Set.json
│      └─lambda
│          ├─a01
│          │      a01-sample.py
│          └─a02
│                 a02-sample.py
├─lib
   ├─Combination ※`組合せ`の xxxx.ts ディレクトリ
   │      Cmb00Stack.ts
   │      Cmb01Stack.ts
   │      Cmb02Stack.ts
   └─Origin ※AWSリソース作成の xxxx.ts ディレクトリ
           Common.ts
           Ec2.ts
           IamRole.ts
           Lambda.ts
           Vpc.ts
```

## コードの規則案を元にちょっと作ってみる

- IAMロール,Lambda,EC2をCDKで作るコードの場合、どのようになるかやってみる。
- 組合せはLambdaとEC2で分けてみる
- Lambda,EC2で必要なIAMロールはそれぞれの組み合せ内で作成することにする


命名規則と実際の名前

|リソース|クラス|関数|インタフェース(props)|インタフェース(set)|
|---|---|---|-----|------|
|文字列の規則→|PascalCase|camelCase|PascalCase|PascalCase|
|命名規則→|XxxStack|createXxxFunc|XxxProps|XxxSet|
|VPC|Vpc2Stack|createVpcFunc|VpcProps|VpcSet|
|IAM Role|IamRoleStack|createIamRolesFunc|IamRoleProps|IamRoleSet|
|Lambda|LambdaStack|createLambdaFunc|LambdaProps|LambdaSet|
|EC2|Ec2Stack|createEc2Func|Ec2Props|Ec2Set|


組合せには接頭辞を用意する

|組合せ名|接頭辞|関数名|備考|
|----|---|----|----|
|Combination00|cmb00|Combination00Func|VPCを作る|
|Combination01|cmb01|Combination01Func|LambdaとそのLambdaに付与するIAMロールを作る|
|Combination02|cmb02|Combination02Func|EC2とそのEC2に付与するIAMロールを作る|

スタック名などに組合せの接頭辞を付与し、デプロイしたときにどの組合せのものか分かりやすくする

|接頭辞|リソース|スタック|変数(props)|変数(set)|依存元|備考|
|---|---|---|---|---|---|---|
|cmb00|VPC|{PjName}{PjEnv}Cmb00VpcStack|cmb00VpcProps|cmb00VpcSet|ー|VPC作成|
|cmb01|IAM Role|{PjName}{PjEnv}Cmb01IamRoleStack|cmb01IamRoleProps|cmb01IamRoleSet|ー|Lambda用のIAMロール|
|cmb01|Lambda|{PjName}{PjEnv}Cmb01LambdaStack|cmb01LambdaProps|cmb01LambdaSet|Cmb01IamRoleStack||
|cmb02|IAM Role|{PjName}{PjEnv}Cmb02IamRoleStack|cmb02IamRoleProps|cmb02IamRoleSet|ー|EC2用のIAMロール|
|cmb02|EC2|{PjName}{PjEnv}Cmb02Ec2Stack|cmb02Ec2Props|cmb02Ec2Set|Cmb02IamRoleStack||

 ※ スタック名の`{PjName}`,`{PjEnv}`はパスカルケースに変換
</rule>

\nAssistant:
"""

body = json.dumps({
    "prompt": prompt,
    "max_tokens_to_sample": 1500,
    "temperature": 0.7,
    "top_k": 1,
    "stop_sequences": ["\n\nHuman"]
})

model_id = "anthropic.claude-v2"
accept = "application/json"
content_type = "application/json"

response = bedrock_runtime_client.invoke_model(
    body=body,
    modelId=model_id,
    accept=accept,
    contentType=content_type
)

response_body = json.loads(response.get('body').read())
print("Generated completion:")
print(response_body.get('completion'))
