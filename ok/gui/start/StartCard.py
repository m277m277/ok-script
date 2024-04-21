from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon, SettingCard, PushButton

import ok
from ok.gui.Communicate import communicate
from ok.gui.widget.StatusBar import StatusBar


class StartCard(SettingCard):
    def __init__(self):
        super().__init__(FluentIcon.PLAY, f'{self.tr("Start")} {ok.gui.app.title}', ok.gui.app.title)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.status_bar = StatusBar("test", done_icon=FluentIcon.PAUSE)
        self.hBoxLayout.addWidget(self.status_bar, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.start_button = PushButton(FluentIcon.PLAY, self.tr("Start"), self)
        self.hBoxLayout.addWidget(self.start_button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.update_status()
        self.start_button.clicked.connect(self.clicked)
        communicate.executor_paused.connect(self.update_status)
        communicate.task.connect(self.update_task)

    def clicked(self):
        if ok.gui.executor.paused:
            ok.gui.executor.start()
        else:
            ok.gui.executor.pause()

    def update_task(self, task):
        self.update_status()

    def update_status(self):
        if ok.gui.executor.paused:
            self.start_button.setText(self.tr("Start"))
            self.start_button.setIcon(FluentIcon.PLAY)
            self.status_bar.hide()
        else:
            self.start_button.setText(self.tr("Pause"))
            self.start_button.setIcon(FluentIcon.PAUSE)
            if task := ok.gui.executor.current_task:
                self.status_bar.setTitle(f'{self.tr("Running")} {task.name}')
            elif active_trigger_task_count := ok.gui.executor.active_trigger_task_count():
                self.status_bar.setTitle(f'{self.tr("Running")} {active_trigger_task_count} {self.tr("trigger tasks")}')
            else:
                self.status_bar.setTitle(f'{self.tr("Waiting for task to be enabled")}')
            self.status_bar.setState(False)
            self.status_bar.show()