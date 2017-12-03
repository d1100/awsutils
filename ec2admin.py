import boto3
import re

sess = boto3.Session(profile_name='default')
#high level client 
ec2 = sess.resource('ec2')
#low level client
client = sess.client('ec2')

#some things you can do with low-level
#client.describe_availability_zones()
#client.describe_vpcs()
#client.describe_instances()

#high level way to see what instances and tags you have
#[(inst.id,inst.tags) for inst in ec2.instances.all()]

#check the vpcs available 
#list(ec2.vpcs.all())
#vpc1 = list(ec2.vpcs.all())[0]
#vpc1.instances
#vpc1.instances.all()

#get an instance
#compute_inst_id = 'i-xxy"-
#compute_inst = ec2.Instance(id = compute_inst_id)

#check the attributes of an instance
#compute_inst.placement
#compute_inst.placement['AvailabilityZone']
#compute_inst.vpc
#comput_inst.tags
#list(compute_inst.network_interfaces)

#set the tags on one instance
#compute_inst.create_tags(Tags=[{'Key':'Name','Value':'cpu-compute-1'}])

#crate a volume in the same availability zone as cpu-compute-1
def create_volume_for_cpu1():
    ec2.create_volume(AvailabilityZone=compute_inst.placement['AvailabilityZone'], \
                      Size=100,VolumeType='gp2',
                      TagSpecifications=[{'ResourceType':'volume', \
                                          'Tags':[{'Key':'Name', \
                                          'Value':'data1'}]}])


def next_free_sda(compute_inst):
    attached_devices = [attach['Device'] for vol in compute_inst.volumes.all() \ 
                                            for attach in vol.attachments]
    "/dev/sda{}".format( max( [int(re.match('^.*sda([0-9]+)',sda).group(1)) for sda in attached_devices]) + 1)

def attach_vol_to_instance(inst,vol_id):
    next_sda = next_free_sda(inst)
    vol = ec2.Volume(vol_id)
    vol.attach_to_instance( Device=next_sda, \ 
                            InstanceId=compute_inst_id)
