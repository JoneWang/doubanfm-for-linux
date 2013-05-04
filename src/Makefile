all: build_ui
	python main.py

build_ui:
	pyuic4 ui/player.ui > ui/player.py
	pyrcc4 ui/resources/res.qrc > ui/res_rc.py
