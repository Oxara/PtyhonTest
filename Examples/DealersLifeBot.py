import pyautogui as autoGui
from inputManager import InputManager
import random, time


class DealerBot:

    @staticmethod
    def OpenStore():
        position = autoGui.locateOnScreen("OpenStore.png", region=[0,0,310,574])
        if position != None:
            InputManager.LeftMouseClick(position[0], position[1])
            return True
        else:
            print(f"OpenStore is not available")
            return False

    @staticmethod
    def DailyStatus():
        position = autoGui.locateOnScreen("DailyStatus.png")
        if position != None:
            InputManager.RightMouseClick(position[0], position[1])
            return True        
        else:
            print(f"DailyStatus is not available")
            return False

    @staticmethod
    def CloseTablet():
        position = autoGui.locateOnScreen("CloseTablet.png", confidence=0.7)
        if position != None:
            InputManager.RightMouseClick(position[0], position[1])
        else:
            print(f"Tablet is not available")

    @staticmethod
    def ShowProduct():
        position = autoGui.locateCenterOnScreen("ShowProduct.png", region=[0,0,310,574])
        if position != None:
            InputManager.LeftMouseClick(position[0], position[1])
            InputManager.RightMouseClick(position[0], position[1])
        else:
            print(f"ShowProduct is not available")

    @staticmethod
    def StartBargain():
        position = autoGui.locateCenterOnScreen("StartBargain.png", region=[0,0,310,574])
        if position != None:
            InputManager.LeftMouseClick(position[0], position[1])
        else:
            print(f"StartBargain is not available")

    @staticmethod
    def FakeProduct():
        position = autoGui.locateCenterOnScreen("FakeProduct.png", region=[0,0,310,574])
        if position != None:
            InputManager.LeftMouseClick(position[0], position[1])
        else:
            print(f"FakeProduct is not available")

    @staticmethod
    def NotInterested():
        position = autoGui.locateCenterOnScreen("NotInterested.png", region=[0,0,310,574])
        if position != None:
            InputManager.LeftMouseClick(position[0], position[1])
            return True
        else:
            print(f"NotInterested is not available")
            return False

    @staticmethod
    def GetPriceEntryPosition():
        return autoGui.locateCenterOnScreen("PriceEntry.png", confidence=0.7)

    @staticmethod
    def EnterPrice():
        position = DealerBot.GetPriceEntryPosition()
        if position != None:
            InputManager.LeftMouseClick(
                position[0], position[1]
            )

            autoGui.press("1")
            #time.sleep(0.2)
            autoGui.press("enter")
            #time.sleep(0.1)
            return
        else:
            print(f"EnterPrice is not available")

    @staticmethod
    def RandomOption():
        selected_option = random.choice([1, 2, 3, 4])
        autoGui.press(str(selected_option))

    @staticmethod
    def Skip():
        position = autoGui.locateOnScreen("Skip.png")
        if position != None:
            InputManager.LeftMouseClick(position[0], position[1])
        else:
            print(f"Skip is not available")

    @staticmethod
    def OK():
        position = autoGui.locateCenterOnScreen("OK.png", confidence=0.8)
        if position != None:
            InputManager.LeftMouseClick(position[0], position[1])
            return True
        else:
            print(f"Continue is not available")
            return False            

    @staticmethod
    def Officer():
        position = autoGui.locateOnScreen("Officer.png", region=[0,0,310,574])
        if position != None:
            autoGui.press('1')
            autoGui.press('3')            
            return True
        else:
            print(f"OpenStore is not available")
            return False

    @staticmethod
    def LordManor():
        position = autoGui.locateOnScreen("LordManor.png", region=[0,0,310,574])
        if position != None:
            autoGui.press('1')
            autoGui.press('3')            
            return True
        else:
            print(f"OpenStore is not available")
            return False

    @staticmethod
    def Virgil():
        position = autoGui.locateOnScreen("Virgil.png", region=[0,0,310,574])
        if position != None:
            autoGui.press('1')
            autoGui.press('1')
            return True
        else:
            print(f"OpenStore is not available")
            return False
        
    @staticmethod
    def DonVito():
        position = autoGui.locateOnScreen("DonVito.png", region=[0,0,310,574])
        if position != None:
            autoGui.press('1')
            autoGui.press('1')
            return True
        else:
            print(f"OpenStore is not available")
            return False

    @staticmethod
    def Mickey():
        position = autoGui.locateOnScreen("Mickey.png", region=[0,0,310,574])
        if position != None:
            autoGui.press('1')
            return True
        else:
            print(f"OpenStore is not available")
            return False

    @staticmethod
    def Bob():
        position = autoGui.locateOnScreen("Bob.png", region=[0,0,310,574])
        if position != None:
            autoGui.press('2')
            autoGui.press('1')
            return True
        else:
            print(f"OpenStore is not available")
            return False
        
    @staticmethod
    def Quibble():
        position = autoGui.locateOnScreen("Quibble.png", region=[0,0,310,574])
        if position != None:
            autoGui.press('1')
            return True
        
        else:
            print(f"OpenStore is not available")
            return False
    @staticmethod
    def NPC():
        position = autoGui.locateOnScreen("NPCBorder.png", region=[0,0,310,574])
        if position != None:
            DealerBot.RandomOption()
        else:
            print("NPC is not available.")

    @staticmethod
    def Pawner():
        position = autoGui.locateOnScreen("Pawner.png", region=[0,0,310,574])
        if position != None:
            DealerBot.NotInterested()
            autoGui.press("del")
        else:
            print(f"Pawner is not available")

    @staticmethod
    def Critical():
        position = autoGui.locateOnScreen("Target.png")
        if position != None:
            autoGui.RightMouseClick(interval=0.1)
        else:
            print(f"Target is not available")

    @staticmethod
    def Seller():
        position = autoGui.locateOnScreen("Seller.png", region=[0,0,310,574])
        if position != None:

            DealerBot.ShowProduct()
            DealerBot.CloseTablet()
            DealerBot.FakeProduct()

            DealerBot.StartBargain()
            #time.sleep(0.2)
            DealerBot.EnterPrice()

            DealerBot.OK()
            DealerBot.Skip()
            DealerBot.Skip()
            DealerBot.OK()
        else:
            print(f"Seller is not available")

    @staticmethod
    def Buyer():
        position = autoGui.locateOnScreen("Buyer.png", region=[0,0,310,574])
        if position != None:

            DealerBot.ShowProduct()
            DealerBot.CloseTablet()
            DealerBot.FakeProduct()

            DealerBot.StartBargain()
            #time.sleep(0.2) 
            autoGui.press("enter")
            #time.sleep(0.1)

            DealerBot.OK()
            DealerBot.Skip()
            DealerBot.Skip()
            DealerBot.OK()

            return True
        else:
            print(f"Buyer is not available")
            return False
