# main.py
from nicegui import ui

ui.label('你好 NiceGUI!')
ui.button('点我', on_click=lambda: ui.notify('按钮被点击了'))

ui.run()