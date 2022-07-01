# 事前に bridge0 と r1, r2 を作成しておく必要がある
# brigdge も mkrouter でよかったはず

from fika import Operator
from shcommand import *
import subprocess

global jails
jails = "/jails"

op = Operator()

op.setupbridge("bridge0")
op.setupbridge("bridge1")
op.setuprouter("r0")
op.setuprouter("r1")
op.setuprouter("r2")
op.setupserver("ns1")

################################################################
# Setup Backborn
#  realsever-epair0b-(epair0a-router0-epair1a-epair1b-bridge0)
################################################################
epaira, epairb = op.createpair()
ifconfig("{0} inet 192.168.11.1 netmask 255.255.255.0".format(epaira))
ifconfig("{0} up".format(epaira))
op.connect("r0", epairb)
op.assignip("r0", epairb, "192.168.11.100", "255.255.255.0")
op.up("r0", epairb)

epaira, epairb = op.createpair()
op.connect("r0", epaira)
op.assignip("r0", epaira, "1.0.0.254", "255.255.0.0")
op.connect("bridge0", epairb)
op.up("r0", epaira)
op.up("bridge0", epairb)


######################################
### AS65001 ###
######################################
epaira, epairb = op.createpair()
op.connect("r1", epaira)
op.connect("bridge0", epairb)
op.assignip("r1", epaira, "1.0.0.1", "255.255.0.0")
op.up("r1", epaira)
op.up("bridge0", epairb)
# op.assigngw("r1", "1.0.0.1")

epaira, epairb = op.createpair()
op.connect("r1", epaira)
op.connect("bridge1", epairb)
op.assignip("r1", epaira, "1.1.0.254", "255.255.0.0")
op.up("r1", epaira)
op.up("bridge1", epairb)

epaira, epairb = op.createpair()
op.connect("ns1", epaira)
op.connect("bridge1", epairb)
op.assignip("ns1", epaira, "1.1.0.1", "255.255.0.0")
op.up("ns1", epaira)
op.up("bridge1", epairb)
op.assigngw("ns1", "1.1.0.254")

### AS65002 ###
######################################
epaira, epairb = op.createpair()
op.connect("r2", epaira)
op.connect("bridge0", epairb)
op.assignip("r2", epaira, "1.0.0.2", "255.255.0.0")
op.up("r2", epaira)
op.up("bridge0", epairb)
# op.assigngw("r2", "1.0.0.2")

op.start("r0", "quagga")
op.start("r1", "quagga")
op.start("r2", "quagga")
op.start("ns1", "nsd")
