from aws_cdk import (
    core,
    aws_ec2 as ec2,
)

class Ec2ForDL(core.Stack):

    def __init__(self, scope: core.App, name: str, key_name: str, **kargs) -> None:
        super().__init__(scope, name, **kargs)

        # VPCの設定
        vpc = ec2.Vpc(
            self, 'Ec2ForDL-Vpc',
            max_azs=1,
            cidr='10.10.0.0/23',
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='public',
                    subnet_type=ec2.SubnetType.PUBLIC,
                )
            ],
            nat_gateways=0,
        )

        # Security Groupの設定
        ## 任意のIPv4のアドレスからのポート22への接続を許可
        sg = ec2.SecurityGroup(
            self, 'Ec2ForDL-Sg',
            vpc=vpc,
            allow_all_outbound=True,
        )
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
        )

        # Ec2 Instanceの設定
        host = ec2.Instance(
            self, 'Ec2ForDL-Instance',
            instance_type=ec2.InstanceType('g4dn.xlarge'),
            machine_image=ec2.MachineImage.generic_linux({
                'ap-northeast-1': 'ami-09c0c16fc46a29ed9'
            }),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=sg,
            key_name=key_name
        )
