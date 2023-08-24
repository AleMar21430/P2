from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtWebEngineCore import *

class RUI_Application (QApplication):
	def __init__(self, Args):
		super().__init__(Args)

class RUI_Button (QPushButton):
	def __init__(self, Style: str = "_Default_Button"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

class RUI_Dock (QDockWidget):
	def __init__(self, Style: str = "_Default_Dock"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

class RUI_Floating_Toggle (QPushButton):
	def __init__(self, Style: str = "_Default_Floating_Toggle"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint| Qt.WindowType.WindowStaysOnTopHint)

		self.setCheckable(True)
		self.setChecked(False)
		self.Drag_Pos = QPoint(0,0)

	def mousePressEvent(self, Event: QMouseEvent):
		if Event.button() == Qt.MouseButton.RightButton:
			self.Drag_Pos = Event.pos()
		super().mousePressEvent(Event)

	def mouseMoveEvent(self, Event: QMouseEvent): 
		if Event.buttons() & Qt.MouseButton.RightButton:
			self.move(self.mapToParent(Event.pos() - self.Drag_Pos))
		super().mouseMoveEvent(Event)

class RUI_File_Browser (QFileDialog):
	def __init__(self, Style: str = "_Default_File_Browser"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

class RUI_Grid_Layout (QGridLayout):
	def __init__(self, Style: str = "_Default_Grid_Layout"):
		super().__init__()
		self.setObjectName(Style)
		self.setContentsMargins(1,1,1,1)
		self.setSpacing(1)

class RUI_Image (QPixmap):
	def __init__(self, File = None):
		Reader = QImageReader(File)
		Reader.setAllocationLimit(1024)
		super().__init__(QPixmap.fromImageReader(Reader))

class RUI_Label (QLabel):
	def __init__(self, Style: str = "_Default_Label"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.setScaledContents(True)

class RUI_Linear_Layout (QBoxLayout):
	def __init__(self, Vertical: bool = True, Margins: int = 1):
		if Vertical:
			super().__init__(QBoxLayout.Direction.TopToBottom)
			self.setAlignment(Qt.AlignmentFlag.AlignTop)
		else:
			super().__init__(QBoxLayout.Direction.LeftToRight)
			self.setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.setContentsMargins(Margins,Margins,Margins,Margins)
		self.setSpacing(1)

	def clear(self):
		for i in range(self.count()):
			self.itemAt(i).widget().hide()
			self.itemAt(i).widget().deleteLater()
		return self

class RUI_Linear_Contents (QWidget):
	def __init__(self, Style: str = "_Default_Linear_Contents", Vertical: bool = True, Margins: int = 1):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setAttribute(Qt.WidgetAttribute.WA_StyleSheetTarget)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)

		self.Layout = RUI_Linear_Layout(Vertical, Margins)
		self.setLayout(self.Layout)

class RUI_List (QListWidget):
	def __init__(self, Style: str = "_Default_List"):
		super().__init__()

		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setAttribute(Qt.WidgetAttribute.WA_StyleSheetTarget)
		self.setObjectName(Style)
		self.verticalScrollBar().setSingleStep(10)
		self.setSpacing(1)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)

class RUI_Main_Window (QMainWindow):
	def __init__(self, Style: str = "_Default_Main_Window"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)

		self.setDockNestingEnabled(True)
		self.setTabPosition(Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.West)
		self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

class RUI_Menu (QMenu):
	def __init__(self, Style: str = "_Default_Menu", Vertical: bool = True):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.Layout = RUI_Linear_Layout(Vertical)
		self.setLayout(self.Layout)

class RUI_Option (QComboBox):
	def __init__(self, Style: str = "_Default_Option"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

class RUI_Progress (QProgressBar):
	def __init__(self, Style: str = "_Default_Progress", Vertical: bool = False):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setTextVisible(False)
		if Vertical:
			self.setOrientation(Qt.Orientation.Vertical)
			self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
		else:
			self.setOrientation(Qt.Orientation.Horizontal)
			self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

	def paintEvent(self, event):
		QProgressBar.paintEvent(self, event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		painterPath = QPainterPath()
		if self.value() != -1:
			painterPath.addText(QPointF(13, self.geometry().height()/2 + QFontMetrics(self.font()).height()/2 - 3), self.font() , f"{self.value()}%")
		painter.strokePath(painterPath, QPen(QColor(0,0,0), 2.5))
		painter.fillPath(painterPath, QColor(250,250,250))

class RUI_Scroll_Area (QScrollArea):
	def __init__(self, Style: str = "_Default_Scorll_Area", Vertical: bool = True):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

		self.setWidgetResizable(True)

		self.Contents = RUI_Linear_Contents()
		self.setWidget(self.Contents)

class RUI_Slider (QSlider):
	def __init__(self, Style: str = "_Default_Slider", Vertical: bool = False):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

		if Vertical: self.setOrientation(Qt.Orientation.Vertical)
		else: self.setOrientation(Qt.Orientation.Horizontal)

class RUI_Splitter (QSplitter):
	def __init__(self, Style: str = "_Default_Splitter", Vertical: bool = True):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

		if Vertical: self.setOrientation(Qt.Orientation.Vertical)
		else: self.setOrientation(Qt.Orientation.Horizontal)

class RUI_Spreadsheet (QTableWidget):
	def __init__(self, Style: str = "_Default_Spreadsheet"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		self.horizontalHeader().setObjectName("_Horizontal")
		self.verticalHeader().setObjectName("_Vertical")

class RUI_Spreadsheet_Item (QTableWidgetItem):
	def __init__(self, Text: str = "Item"):
		super().__init__()

class RUI_Text_Stream (QTextBrowser):
	def __init__(self, Style: str = "_Default_Text_Stream"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

	def append(self, Text: str, Color: str = "255,255,255"):
		print(Text)
		super().append(f'<p style="color:rgb({Color})">{str(Text)}</p>')
		super().verticalScrollBar().setValue(super().verticalScrollBar().maximum())

	def appendPlain(self, Text: str):
		super().insertPlainText(Text)
		super().verticalScrollBar().setValue(super().verticalScrollBar().maximum())

class RUI_Tree (QTreeWidget):
	def __init__(self, Style: str = "_Default_Tree"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

		self.setHeaderHidden(True)

class RUI_Tree_Item (QTreeWidgetItem):
	def __init__(self, Parent: QTreeWidget | QTreeWidgetItem, Text: str = "Item"):
		super().__init__(Parent)
		self.setText(0, Text)

class RUI_Tab_Widget (QTabWidget):
	def __init__(self, Style: str = "_Default_Tab_Widget", Vertical: bool = True):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		if Vertical:
			self.setTabPosition(QTabWidget.TabPosition.North)
		else:
			self.setTabPosition(QTabWidget.TabPosition.West)

class RUI_Text_Input (QPlainTextEdit):
	def __init__(self, Style: str = "_Default_Text_Input"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setTabStopDistance(40)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

class RUI_HTML_Input (QTextEdit):
	def __init__(self, Style: str = "_Default_Text_Input"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

class RUI_Toggle (RUI_Button):
	def __init__(self, Style: str = "_Default_Button"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		self.setCheckable(True)
		self.setChecked(False)

class RUI_ToolBar (QToolBar):
	def __init__(self, Style: str = "_Default_Toolbar"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		self.layout().setContentsMargins(1,1,1,1)
		self.layout().setSpacing(1)

		self.setFloatable(False)
		self.setMovable(False)
		self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
		self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

class RUI_Value_Input (QLineEdit):
	def __init__(self, Type: str = "str", Style: str = "_Default_Value_Input"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

		if Type == "int":
			self.Validator = QIntValidator()
			self.setValidator(self.Validator)
		elif Type == "float":
			self.Validator = QDoubleValidator()
			self.setValidator(self.Validator)

class RUI_Web_Viewer(QWebEngineView):
	def __init__(self, Style: str = "_Default_Webview"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

class RUI_Widget (QWidget):
	def __init__(self, Style: str = "_Default_Widget"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)