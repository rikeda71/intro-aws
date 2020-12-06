#!/usr/bin/env python3

from aws_cdk import core

from ch08.ch08_stack import Ch08Stack


app = core.App()
Ch08Stack(app, "ch08")

app.synth()
