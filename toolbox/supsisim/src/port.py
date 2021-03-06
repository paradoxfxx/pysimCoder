from pyqt5  import QGraphicsPathItem, QGraphicsItem, QPainterPath, QtCore, QTransform

from supsisim.const import PW

class Port(QGraphicsPathItem):
    """A block holds ports that can be connected to."""
    def __init__(self, parent, scene, name = ''):
        super(Port, self).__init__(parent)
        self.scene = scene
        #self.scene.addItem(self)
        self.block = None
        self.name = ''
        self.line_color = QtCore.Qt.black
        self.fill_color = QtCore.Qt.black
        self.p = QPainterPath()
        self.connections = []
        self.nodeID = '0'
        self.parent = parent

    def setup(self):
        pass

    def itemChange(self, change, value):
        if change == self.ItemScenePositionHasChanged:
            for conn in self.connections:
                try:
                    conn.update_pos_from_ports()
                    conn.update_path()
                except AttributeError:
                    self.connections.remove(conn)
        return value

    def is_connected(self, other_port):
        for conn in self.connections:
            if conn.port1 == other_port or conn.port2 == other_port:
                return True
        return False

    def remove(self):
        for conn in self.connections:
            try:
                conn.remove()
            except:
                pass
        try:
            self.scene().removeItem(self)
        except AttributeError:
            pass

            try:
                self.scene().removeItem(self)
            except AttributeError:
                pass

    def setFlip(self):
        isflipped = self.parent.flip
        if isflipped:
            self.setTransform(QTransform.fromScale(-1, 1))
        else:
            self.setTransform(QTransform.fromScale(1, 1))
                
class InPort(Port):
    def __init__(self, parent, scene):
        super(InPort, self).__init__(parent, scene)
        self.setup()

    def __str__(self):
        txt  = 'InPort \n'
        txt += 'Parent : ' + self.parent.name + '\n'
        txt += 'Node ID :' + self.nodeID + '\n'
        txt += 'Connections: ' + (len(self.connections)).__str__() + '\n'
        return txt
    
    def setup(self):
        self.setPen(self.line_color)
        self.setBrush(self.fill_color)
        self.p.addRect(-PW/2, -PW/2, PW, PW)
        self.setPath(self.p)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

class OutPort(Port):
    def __init__(self, parent, scene):
        super(OutPort, self).__init__(parent, scene)
        self.setup()

    def __str__(self):
        txt  = 'OutPort \n'
        txt += 'Parent : ' + self.parent.name + '\n'
        txt += 'Node ID :' + self.nodeID + '\n'
        txt += 'Connections: ' + (len(self.connections)).__str__() + '\n'
        return txt
    
    def setup(self):
        self.setPen(self.line_color)
        self.setBrush(self.fill_color)
        self.p.addEllipse(-PW/2, -PW/2, PW, PW)
        self.setPath(self.p)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
         
class InNodePort(Port):
    def __init__(self, parent, scene):
        super(InNodePort, self).__init__(parent, scene)
        self.setup()

    def __str__(self):
        txt  = 'Node In \n'
        txt += 'Connections: ' + (len(self.connections)).__str__() + '\n'
        return txt

    def setup(self):
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

class OutNodePort(Port):
    def __init__(self, parent, scene):
        super(OutNodePort, self).__init__(parent, scene)
        self.setup()

    def __str__(self):
        txt  = 'Node Out \n'
        txt += 'Connections: ' + (len(self.connections)).__str__() + '\n'
        return txt

    def setup(self):
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

