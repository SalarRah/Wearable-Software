# -*- coding: utf-8 -*-

import logging
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QListWidget, QListWidgetItem, QStackedWidget, QGridLayout, QGroupBox)
from PyQt5.QtGui import (QPixmap)

from deviceSettings import DeviceSettingsWidget

logging.basicConfig(level=logging.DEBUG)

class InterfaceWidget(QWidget):
    """
    Interface Widget.

    Interface as the central widget of the main window displaying the board informations and connected peripheral devices
    """

    # Signal for connection button clicked
    configureConnectionClicked = pyqtSignal()
    # Signal for connect
    connect = pyqtSignal()

    # Board label
    _boardLabel = None
    # Board status label
    _boardStatusLabel = None
    # Board ip and port label
    _boardIpPortLabel = None
    # Board Device stack
    _deviceStack = None
    # Board Device list
    _deviceList = None
    # Selected device
    _selectedDeviceName = None

    def __init__(self):
        """Initialize the interface widget."""
        super().__init__()

        # Initialize interface UI
        self.initUI()

    def initUI(self):
        """Initialize the ui of the interface widget."""
        # Configure button handling
        configureButton = QPushButton("Configure …")
        configureButton.clicked.connect(self.onConfigureConnection)
        connectButton = QPushButton("Connect")
        connectButton.clicked.connect(self.onConnect)

        # Image of current board
        boardPixmapLabel = QLabel()
        boardPixmap = QPixmap()
        scaledboardPixmap = boardPixmap.scaledToWidth(164)
        boardPixmapLabel.setPixmap(scaledboardPixmap)
        self._boardPixmapLabel = boardPixmapLabel

        # Label of current board status
        boardConnectionTypeLabel = QLabel('Connection Type: <b></b>')
        boardConnectionTypeLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._boardConnectionTypeLabel = boardConnectionTypeLabel

        # Label of current board status
        boardStatusLabel = QLabel('Status: <b>Offline</b>')
        boardStatusLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._boardStatusLabel = boardStatusLabel

        # Label of current board ip and port
        boardIpPortLabel = QLabel('IP: <b>–</b>')
        boardIpPortLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._boardIpPortLabel = boardIpPortLabel

        # List of connected devices
        deviceList = QListWidget()
        deviceList.itemClicked.connect(self.onSelectDevice)
        self._deviceList = deviceList

        # Stack of connected device settings
        deviceStack = QStackedWidget()
        self._deviceStack = deviceStack

        # Layout for information box
        informationGridLayout = QGridLayout()
        informationGridLayout.addWidget(boardConnectionTypeLabel,   0, 0, 1, 2, Qt.AlignLeft)
        informationGridLayout.addWidget(boardStatusLabel,           1, 0, Qt.AlignLeft)
        informationGridLayout.addWidget(boardIpPortLabel,           1, 1, Qt.AlignLeft)
        informationGridLayout.addWidget(connectButton,              2, 0, Qt.AlignLeft)
        informationGridLayout.addWidget(configureButton,            2, 1, Qt.AlignLeft)

        # Group informations
        groupLayout = QGroupBox('Information')
        groupLayout.setLayout(informationGridLayout)
        self._groupLayout = groupLayout

        # Grid for the interface layout
        bodyGridLayout = QGridLayout()
        bodyGridLayout.addWidget(boardPixmapLabel,      0, 0, Qt.AlignCenter)
        bodyGridLayout.addWidget(groupLayout,           0, 1, Qt.AlignLeft)
        bodyGridLayout.addWidget(deviceList,            1, 0, Qt.AlignLeft)
        bodyGridLayout.addWidget(deviceStack,           1, 1, Qt.AlignLeft)

        # Define stretching behaviour
        bodyGridLayout.setRowStretch(0, 1)
        bodyGridLayout.setRowStretch(1, 10)
        bodyGridLayout.setColumnStretch(0, 1)
        bodyGridLayout.setColumnStretch(1, 10)

        self.setLayout(bodyGridLayout)

    def setBoardInformation(self, board):
        """Set board information."""
        #Set name label
        self._groupLayout.setTitle(board.name())

        #Set image label
        boardPixmap = QPixmap('assets/{}.jpg'.format(board.name()))
        scaledboardPixmap = boardPixmap.scaledToWidth(164)
        self._boardPixmapLabel.setPixmap(scaledboardPixmap)

        #Set connection type
        self._boardConnectionTypeLabel.setText('Connection Type <b>{}</b>'.format(board.connectionType()))

    def setStatus(self, status):
        """Set states label."""
        self._boardStatusLabel.setText('Status <b>{}</b>'.format(status))

    def setIpAndPort(self, ip, port):
        """Set ip and port label."""
        self._boardIpPortLabel.setText('IP <b>{}</b> : <b>{}</b>'.format(ip, port))

    def updateDeviceList(self, devices):
        """Update device stack."""
        # Remove devices from list/stack
        while self._deviceList.count() > 0:
            self._deviceList.takeItem(0)
        while self._deviceStack.count() > 0:
            deviceWidget = self._deviceStack.widget(0)
            self._deviceStack.removeWidget(deviceWidget)
        # Add devices to list/stack
        deviceToSelect = None
        deviceListItemToSelect = None
        deviceWidgetToSelect = None
        for device in devices:
            deviceListItem = QListWidgetItem(device.name())
            deviceWidget = DeviceSettingsWidget(device)
            self._deviceList.addItem(deviceListItem)
            self._deviceStack.addWidget(deviceWidget)
            # Check for previous selection
            if (device.name() == self._selectedDeviceName):
                deviceToSelect = device
                deviceListItemToSelect = deviceListItem
                deviceWidgetToSelect = deviceWidget
        # Reselect device
        if (deviceToSelect != None):
            self._deviceList.setCurrentItem(deviceListItemToSelect)
            self._deviceStack.setCurrentWidget(deviceWidgetToSelect)
        elif (len(self._deviceList) > 0):
            self._deviceList.setCurrentRow(0)
            self._deviceStack.setCurrentIndex(0)


        # Sort the device list
        self._deviceList.sortItems(Qt.AscendingOrder);

    def updateData(self):
        """Update all data elements."""
        # Update data for all devices
        for i in range(0, self._deviceList.count()):
            self._deviceStack.widget(i).updateData()


    @pyqtSlot()
    def onConfigureConnection(self):
        """Listen to configure connection click event."""
        self.configureConnectionClicked.emit()
    @pyqtSlot()
    def onConnect(self):
        """Listen to configure connection click event."""
        self.connect.emit()
    @pyqtSlot(QListWidgetItem)
    def onSelectDevice(self, listItem):
        """Listen to device selection event."""
        # Check if the list isn't empty
        name = listItem.text()
        if (self._deviceList.count() > 0):
            # Look for widget with name
            for i in range(0, self._deviceList.count()):
                deviceWidget = self._deviceStack.widget(i)
                # Break on first matching widget found
                if (deviceWidget.device().name() == name):
                    self._deviceStack.setCurrentWidget(deviceWidget)
                    self._selectedDeviceName = name
                    break
            # Ignore when widget does no longer exist
            else:
                pass
