# OpenCodeBlock an open-source tool for modular visual programing in python
# Copyright (C) 2021 Mathïs FEDERICO <https://www.gnu.org/licenses/>

""" Module for the base OCB Code Block. """

from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from opencodeblocks.graphics.blocks.block import OCBBlock
from opencodeblocks.graphics.pyeditor import PythonEditor


class OCBCodeBlock(OCBBlock):

    """
    Code Block

    Features an area to edit code as well as a panel to display the output.

    The following is always true:
    output_panel_height + source_panel_height + edge_size*2 + title_height == height

    """

    def __init__(self, **kwargs):
        super().__init__(block_type='code', **kwargs)

        self.output_panel_height = self.height / 3
        self._min_output_panel_height = 20
        self._min_source_editor_height = 20

        self.source_editor = self.init_source_editor()
        self.display = self.init_display()
        self.stdout = ""
        self.image = ""

        self.update_all()  # Set the geometry of display and source_editor

    def init_source_editor(self):
        """ Initialize the python source code editor. """
        source_editor = PythonEditor(self)
        self.splitter.addWidget(source_editor)
        return source_editor

    @property
    def source(self) -> str:
        """ Source code. """
        return self._source

    @source.setter
    def source(self, value: str):
        self._source = value
        if hasattr(self, 'source_editor'):
            self.source_editor.setText(self._source)

    @property
    def stdout(self) -> str:
        """ Code output. Be careful, this also includes stderr """
        return self._stdout

    @stdout.setter
    def stdout(self, value: str):
        self._stdout = value
        if hasattr(self, 'source_editor'):
            # If there is a text output, erase the image output and display the
            # text output
            self.image = ""
            self.display.setText(self._stdout)

    @property
    def image(self) -> str:
        """ Code output. """
        return self._image

    @image.setter
    def image(self, value: str):
        self._image = value
        if hasattr(self, 'source_editor') and self.image != "":
            # If there is an image output, erase the text output and display
            # the image output
            editor_widget = self.display
            editor_widget.setText("")
            qlabel = editor_widget
            ba = QByteArray.fromBase64(str.encode(self.image))
            pixmap = QPixmap()
            pixmap.loadFromData(ba)
            qlabel.setPixmap(pixmap)

    @source.setter
    def source(self, value: str):
        self._source = value
        if hasattr(self, 'source_editor'):
            editor_widget = self.source_editor
            editor_widget.setText(self._source)

    def init_display(self):
        """ Initialize the output display widget: QLabel """
        display = QLabel()
        display.setText("")
        self.splitter.addWidget(display)
        return display
