import numpy
import pygetwindow as getWindow

from ctypes import windll
import win32gui, win32ui, win32con, win32api


class WindowManager:
    # Monitor bilgileri
    @staticmethod
    def ShowMonitorInfo():
        monitor_infos = []
        for monitor_num in range(win32api.GetSystemMetrics(80)):
            monitor_info = win32api.GetMonitorInfo(
                win32api.MonitorFromPoint(
                    (0, 0), win32con.MONITOR_DEFAULTTOPRIMARY + monitor_num
                )
            )
            monitor_infos.append(monitor_info)

        for idx, monitor_info in enumerate(monitor_infos, start=1):
            monitor = monitor_info["Monitor"]
            work_area = monitor_info["Work"]
            print(f"Monitor {idx}:")
            print(
                f"  Monitor Area: {monitor[0]}, {monitor[1]}, {monitor[2] - monitor[0]}, {monitor[3] - monitor[1]}"
            )
            print(
                f"  Work Area: {work_area[0]}, {work_area[1]}, {work_area[2] - work_area[0]}, {work_area[3] - work_area[1]}"
            )

    # Aktif olarak çalışan uygulamaların listesi
    @staticmethod
    def ShowRunningApplications():
        screens = getWindow.getAllTitles()
        for idx, screen in enumerate(screens, start=1):
            print(f"Application {idx}: {screen}")

    # Görüntü alınmak istenen uygulama çalışıyor mu?
    @staticmethod
    def IsApplicationRunning(applicationName):
        open_windows = getWindow.getWindowsWithTitle(applicationName)

        if len(open_windows) > 0:
            return open_windows[0].isActive
        else:
            return False

    @staticmethod
    def Capture(window_name: str):
        # Adapted from https://stackoverflow.com/questions/19695214/screenshot-of-inactive-window-printwindow-win32gui
        windll.user32.SetProcessDPIAware()
        hwnd = win32gui.FindWindow(None, window_name)

        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        w = right - left
        h = bottom - top

        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        try:
            bitmap = win32ui.CreateBitmap()
            bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        except win32ui.error as e:
            print(f"Error creating compatible bitmap: {e}")
            # Additional error handling or logging can be added here

        save_dc.SelectObject(bitmap)

        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)

        img = numpy.frombuffer(bmpstr, dtype=numpy.uint8).reshape(
            (bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4)
        )
        img = numpy.ascontiguousarray(img)[
            ..., :-1
        ]  # make image C_CONTIGUOUS and drop alpha channel

        if not result:  # result should be 1
            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwnd_dc)
            raise RuntimeError(f"Unable to acquire screenshot! Result: {result}")

        return img
