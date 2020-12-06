from aws_cdk import (
    core,
    aws_dynamodb as ddb
)

class SimpleDynamoDB(core.Stack):

    def __init__(self, scope: core.App, name: str, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # <1>
        table = ddb.Table(
            self, "SimpleTable",
            # 全てのDynamoDBテーブルに指定されているべき固有のID
            partition_key=ddb.Attribute(
                name="item_id",
                type=ddb.AttributeType.STRING
            ),
            # 課金形態
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=core.RemovalPolicy.DESTROY
        )
        core.CfnOutput(self, "TableName", value=table.table_name)


