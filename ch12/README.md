# 12. Hands-on 5: Bashoutter

## s3のpublic access mode
- public access modeをオンにすると、バケットの中のファイルは基本的に認証なしで誰でも閲覧できるようになる。
- URLは`http://xxx.s3-website-ap-northeast-1.amazonaws.com/`のような形式
- サーブされるファイルは `website_index_document`パラメタで指定できる。ここにhtmlファイルを渡せばいい

### CloudFront
- より本格的なウェブページをs3を使って運用する場合に追加するべきサービス
- CloudFrontには`Content Delivery Network(CDN)`と言う機能が備わっている。CDNは頻繁にアクセスされるデータをメモリにキャッシュしておくことで、クライアントがキャッシュを使ってページへのアクセスができるようになる
- CloudFrontを使うことで、HTTPS通信を設定することもできるので必須

### API Gateway
- APIの入り口として、APIのリクエストパスに従って、lambda関数などに接続を行う役割を担う。
- 一般的なサーバーにおけるルーターの役割を担う（つまり、サーバーレスのルーターとも言える）
- APIリクエストが来た時のみ起動し、APIが来ていない時は完全にシャットダウンしている。
- 一秒間に1000~10000オーダーのAPIリクエストを捌くことができるシステムを用意に構築できる。
- 月ごとに1,000,000件のリクエストまでを0円で捌くことができるため有用


