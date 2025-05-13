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

        #jumpstart_model = JumpStartSageMakerEndpoint(self,'MyCfnModel',
         # model=JumpStartModel.object-detection-201516,
         # ccept_eula=True,
         # instance_type=SageMakerInstanceType.ML_G5_2_XLARGE,
         # endpoint_name="zpac028-endpoint")
