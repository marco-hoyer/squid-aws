import logging
from boto import ec2
from squid_dynamodb.utils import timed

class Ec2AuthInfoProvider(object):

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s',
                            datefmt='%d.%m.%Y %H:%M:%S',
                            level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.aws = ec2.connect_to_region("eu-west-1")

    def get_instances(self, filter):
        instances = []

        reservations = self.aws.get_all_reservations(filters=filter)
        for reservation in reservations:
            instances.extend(reservation.instances)

        return instances

    def get_instance_for_private_ip(self, private_ip):
        #TODO: there could be more than one instance with same private_ip if you have multiple vpc's in your account,
        # we should reflect this here!
        instances = self.get_instances({"private-ip-address": str(private_ip)})

        if len(instances) == 1:
            return instances[0]
        elif len(instances) == 0:
            self.logger.error("No instance found for {0}.".format(private_ip))
            return None
        else:
            self.logger.error("More than one instance found for {0}. Impossible so far!".format(private_ip))
            return None

    @timed
    def get_stack_name_for_private_ip(self, private_ip):
        instance = self.get_instance_for_private_ip(private_ip)
        return instance.tags['aws:cloudformation:stack-name']


if __name__ == '__main__':
    authhelper = Ec2AuthInfoProvider()
    print authhelper.get_stack_name_for_private_ip("10.40.176.187")