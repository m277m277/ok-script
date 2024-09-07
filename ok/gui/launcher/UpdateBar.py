from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QVBoxLayout
from qfluentwidgets import PushButton, ComboBox

from ok.gui.Communicate import communicate
from ok.gui.util.Alert import alert_error
from ok.logging.Logger import get_logger
from ok.update.GitUpdater import GitUpdater

logger = get_logger(__name__)


class UpdateBar(QWidget):

    def __init__(self, config, updater: GitUpdater):
        super().__init__()
        self.updater = updater

        self.layout = QVBoxLayout()

        self.version_log_label = QLabel()
        self.version_log_label.setWordWrap(True)
        self.layout.addWidget(self.version_log_label)

        self.hbox_layout = QHBoxLayout()
        self.layout.addLayout(self.hbox_layout)

        communicate.update_logs.connect(self.update_logs)
        self.hbox_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.hbox_layout.setSpacing(20)
        self.version_label = QLabel(self.tr("Current Version: ") + self.updater.version)
        self.hbox_layout.addWidget(self.version_label)
        communicate.versions.connect(self.update_versions)
        communicate.clone_version.connect(self.clone_version)
        communicate.update_running.connect(self.update_running)
        self.update_source_box = QHBoxLayout()
        self.update_source_box.setSpacing(6)

        self.hbox_layout.addLayout(self.update_source_box, stretch=0)
        self.source_label = QLabel(self.tr("Update Source:"))
        self.update_source_box.addWidget(self.source_label, stretch=0)

        self.update_sources = ComboBox()
        self.update_source_box.addWidget(self.update_sources, stretch=0)
        self.update_source_box.addSpacing(10)
        sources = config.get('git_update').get('sources')
        source_names = [source['name'] for source in sources]
        self.update_sources.addItems(source_names)
        if self.updater.launcher_config.get('source') in source_names:
            self.update_sources.setCurrentText(self.updater.launcher_config.get('source'))
        else:
            self.update_sources.setCurrentText(source_names[0])
        self.update_sources.currentTextChanged.connect(self.updater.update_source)

        self.check_update_button = PushButton(self.tr("Check for Update"))
        self.hbox_layout.addWidget(self.check_update_button)
        self.check_update_button.clicked.connect(self.updater.list_all_versions)

        self.version_list = ComboBox()
        self.version_list.setVisible(False)
        self.hbox_layout.addWidget(self.version_list)
        self.version_list.currentTextChanged.connect(self.updater.version_selection_changed)

        self.update_button = PushButton(self.tr("Update"))
        self.update_button.clicked.connect(self.update_clicked)
        self.hbox_layout.addWidget(self.update_button)

        self.update_button.setVisible(False)

        self.is_newest = QLabel(self.tr("This is the newest version"))
        self.is_newest.setVisible(False)
        self.hbox_layout.addWidget(self.is_newest)

        self.setLayout(self.layout)

    def update_logs(self, logs):
        if logs:
            self.version_log_label.setText(logs)
        else:
            self.version_log_label.setText("")
        self.version_label.setVisible(logs is not None)

    def update_clicked(self):
        self.updater.update_to_version(self.version_list.currentText())
        self.update_button.setDisabled(True)
        self.check_update_button.setDisabled(True)

    def clone_version(self, error):
        self.update_button.setDisabled(False)
        if error:
            alert_error(error)

    def update_running(self, running):
        self.update_button.setDisabled(running)
        self.check_update_button.setDisabled(running)
        self.update_sources.setDisabled(running)
        self.version_list.setDisabled(running)

    def update_versions(self, versions):
        if not versions:  # fetch version error
            self.version_list.clear()
        else:
            current_items = [self.version_list.itemText(i) for i in range(self.version_list.count())]
            if current_items != versions:
                self.version_list.clear()
                self.version_list.addItems(versions)
        self.version_list.setVisible(versions is not None)
        self.update_button.setVisible(versions is not None)
        self.is_newest.setVisible(len(versions) == 0)
