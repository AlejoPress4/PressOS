
def apply_styles(object, style):
    object.setStyleSheet(style)


desktopST = """
        QWidget#centralwidget {
            background-image: url('../graphic_resources/images/Untitled.png');
            background-repeat: no-repeat;
            background-position: center;
        }
        QGroupBox#group_box {
            background: transparent;
        
        }
    """    