from PyQt5.QtGui import QPen


class Pen(QPen):
    def __init__(self, witdh, brush, style):
        super(Pen, self).__init__()
        self.setWidth(witdh)
        self.setBrush(brush)
        self.setStyle(style)
