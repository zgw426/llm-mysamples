# llm-mysamples

## Amazon Bedrockの実装メモ

### Amazon Bedrock実装①：Python3(boto3)で実装してみる

- https://zenn.dev/zgw426/articles/e4046e62916d0f
    - Bedrock学びはじめ
    - PythonスクリプトでBedrockを使ってみました。
    - Pythonモジュールをインストールするとすぐ使えました。便利ですね

### Amazon Bedrock実装②：Docker on Cloud9で実装してみる

- https://zenn.dev/zgw426/articles/d5779a1c2ce1e4
    - BedrockをPythonで使える環境をDockerで用意できるようにしました。
    - 今後も考えて LangChain のモジュールもインストールしています。


### Webサーバーを立てずにlambdaを実行するhtml+JavaScript on Cloud9

- https://zenn.dev/zgw426/articles/52170421028231
    - Bedrockには直接関係ないのですが、Bedrockが使えるWebサイトを開発するために便利な環境を作りました。
    - LambdaとCloud9のHTMLプレビュー機能を使うことでWebサーバを立てずにWebサイトが利用できるようにしました。
    - Lambda内の処理でBedrockを呼び出せば、Bedrockと連携したWebサイトの開発ができる、という算段です。


### Amazon Bedrock実装③：Lambda(Python3)で実装してみる

- https://zenn.dev/zgw426/articles/cacdf290e4a599
    - Bedrockを実行するLambdaを作ります。次のブログでLambdaを使いWebサイトを作ります。


### Amazon Bedrock実装④：Cloud9環境のhtmlプレビューでBedrockを使えるようにする

- https://zenn.dev/zgw426/articles/de0892676f0bce
    - 作成したLambdaと前回のブログで作ったCloud9のHTMLプレビュー機能を組合せてWebサイトからBedrockを使えるようにしました。
    - デモ動画
    - https://www.youtube.com/watch?v=uX6io8uNTf0&t=53s



### Amazon Bedrock実装⑤：LangChainでBedrockを使ってみる

- https://zenn.dev/zgw426/articles/b260f75c516e9a
    - LangChainを使ってBedrockを使ってみます。ただ使っただけでLangChainはよくわかってません。

## Amazon Kendraの実装メモ

### Amazon Kendra実装①：Python3で使ってみる

- https://zenn.dev/zgw426/articles/6a680f9212b124
    - Kendraを実行するPythonスクリプトを作りました。
    - （日本語対応してるのありがたい）

### Amazon Kendra実装②：Kendraファセット検索やってみる

- https://zenn.dev/zgw426/articles/8e196043a33ac8
    - Kendraでより詳細な検索ができるようになるというファセット検索を試しました。
    - 追加した属性で絞込検索などができるようになります。

## RAGの実装メモ

### RAG実装①：Amazon Bedrock,Kendra(LangChain不使用)

- https://zenn.dev/zgw426/articles/a9d36104ded4de
    - BedrockとKendraを使いRAGを作りました。（LangCahinは使っていません）



