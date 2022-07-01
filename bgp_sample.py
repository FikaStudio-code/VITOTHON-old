# 事前に bridge0 と r1, r2 を作成しておく必要がある
# brigdge も mkrouter でよかったはず

from fika import Operator
import subprocess

global jails
jails = "/jails"

op = Operator()

op.setupbridge("bridge0")
op.setuprouter("r1")
op.setuprouter("r2")

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

######################################
### AS65002 ###
######################################
epaira, epairb = op.createpair()
op.connect("r2", epaira)
op.connect("bridge0", epairb)
op.assignip("r2", epaira, "1.0.0.2", "255.255.0.0")
op.up("r2", epaira)
op.up("bridge0", epairb)
# op.assigngw("r2", "1.0.0.2")

op.start("r1", "quagga")
op.start("r2", "quagga")
