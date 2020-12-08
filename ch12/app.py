#!/usr/bin/env python3

from aws_cdk import core

from ch12.ch12_stack import Ch12Stack


app = core.App()
Ch12Stack(app, "ch12")

app.synth()
