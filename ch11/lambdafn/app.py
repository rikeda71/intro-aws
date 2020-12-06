from aws_cdk import (
    core,
    aws_lambda as _lambda
)
import os

# lambdaで実行するメソッドの定義
FUNC = """
import time
from random import choice, randint
def handler(event, context):
    time.sleep(randint(2,5))
    pokemon = ["ヒトカゲ", "ゼニガメ", "フシギダネ"]
    message = "オーキド博士> Congratulations! You are given " + choice(pokemon)
    print(message)
    return message
"""

class SimpleLambda(core.Stack):

    def __init__(self, scope: core.App, name: str, **kargs) -> None:
        super().__init__(scope, name, **kargs)

        # lambda handler の設定
        handler = _lambda.Function(
            self, 'SimpleLambdaHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,  # python3.7 の環境で実施
            code=_lambda.Code.from_inline(FUNC), # 実行されるべき関数が書かれたコードを指定。文字列の他にファイルも指定可能
            handler='index.handler',             # index.`handler`関数をメイン関数として実行する。 handlerを変更したら他のメソッドを実行する
            memory_size=128,                     # 最大メモリサイズ
            timeout=core.Duration.seconds(10),   # タイムアウトまでの時間
            dead_letter_queue_enabled=True
        )
