# Hands-on 1: 初めてのEC2インスタンスを起動する

## 利用するサービスの説明

### VPC
- AWS上にプライベートな仮想ネットワーク環境を構築するツール。
- EC2インスタンスが1つだけであったとしてもVPCは必ず1つは用意しなければならない

```python
vpc = ec2.Vpc(
    self, "MyFirstEc2-Vpc",
    max_azs=1,  # availability zone = 1  特にデータセンターの障害を気にする必要がない設定
    cidr="10.10.0.0/23",  # IPv4のレンジ指定。10.10.0.0 ~ 10.10.1.255までのアドレス範囲を表している。256 * 2 = 512個のユニークなIPv4アドレスを作成することになる。いくら作成しても無料
    subnet_configuration=[
        ec2.SubnetConfiguration(
            name="public",
            subnet_type=ec2.SubnetType.PUBLIC, # 外部から通信したいのでpublic。セキュリティ的な問題からEC2インスタンスなどはprivateにする
        )
    ],
    nat_gateways=0,  # 外部のネットワークと通信する必要がある場合は1以上にする。0だと課金されない
)
```

### Security Group
- EC2インスタンスに付与できる仮想ファイアウォール
- 特定IPからの通信を許可、禁止などができる

```python
sg = ec2.SecurityGroup(
    self, "MyFirstEc2Vpc-Sg",
    vpc=vpc,
    allow_all_outbound=True,  # VPCネットワークからの外部通信を許可
)
sg.add_ingress_rule(
    peer=ec2.Peer.any_ipv4(),  # 全てのIPv4ネットワークから22ポートへのアクセスを許可
    connection=ec2.Port.tcp(22),
)
```

### EC2(Elastic Compute Cloud)
- 仮想サーバーを立ち上げるサービス

```python
host = ec2.Instance(
    self, "MyFirstEc2Instance",
    instance_type=ec2.InstanceType("t2.micro"),  # t2.micro
    machine_image=ec2.MachineImage.latest_amazon_linux(),  # OS: amazon_linux
    vpc=vpc,
    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
    security_group=sg,
    key_name=key_name
)
```

## デプロイ方法

### AWSのシークレットキーをセット

```sh
$ export AWS_ACCESS_KEY_ID=***
$ export AWS_SECRET_ACCESS_KEY=***
$ export AWS_DEFAULT_REGION=ap-northeast-1
```


### ssh鍵を作成

```sh
$ export KEY_NAME='HirakeGoma'
$ aws ec2 create-key-pair --key-name ${KEY_NAME} --query 'KeyMaterial' --output text > ${KEY_NAME}.pem
$ chmod 400 HirakeGoma.pem
$ mv HirakeGoma.pem ~/.ssh/
$ chmod 400 ~/.ssh/HirakeGoma.pem
```

### デプロイの実行

```sh
$ cdk deploy -c key_name="HirakeGoma" # wait a minutes...
```

### sshによる接続

- 22ポートはパブリックネットワークに繋がっているため、sshで接続できる

```sh
$ ssh -i ~/.ssh/HirakeGoma.pem ec2-user@<IP Address>
```

## AWSコンソールによるリソースの確認

- `CloudFormation`から今回デプロイしたリソースを確認することができる

## リソースの削除

- `cdk`で管理されているので、このコマンドから簡単に消すことができる

```sh
$ cdk destroy
```

- 鍵は別管轄なので、`aws`コマンドで消す

```sh
$ aws ec2 delete-key-pair --key-name 'HirakeGoma'
$ rm -f ~/.ssh/HirakeGoma.pem
```
