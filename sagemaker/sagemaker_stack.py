from constructs import Construct
from cdklabs.generative_ai_cdk_constructs import (
    JumpStartSageMakerEndpoint,
    JumpStartModel,
    SageMakerInstanceType
)
from aws_cdk import (
    Duration,
    Stack,
    aws_sagemaker as sagemaker,
    aws_iam as iam
)



class SagemakerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

# create vpc

        # Create Sagemaker execution role
        execution_role = iam.Role(self, "MyCfnRole",
          assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
          role_name="zpac028-sagemaker-execution-role")

        # Add managed policy to Sagemaker role
        execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
          "AmazonSageMakerFullAccess"))

        # Create domain
        sagemaker_domain = sagemaker.CfnDomain(self, "MyCfnDomain",
          auth_mode="IAM",
          #default_user_settings=sagemaker.CfnDomain.UserSettingsProperty(
          #  execution_role="arn:aws:iam::605134434340:role/service-role/AmazonSageMakerDomainExecution"),
          default_user_settings=sagemaker.CfnDomain.UserSettingsProperty(
            execution_role=execution_role.role_arn),
          domain_name="zpac028-domain",
          subnet_ids=["subnet-0538a9a5a606d0942","subnet-03ef234af6a099903","subnet-075f0f959d7ad091a"],
          vpc_id="vpc-0a4bddeced3423e2c")

        # Create user profile
        sagemaker_user_profile = sagemaker.CfnUserProfile(self, "MyCfnUserProfile",
          domain_id=sagemaker_domain.attr_domain_id,
          user_profile_name="zpac028-user-profile",
          user_settings=sagemaker.CfnUserProfile.UserSettingsProperty(
            execution_role=execution_role.role_arn))

        sagemaker_user_profile.add_dependency(sagemaker_domain)


#------------------------------------------------------------------#
        model = sagemaker.CfnModel(self, "MyCfnModel",
          execution_role_arn=execution_role.role_arn,
          containers=[
            sagemaker.CfnModel.ContainerDefinitionProperty(
              image="763104351884.dkr.ecr.eu-central-1.amazonaws.com/mxnet-inference:1.9.0-gpu-py38",
          #    environment=env,
              mode="SingleModel",
              model_data_source = sagemaker.CfnModel.ModelDataSourceProperty(
                s3_data_source = sagemaker.CfnModel.S3DataSourceProperty(
                compression_type="None",
                s3_data_type="S3Prefix",
                s3_uri="s3://jumpstart-cache-prod-eu-central-1/mxnet-od/mxnet-od-ssd-512-mobilenet1-0-coco/artifacts/inference-prepack/v1.0.0/")))],
          model_name= "zpac028-model")

        endpoint_config = sagemaker.CfnEndpointConfig(self, "MyCfnEndpointConfig",
          endpoint_config_name= "zpac028-endpoint-config",
          production_variants=[
            sagemaker.CfnEndpointConfig.ProductionVariantProperty(
              model_name=model.attr_model_name,
              variant_name="AllTraffic",
              initial_variant_weight=1,
              initial_instance_count=1,
              instance_type="ml.p3.2xlarge")])

        endpoint = sagemaker.CfnEndpoint(self, "MyCfnEndpoint",
                                endpoint_name="zpac028-endpoint",
                                endpoint_config_name=endpoint_config.attr_endpoint_config_name)
