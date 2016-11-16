""" Tree node module for Huffman tree """

class TreeNode(object):
    """ Tree node for Huffman tree """

    def __init__(self, sign, prob):
        self.sign = sign
        self.probability = prob
        self.code = ''
        self.left = None
        self.right = None

    def set_code(self, code):
        """ Resursively set code value for tree """

        self.code = code
        if self.left is not None:
            self.left.set_code(self.code + '1')
        if self.right is not None:
            self.right.set_code(self.code + '0')

    def is_leaf(self):
        """ Checks if node is a leaf """
        return self.left is None and self.right is None

    def __str__(self):
        return "Sign={" + self.sign + '}, Prob='+str(self.probability)+', Code=' + self.code
