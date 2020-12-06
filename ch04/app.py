import os

from aws_cdk import core

from ec2_stack.app import MyFirstEC2

app = core.App()
MyFirstEC2(
    app, "ec2",
    key_name=app.node.try_get_context("key_name"),
    env={
        'region': os.environ['CDK_DEFAULT_REGION'],
        'account': os.environ['CDK_DEFAULT_ACCOUNT']
    }
)

app.synth()
