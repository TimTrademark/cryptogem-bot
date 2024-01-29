from flask import render_template


class ControlPanelController:
    @staticmethod
    def index():
        return render_template("index.html")
