import rospy
from robonomics_msgs.msg import Demand, Offer
from ethereum_common.msg import UInt256
from ethereum_common.srv import BlockNumber
from ipfs_common.msg import Multihash

class MakeAskBid:

    model = 'QmWboFP8XeBtFMbCeMiStRY3gKFBSR5iQzkKgeNgQz3dZ5'
    # token = '0xdEA33F21294399c675C8F1D6C4a1F39b0719BCBf'    # kovan
    cost  = 1
    count = 1

    def __init__(self):
        rospy.init_node("make_ask_bid_node")

        #self.web3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
        self.signing_offer = rospy.Publisher('/liability/infochan/eth/signing/offer', Offer, queue_size=128)

        def callback(m):
            rospy.loginfo("about to make a offer")

            if m.model != Multihash(multihash=self.model):
                rospy.loginfo("Doesn't fit")
                return

            msg                 = Offer()
            msg.model           = m.model
            msg.objective       = m.objective
            msg.token           = m.token
            msg.cost            = m.cost
            msg.validator       = m.validator
            msg.lighthouse      = m.lighthouse
            rospy.wait_for_service('/eth/current_block')
            msg.lighthouseFee   = UInt256('0')
            msg.deadline        = UInt256(str(rospy.ServiceProxy('/eth/current_block', BlockNumber)().number + 100))
            rospy.loginfo("Publishing...")
            rospy.loginfo(msg)
            self.signing_offer.publish(msg)
        rospy.Subscriber('/liability/infochan/incoming/demand', Demand, callback)

    def spin(self):
        rospy.spin()

