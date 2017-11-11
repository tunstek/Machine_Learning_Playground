
class Synapse:
    def __init__(self, frm, to, weight):
        self.frm = frm
        self.to = to
        self.weight = weight
        
    def __str__(self):
        return "( " + self.frm.id + " , " + self.to.id + " , " + self.weight + " )"
