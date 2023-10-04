import pyautogui as autoGui

class MouseButton:
    LeftButton = 'left'
    RightButton = 'right'
    MiddleButton = 'middle'

class InputManager:

    @staticmethod
    def GetMousePosition():
        mouse_x, mouse_y = autoGui.position()
        return mouse_x, mouse_y
    
    @staticmethod
    def SetMousePosition(mouse_x, mouse_y):
        autoGui.moveTo(x=mouse_x, y=mouse_y)

    @staticmethod
    def LeftMouseClick(mouse_x, mouse_y):
        InputManager.MouseClick(MouseButton.LeftButton, 1, mouse_x, mouse_y)

    @staticmethod
    def LeftMouseClick(mouse_x, mouse_y, clickCount):
        InputManager.MouseClick(MouseButton.LeftButton, clickCount, mouse_x, mouse_y)

    @staticmethod
    def RightMouseClick(mouse_x, mouse_y):
        InputManager.MouseClick(MouseButton.RightButton, 1, mouse_x, mouse_y)

    @staticmethod
    def RightMouseClick(mouse_x, mouse_y, clickCount):
        InputManager.MouseClick(MouseButton.RightButton, clickCount, mouse_x, mouse_y)

    @staticmethod
    def MiddleMouseClick(mouse_x, mouse_y):
        InputManager.MouseClick(MouseButton.MiddleButton, 1, mouse_x, mouse_y)

    @staticmethod
    def MiddleMouseClick(mouse_x, mouse_y, clickCount):
        InputManager.MouseClick(MouseButton.MiddleButton, clickCount, mouse_x, mouse_y)

    @staticmethod
    def MouseClick(targetButton, clickCount, mouse_x, mouse_y):
        InputManager.SetMousePosition(mouse_x, mouse_y)
        autoGui.mouseDown(button=targetButton, clicks=clickCount)
        autoGui.mouseUp()
