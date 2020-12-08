from aws_cdk import (
    core,
    aws_dynamodb as ddb,
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_lambda as _lambda,
    aws_ssm as ssm,
    aws_apigateway as apigw,
)

class Ch12Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 俳句情報を記録しておくためのDynamoDBテーブルを定義
        table = ddb.Table(
            self, 'Bashoutter-Table',
            partition_key=ddb.Attribute(
                name='item_id',
                type=ddb.AttributeType.STRING
            ),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # 続いて、静的コンテンツを配信するためのS3バケットを用意
        bucket = s3.Bucket(
            self, 'Bashoutter-Bucket',
            sebsite_index_document='index.html'
            public_read_access=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )
        s3_deploy.BuckeetDeployment(
            self, 'BucketDeployment',
            destination_bucket=bucket,
            sources=[s3_deploy.Source.asset('./gui/dist')],
            retain_on_delete=False,
        )

        # lambda関数の定義
        common_params = {
            'runtime': _lambda.Runtime.PYTHON_3_7,
            'environment': {
                'TABLE_NAME': table.table_name
            }
        }

        get_haiku_lambda = _lambda.Function(
            self, "GetHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.get_haiku",
            memory_size=512,
            **common_params,
        )
        post_haiku_lambda = _lambda.Function(
            self, "PostHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.post_haiku",
            **common_params,
        )
        patch_haiku_lambda = _lambda.Function(
            self, "PatchHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.patch_haiku",
            **common_params,
        )
        delete_haiku_lambda = _lambda.Function(
            self, "DeleteHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.delete_haiku",
            **common_params,
        )

        # DBの権限付与
        table.grant_read_data(get_haiku_lambda)
        table.grant_read_write_data(post_haiku_lambda)
        table.grant_read_write_data(patch_haiku_lambda)
        table.grant_read_write_data(delete_haiku_lambda)

        # API GateewayによってlambdaとAPIパスを紐付ける
        api = apigw.RestApi(
            self, "BashoutterApi",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            )
        )

        haiku = api.root.add_resource("haiku")
        haiku.add_method(
            "GET",
            apigw.LambdaIntegration(get_haiku_lambda)
        )
        haiku.add_method(
            "POST",
            apigw.LambdaIntegration(post_haiku_lambda)
        )

        haiku_item_id = haiku.add_resource("{item_id}")
        haiku_item_id.add_method(
            "PATCH",
            apigw.LambdaIntegration(patch_haiku_lambda)
        )
        haiku_item_id.add_method(
            "DELETE",
            apigw.LambdaIntegration(delete_haiku_lambda)
        )
