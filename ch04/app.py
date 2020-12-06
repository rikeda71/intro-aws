#!/usr/bin/env python3

from aws_cdk import core

from ch04.ch04_stack import Ch04Stack


app = core.App()
Ch04Stack(app, "ch04")

app.synth()
