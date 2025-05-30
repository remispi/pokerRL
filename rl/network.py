from typing import Sequence
from tinygrad.tensor import Tensor
from tinygrad.nn import Conv2d, BatchNorm2d
import numpy as np

class ConvBlock:
    def __init__(self, c_in, c_out, kernel_size=3, stride=1,  padding=0, groups=1, dilation=1):
        self.conv = Conv2d(c_in, c_out, kernel_size, stride, padding, dilation, groups, bias=False)
        self.bn = BatchNorm2d(c_out, eps=0.001)
        
    def __call__(self, x):
        return self.bn(self.conv(x))
    
class BottleneckBlock:
    def __init__(self, c_in, c_middle, c_out, kernel_size=3, stride=1,  padding=0, groups=1, dilation=1):
        self.conv_in = Conv2d(c_in, c_middle, 1, stride, padding,dilation,groups,bias=False)
        self.bn_in = BatchNorm2d(c_middle, eps=0.001)
        self.conv_middle = Conv2d(c_middle, c_middle, kernel_size, stride, padding, dilation, groups, bias=False)
        self.bn_middle = BatchNorm2d(c_middle, eps=0.001)
        self.conv_out = Conv2d(c_middle, c_out, 1, stride, padding,dilation,groups,bias=False)
        self.bn_out = BatchNorm2d(c_out, eps=0.001)
        
    def __call__(self, x):
        reduced = self.bn_in(self.conv_in(x)).relu()
        middle = self.bn_middle(self.conv_middle(reduced)).relu()
        out = self.bn_out(self.conv_out(middle))
        return (x + out).relu()