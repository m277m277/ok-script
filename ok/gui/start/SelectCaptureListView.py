from PySide6.QtWidgets import QListWidgetItem
from qfluentwidgets import ListWidget


class SelectCaptureListView(ListWidget):
    def __init__(self, index_change_callback):
        super().__init__()
        self.itemSelectionChanged.connect(index_change_callback)

    def update_for_device(self, device, hwnd, capture):
        if self.count() == 0:
            item = QListWidgetItem(self.tr(f"Game Window"))
            self.addItem(item)
        tips = hwnd or ""
        if device == "windows":
            title = self.tr("Game Window")
            if self.count() == 2:
                self.takeItem(1)
        else:
            title = self.tr("Emulator Window(Supports Background, Fast, Low Latency)")
            if self.count() == 1:
                item = QListWidgetItem(self.tr("ADB(Supports Background, Slow, High Compatibility, High Latency)"))
                self.addItem(item)
        self.item(0).setText(f"{title} - {tips}")
        selected = 0 if capture == "windows" else 1
        self.setCurrentRow(selected)
