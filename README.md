# qiita-zenn-trend-metadata-fetcher-lambda-docker
このLambda関数は、QiitaとZennのトレンド記事のメタデータをAPIを使用してフェッチし、S3に保存するために作成されました。Dockerを使用して開発されており、Dockerfileとdocker-composeが含まれます。関数は、定期的にトリガーされ、フェッチされたメタデータをS3にアップロードします。メタデータには、記事のタイトル、著者、投稿日時、URLなどが含まれます。S3バケットの設定や、APIついては、この関数を使用する前にドキュメンテーションを確認してください。

APIについて、第三者が作成し運用している以下のAPIを利用しています。
- qiita
    - [git](https://github.com/kaisugi/qiita-trend-api)
    - API
        - トレンド : https://qiita-api.vercel.app/trend.json

- zenn
    - [git](https://github.com/kaisugi/zenn-trend-api)
    - API
        - 技術トレンド : https://zenn-api.vercel.app/trendTech.json
        - アイデアトレンド : https://zenn-api.vercel.app/trendIdea.json