'''
iPhone 스타일의 GUI 계산기.
PyQt5를 사용하여 기본 사칙연산, %, +/- 변환, C(초기화) 기능을 제공합니다.
실행: python calculator.py
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5 import QtCore

class Calculator(QWidget):
    '''
    iPhone 스타일의 계산기 위젯 클래스.
    숫자, 연산자, 특수 기능 버튼을 포함한 UI와 계산 로직을 구현합니다.
    '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone Calculator')
        self.setFixedSize(320, 480)
        self.init_ui()
        # 계산기 상태 초기화
        self.current = ''
        self.last_result = None

    def init_ui(self):
        '''
        계산기 UI(버튼, 디스플레이 등)를 초기화합니다.
        '''
        # 그리드 레이아웃 설정
        grid = QGridLayout()
        # 디스플레이 설정
        self.display = QLineEdit('0')
        # 숫자 입력 시 디스플레이 초기화
        self.display.setAlignment(QtCore.Qt.AlignRight)
        # 읽기 전용 설정
        self.display.setReadOnly(True)
        # 고정 높이 설정
        self.display.setFixedHeight(60)
        # 그리드에 디스플레이 추가
        grid.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row, btn_row in enumerate(buttons):
            for col, btn_text in enumerate(btn_row):
                # 버튼 생성
                if btn_text == '0':
                    # 버튼 생성
                    btn = QPushButton(btn_text)
                    # 0 버튼은 두 열을 차지합니다.
                    btn.setFixedSize(140, 60)
                    grid.addWidget(btn, row+1, col, 1, 2)
                    col += 1
                else:
                    btn = QPushButton(btn_text)
                    btn.setFixedSize(60, 60)
                    grid.addWidget(btn, row+1, col, 1, 1)
                # 버튼 클릭 시 이벤트 연결
                btn.clicked.connect(self.on_button_click)
        # 레이아웃 설정
        self.setLayout(grid)

    def on_button_click(self):
        '''
        버튼 클릭 이벤트 핸들러. 입력값에 따라 계산, 초기화, 부호변경, % 연산을 처리합니다.
        '''
        # 현재 버튼의 텍스트 가져오기
        sender = self.sender()
        button_text = sender.text()
        # 숫자 및 소수점 입력 처리
        if button_text in '0123456789.':
            if self.display.text() == '0' and button_text != '.':
                self.display.setText(button_text)
            else:
                self.display.setText(self.display.text() + button_text)
        # 연산자 입력 처리
        elif button_text in '+-*/':
            self.current = self.display.text() + button_text
            self.display.setText('')
        elif button_text == '=':
            expr = self.current + self.display.text()
            try:
                # 0으로 나누기 예외 처리
                if '/0' in expr or expr.endswith('/0'):
                    raise ZeroDivisionError
                result = eval(expr)
                # 결과가 너무 크면 OverflowError 발생
                if abs(result) > 1e100:
                    raise OverflowError
                self.display.setText(str(result))
                self.last_result = result
            except ZeroDivisionError:
                self.display.setText('Error: 0으로 나눔')
            except OverflowError:
                self.display.setText('Error: 범위 초과')
            except Exception:
                self.display.setText('Error')
            self.current = ''
        elif button_text == 'C':
            self.display.setText('0')
            self.current = ''
        elif button_text == '+/-':
            val = self.display.text()
            if val.startswith('-'):
                self.display.setText(val[1:])
            elif val != '0':
                self.display.setText('-' + val)
        elif button_text == '%':
            try:
                val = float(self.display.text())
                self.display.setText(str(val / 100))
            except Exception:
                self.display.setText('Error')

if __name__ == '__main__':
    # 프로그램 진입점. QApplication을 생성하고 Calculator 위젯을 실행합니다.
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    # this code run when the application is closed
    sys.exit(app.exec_())
