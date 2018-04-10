import rospy
from robonomics_lighthouse.msg import Ask, Bid
from std_srvs.srv import Empty, EmptyResponse

class MakeAskBid:

    model = 'QmWboFP8XeBtFMbNYK3Ne8Z3gKFBSR5iQzkKgeNgQz3dZ4'
    token = '0x2b3ce4c151f7c9662fdd12e5b9c7b39b0d61e7f2'    # kovan
    cost  = 10
    count = 1
    deadline = 8000000

    def __init__(self):
        rospy.init_node("make_ask_bid_node")
        self.signing_ask = rospy.Publisher('lighthouse/infochan/signing/ask', Ask, queue_size=128)
        self.signing_bid = rospy.Publisher('lighthouse/infochan/signing/bid', Bid, queue_size=128)

        def callmakebid(req):
            self.makebid()
            return EmptyResponse()
        rospy.Service('make_bid', Empty, callmakebid)

        def callmakeask(req):
            self.makeask()
            return EmptyResponse()
        rospy.Service('make_ask', Empty, callmakeask)

    def spin(self):
        rospy.spin()

    def makebid(self):
        rospy.loginfo("about to make a bid")
        msg = Bid()
        msg.model = self.model
        msg.token = self.token
        msg.cost = self.cost
        msg.count = self.count
        msg.lighthouseFee = 0
        msg.deadline = self.deadline
        self.signing_bid.publish(msg)


    def makeask(self):
        rospy.loginfo("about to make an ask")
        msg = Ask()
        msg.model = self.model
        msg.objective = 'QmUo3vvSXZPQaQWjb3cH3qQo1hc8vAUqNnqbdVABbSLb6r' # should publish to /task topic
        msg.token = self.token
        msg.cost  = self.cost
        msg.count = self.count
        msg.validator = '0x0000000000000000000000000000000000000000'
        msg.deadline = self.deadline
        self.signing_ask.publish(msg)
