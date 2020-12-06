import os

from aws_cdk import core

from ec2_stack_for_dl.app import Ec2ForDL

app = core.App()
Ec2ForDL(
    app, "ec2-for-DL",
    key_name=app.node.try_get_context("key_name"),
    env={
        'region': os.environ['CDK_DEFAULT_REGION'],
        'account': os.environ['CDK_DEFAULT_ACCOUNT']
    }
)

app.synth()
