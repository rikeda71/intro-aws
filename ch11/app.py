#!/usr/bin/env python3

from aws_cdk import core

from lambdafn.app import SimpleLambda
from dynamodb.app import SimpleDynamoDB


app = core.App()
SimpleLambda(app, 'lambda')
SimpleDynamoDB(app, 'dynamodb')

app.synth()
