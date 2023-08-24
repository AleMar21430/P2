from RUI_Core import *

class RUI_Toast(RUI_Menu):
	def __init__(self, Message = "Message", Position = "Center", color = "250,50,50"):
		super().__init__()
		Layout = RUI_Linear_Layout()
		Label = RUI_Label()
		Label.setText(Message)
		Layout.addWidget(Label)
		self.setLayout(Layout)
		self.setWindowTitle(Message)
		self.setStyleSheet(f"color:rgb({color}); font-size:26px; padding: 5px 10px 5px 10px;")
		self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.Popup)
		self.setFixedSize(Label.sizeHint())

		if type(Position) == str:
			Position = QPoint(960 - (Label.sizeHint().width()/2),1080 - (Label.sizeHint().height()*4))

		timer = QTimer()
		timer.timeout.connect(self.close)
		timer.start(1500)
		self.exec(Position)

class RUI_Graphics_Viewport (QGraphicsView):
	def __init__(self):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setContentsMargins(0,0,0,0)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

		self.setRenderHint(QPainter.RenderHint.Antialiasing)
		self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
		self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
		self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setMouseTracking(True)
		self.Panning_View = False
		self.currentScale = 1

	def wheelEvent(self, event: QWheelEvent):
		zoomFactor = 1.25
		
		oldPos = self.mapToScene(event.position().toPoint())
		if event.angleDelta().y() > 0:
			self.scale(zoomFactor, zoomFactor)
			self.currentScale *= zoomFactor
		elif self.currentScale > 0.1:
			self.scale(1/zoomFactor, 1/zoomFactor)
			self.currentScale /= zoomFactor
		
		newPos = self.mapToScene(event.position().toPoint())
		delta = newPos - oldPos
		self.translate(delta.x(), delta.y())

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.RightButton:
			self.Panning_View = True
			self.lastPos = event.pos()

	def mouseReleaseEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.RightButton:
			self.Panning_View = False

	def mouseMoveEvent(self, event: QMoveEvent):
		if self.Panning_View:
			delta = (event.pos() - self.lastPos)
			self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
			self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
			self.lastPos = event.pos()
		else: super().mouseMoveEvent(event)

class RUI_Pair(RUI_Linear_Contents):
	def __init__(self, First: RUI_Widget, Second: RUI_Widget, Vertical: bool = False):
		super().__init__(Vertical = Vertical, Margins = 0)
		self.Layout.addWidget(First)
		self.Layout.addWidget(Second)
		self.Layout.setStretch(0,1)
		self.Layout.setStretch(1,1)

class RUI_Drop_Down(RUI_Linear_Contents):
	def __init__(self):
		super().__init__()
		Toggle = RUI_Toggle()
		self.Contents = RUI_Linear_Contents()
		self.Layout.addWidget(Toggle)
		self.Layout.addWidget(self.Contents)
		self.Contents.setFixedHeight(0)
		Toggle.clicked.connect(lambda Checked: self.expandCollapse(Checked))

	def expandCollapse(self, Checked):
		if (Checked):
			self.Contents.setFixedHeight(self.Contents.sizeHint().height())
		else:
			self.Contents.setFixedHeight(0)

class RUI_Input(RUI_Linear_Contents):
	def __init__(self, Widget: RUI_Widget, Title: str = "Value"):
		super().__init__(Vertical = True, Margins = 0)

		self.Label = RUI_Label("Label")
		self.Label.setText(Title)
		self.Layout.addWidget(self.Label)
		self.Layout.addWidget(Widget)

class RUI_Input_Slider(RUI_Linear_Contents):
	def __init__(self, Type = "int", Min = 0, Max = 10, Float_Decimals = 2):
		super().__init__(Vertical = True, Margins = 0)
		self.Type = Type

		Layout = RUI_Linear_Layout(False, 0)
		self.Popup_Line = RUI_Menu()
		self.Popup_Line.setLayout(Layout)

		if Type == "int":
			self.Line = RUI_Value_Input("int")
			self.Input = RUI_Int_Slider(self, Min, Max)
			self.Layout.addWidget(self.Input)
		else:
			self.Line = RUI_Value_Input("float")
			self.Input = RUI_Float_Slider(self, Float_Decimals, Min, Max)
			self.Layout.addWidget(self.Input)

		Layout.addWidget(self.Line)
		self.Line.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
		self.Line.textChanged.connect(self.updateSlider)
		self.Line.returnPressed.connect(self.updateText)

	def setValue(self, Value = 0):
		if self.Type == "int":
			self.Input.setValue(int(Value))
		else:
			self.Input.setValue(str(round(Value,2)))
		return self

	def updateSlider(self):
		if self.Type == "int":
			self.Input.setValue(int(self.Line.text()))
		else:
			self.Input.setValue(self.Line.text())

	def textEdit(self):
		if self.Type == "int":
			self.Line.setText(str(self.Input.value()))
		else:
			self.Line.setText(str(round(self.Input.value()/10**self.Input.Decimals,self.Input.Decimals)))
		self.Line.selectAll()
		self.Line.setFocus()
		self.Line.setFixedSize(self.Input.width(), self.Input.height())
		self.Popup_Line.setFixedSize(self.Input.width(), self.Input.height())
		self.Popup_Line.exec(self.mapToGlobal(QPoint(self.Input.pos().x()-1,self.Input.pos().y()-1)))

	def updateText(self):
		self.Popup_Line.close()

	def value(self):
		if self.Type == "int":
			return self.Input.value()
		else:
			return round(self.Input.value()/10**self.Input.Decimals,self.Input.Decimals)

class RUI_Int_Slider(RUI_Slider):
	def __init__(self, Parent: RUI_Input_Slider, Min = 0, Max = 100):
		super().__init__()
		self.Parent = Parent
		self.setRange(Min,Max)

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.LeftButton:
			Option = QStyleOptionSlider()
			self.initStyleOption(Option)
			Slider_Size = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, Option, QStyle.SubControl.SC_SliderHandle, self)
			if event.pos() not in Slider_Size.getCoords():
				Handle_Size = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, Option, QStyle.SubControl.SC_SliderGroove, self)
				Center = Slider_Size.center() - Slider_Size.topLeft()
				Pos = event.pos() - Center
				Length = Slider_Size.width()
				Min = Handle_Size.x()
				Max = Handle_Size.right() - Length + 1
				Pos = Pos.x()
				Value = self.style().sliderValueFromPosition( self.minimum(), self.maximum(), Pos - Min, Max - Min)
				self.setSliderPosition(Value)
			super().mousePressEvent(event)
		elif event.button() == Qt.MouseButton.RightButton and not self.isSliderDown():
			self.Parent.textEdit()

	def paintEvent(self, event):
		QSlider.paintEvent(self, event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		painterPath = QPainterPath()
		painterPath.addText(QPointF(13, self.geometry().height()/2 + QFontMetrics(self.font()).height()/2 - 3), self.font() , str(self.value()))
		painter.strokePath(painterPath, QPen(QColor(0,0,0), 2.5))
		painter.fillPath(painterPath, QColor(250,250,250))

	def wheelEvent(self, event: QWheelEvent):
		pass

class RUI_Float_Slider(RUI_Slider):
	def __init__(self, Parent: RUI_Input_Slider, Decimals = 2, Min = 0, Max = 10):
		super().__init__()
		self.Parent = Parent
		self.Decimals = Decimals
		self.Min = Min
		self.Max = Max

		self.setRange(Min*10**Decimals,Max*10**Decimals)

	def setValue(self, value):
		super().setValue(int(float(value)*10**self.Decimals))

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.LeftButton:
			Option = QStyleOptionSlider()
			self.initStyleOption(Option)
			Slider_Size = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, Option, QStyle.SubControl.SC_SliderHandle, self)
			if event.pos() not in Slider_Size.getCoords():
				Handle_Size = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, Option, QStyle.SubControl.SC_SliderGroove, self)
				Center = Slider_Size.center() - Slider_Size.topLeft()
				Pos = event.pos() - Center
				Length = Slider_Size.width()
				Min = Handle_Size.x()
				Max = Handle_Size.right() - Length + 1
				Pos = Pos.x()
				Value = self.style().sliderValueFromPosition( self.minimum(), self.maximum(), Pos - Min, Max - Min)
				self.setSliderPosition(Value)
			super().mousePressEvent(event)
		elif event.button() == Qt.MouseButton.RightButton and not self.isSliderDown():
			self.Parent.textEdit()

	def paintEvent(self, event):
		QSlider.paintEvent(self, event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		painterPath = QPainterPath()
		painterPath.addText(QPointF(13, self.geometry().height()/2 + QFontMetrics(self.font()).height()/2 - 3), self.font() , str(round(self.value()/10**self.Decimals, self.Decimals)))
		painter.strokePath(painterPath, QPen(QColor(0,0,0), 2.5))
		painter.fillPath(painterPath, QColor(250,250,250))

	def wheelEvent(self, event: QWheelEvent):
		pass