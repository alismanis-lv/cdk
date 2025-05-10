#!/usr/bin/env python3

import aws_cdk as cdk

from sagemaker.sagemaker_stack import SagemakerStack


app = cdk.App()
SagemakerStack(app, "SagemakerStack")

app.synth()
