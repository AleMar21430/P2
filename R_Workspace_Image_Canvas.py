from RUI_Custom import *

class R_Image_Canvas_Scene(QGraphicsScene):
	def __init__(self):
		super().__init__()
		
		self.point1 = MovablePoint(0, -100)
		self.point2 = MovablePoint(0, 100)
		self.line_charge = Line_Charge(0,-100,0,100)

		self.addItem(self.point1)
		self.addItem(self.point2)
		self.addItem(self.line_charge)

		measure_item = Measure()
		measure_item.setPos(10,0)
		self.addItem(measure_item)

	# def update(self):
	# 	self.line_charge.setLine(QLineF(self.point1.pos(), self.point2.pos()))
	# 	super().update()

class R_Workspace_Image_Canvas (RUI_Linear_Contents):
	def __init__(self, Log: RUI_Text_Stream):
		super().__init__("_Container",True)
		self.Log = Log

		self.Scene = R_Image_Canvas_Scene()
		self.Viewport = R_Image_Canvas_Viewport()
		self.Viewport.setScene(self.Scene)

		self.Layout.addWidget(self.Viewport)

class R_Image_Canvas_Viewport(RUI_Graphics_Viewport):
	BG_Color = QColor(25,25,25)
	Grid_Small = QPen(QColor(50, 50, 50), 0.5)
	Gird_Large = QPen(QColor(75, 75, 75), 0.75)
	Grid_Size = 100
	Grid_Subdivisions = int(Grid_Size / 10)
	item = None

	def __init__(self):
		super().__init__()
		self.Last_Pos_Pan = QPoint(0,0)
		self.Last_Pos_Move = QPoint(0,0)
		self.Moving_Item = False
		self.Selecting_Item = False
		self.Panning_View = False

	def drawBackground(self, painter, rect):
		painter.fillRect(rect, self.BG_Color)

		left = int(rect.left()) - (int(rect.left()) % self.Grid_Subdivisions)
		top = int(rect.top()) - (int(rect.top()) % self.Grid_Subdivisions)

		# Draw horizontal fine lines
		gridLines = []
		painter.setPen(self.Grid_Small)
		y = float(top)
		while y < float(rect.bottom()):
			gridLines.append(QLineF(rect.left(), y, rect.right(), y))
			y += self.Grid_Subdivisions
		painter.drawLines(gridLines)

		# Draw vertical fine lines
		gridLines = []
		painter.setPen(self.Grid_Small)
		x = float(left)
		while x < float(rect.right()):
			gridLines.append(QLineF(x, rect.top(), x, rect.bottom()))
			x += self.Grid_Subdivisions
		painter.drawLines(gridLines)

		# Draw thick grid
		left = int(rect.left()) - (int(rect.left()) % self.Grid_Size)
		top = int(rect.top()) - (int(rect.top()) % self.Grid_Size)

		# Draw vertical thick lines
		gridLines = []
		painter.setPen(self.Gird_Large)
		x = left
		while x < rect.right():
			gridLines.append(QLineF(x, rect.top(), x, rect.bottom()))
			x += self.Grid_Size
		painter.drawLines(gridLines)

		# Draw horizontal thick lines
		gridLines = []
		painter.setPen(self.Gird_Large)
		y = top
		while y < rect.bottom():
			gridLines.append(QLineF(rect.left(), y, rect.right(), y))
			y += self.Grid_Size
		painter.drawLines(gridLines)

		return super().drawBackground(painter, rect)

	def wheelEvent(self, event: QWheelEvent):
		zoomInFactor = 1.25
		zoomOutFactor = 1 / zoomInFactor
		oldPos = self.mapToScene(event.position().toPoint())
		if event.angleDelta().y() > 0:
			zoomFactor = zoomInFactor
		else:
			zoomFactor = zoomOutFactor

		currentScale = self.transform().m11()
		if zoomFactor * currentScale > 100.0:
			zoomFactor = 100.0 / currentScale
		elif zoomFactor * currentScale < 0.005:
			zoomFactor = 0.005 / currentScale

		self.scale(zoomFactor, zoomFactor)
		newPos = self.mapToScene(event.position().toPoint())
		delta = newPos - oldPos
		self.translate(delta.x(), delta.y())

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.RightButton or event.button() == Qt.MouseButton.MiddleButton:
			self.Panning_View = True
			self.Last_Pos_Pan = event.pos()
		elif event.button() == Qt.MouseButton.LeftButton:
			self.Moving_Item = True
			self.item = self.itemAt(event.pos())
			self.Last_Pos_Move = event.pos()

	def mouseReleaseEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.RightButton or event.button() == Qt.MouseButton.MiddleButton:
			self.Panning_View = False
		elif event.button() == Qt.MouseButton.LeftButton:
			self.Moving_Item = False

	def mouseMoveEvent(self, event: QMoveEvent):
		if self.Moving_Item and self.item is not None:
			print("Moving")
			delta = (event.pos() - self.Last_Pos_Move) / self.transform().m11()
			self.item.setPos(self.item.pos().toPoint() + delta)
			self.Last_Pos_Move = event.pos()

			for item in self.scene().items():
				if type(item) == Measure:
					item.setVector(10,5)

		elif self.Panning_View:
			delta = (event.pos() - self.Last_Pos_Pan)
			self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
			self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
			self.Last_Pos_Pan = event.pos()

		else: super().mouseMoveEvent(event)
		self.scene().update()

class MovablePoint(QGraphicsEllipseItem):
	def __init__(self, x, y):
		super().__init__(x - 4, y - 4, 8, 8)
		self.setBrush(Qt.GlobalColor.blue)
		self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable, True)
		self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable, True)
		self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
		self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemSendsScenePositionChanges, True)

class Line_Charge(QGraphicsLineItem):
	def __init__(self, x1, y1, x2, y2):
		super().__init__(x1, y1, x2, y2)
		self.setPen(QPen(Qt.GlobalColor.red))

class Measure(QGraphicsItem):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.center = QPointF(0, 0)
		self.vector = QLineF(self.center, self.center + QPointF(50, 0))
		self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
		self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
		self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
		
	def boundingRect(self):
		return self.childrenBoundingRect()

	def paint(self, painter, option, widget):
		pen = QPen(Qt.GlobalColor.white, 2)
		brush = QBrush(Qt.GlobalColor.white)
		painter.setPen(pen)
		painter.setBrush(brush)

		# Draw a dot at the center
		dot_radius = 2
		painter.drawEllipse(self.center , dot_radius * 2, dot_radius * 2)

		# Draw the vector arrow
		arrow_length = self.vector.length()
		arrow_angle = -self.vector.angle()  # Negative angle for correct orientation
		arrow_tip = self.vector.p2()
		arrow_head_size = 5

		painter.drawLine(self.center, arrow_tip)

		# Calculate arrowhead points
		transform = QTransform().translate(arrow_tip.x(), arrow_tip.y()).rotate(arrow_angle + 90)
		arrowhead_left = transform.map(QPointF(-arrow_head_size * 0.6, arrow_head_size))
		arrowhead_right = transform.map(QPointF(arrow_head_size * 0.6, arrow_head_size))

		painter.drawLine(arrow_tip, arrowhead_left)
		painter.drawLine(arrow_tip, arrowhead_right)

	def setVector(self, length, angle_degrees):
		self.vector = QLineF(self.center, self.center + QPointF(length, 0))
		self.vector.setAngle(-angle_degrees)
		self.update()