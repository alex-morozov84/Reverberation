def main():
    return """
    QMainWindow{
    background-color: white;
    }
    QWidget{
    background-color: white;  
    }
    QLabel{
    font: 35px;
    }
    QLineEdit{
    font: 15px Source Sans Pro;
    height: 30px;
    margin-bottom: 10px;
    border: 1px solid gray;
    border-radius: 5px;
    padding-left: 5px;
    }
    QComboBox{
    font: 15px Source Sans Pro;
    height: 30px;
    margin-bottom: 10px;
    border: 1px solid gray;
    border-radius: 5px;
    padding-left: 5px;
    }
    QComboBox::drop-down {
    border: 1px solid #D3D3D3;
    border-radius: 2px;
    }
    QComboBox::down-arrow {
    padding: 0px 1px 0px 5px;
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #EEEEEE, stop: 1 #FFFFFF);
    }
    QLabel{
    font: 14px Source Sans Pro;
    margin-bottom: 10px    
    }
    QPushButton#addInteriorBtn{
    background-color: #fcc324;
    border-style: outset;
    border-width: 2px;
    border-radius: 7px;
    border-color: beige;
    font: 15px Arial Bold;
    padding: 6px;
    min-width: 6em;
    }
    QPushButton#addInteriorBtn:hover{
    background-color: #fc9222;
    }
    QPushButton#resultBtn{
    background-color: #fcc324;
    border-style: outset;
    border-width: 2px;
    border-radius: 7px;
    border-color: beige;
    font: 20px Roboto-Regular;
    padding: 6px;
    min-width: 6em;
    margin: 0 auto;
    height: 40px
    }
    QPushButton#resultBtn:hover{
    background-color: #fc9222;
    }
    """

def options_group():
    return """
    QGroupBox{
    border-radius: 3px;
    font: 12px Return to classic;
    text-transform: uppercase;
    border: 1px solid gray;
    padding: 10px;
    margin-bottom: 10px;
    color: #FF5900;
    }
    QLabel{
    font: 16px Roboto-Medium;
    }
    """
def doors_and_windows_group():
    return """
    QGroupBox{
    height: 50px;
    border-radius: 3px;
    font: 12px Return to classic;
    text-transform: uppercase;
    border: 1px solid gray;
    padding: 10px;
    margin-bottom: 10px;
    color: #FF5900;
    }
    QLabel{
    font: 16px Roboto-Medium;
    }
    """
def interior_group():
    return """
    QGroupBox{
    height: 50px;
    border-radius: 3px;
    font: 12px Return to classic;
    text-transform: uppercase;
    border: 1px solid gray;
    padding: 10px;
    color: #FF5900;
    }
    QLabel{
    font: 16px Roboto-Medium;
    }
    """
def blank_group():
    return """
    QGroupBox{
    border: 0px solid gray;
    }
    """
def people_group():
    return """
    QGroupBox{
    height: 50px;
    border-radius: 3px;
    font: 12px Return to classic;
    text-transform: uppercase;
    border: 1px solid gray;
    padding: 10px;
    color: #FF5900;

    }
    QLabel{
    font: 16px Roboto-Medium;
    }
    """
def result_group():
    return """
    QGroupBox{
    height: 50px;
    border-radius: 3px;
    font: 12px Return to classic;
    text-transform: uppercase;
    border: 1px solid gray;
    padding: 10px;
    margin-bottom: 10px;
    color: #FF5900;
    }
    QLabel{
    font: 16px Roboto-Medium;
    }
    """

# Пытался ситилзиовать график (не работает)
# def chart():
#     return """
#     QChartView{
#     font: 16px Roboto-Medium;
#     }
#     legend{
#     font: 16px Roboto-Medium;
#     }
#     """