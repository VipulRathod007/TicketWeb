import qrcode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime


class Ticket:
    """Represents Ticket class"""

    def __init__(self, inBuyerName: str, inContactNum: int, inSeatCount: int, inTicketID: int):
        self.__mBuyerName = inBuyerName
        self.__mContact = inContactNum
        self.__mSeatCount = inSeatCount
        self.__mTicketID = inTicketID

    @property
    def Buyer(self):
        return self.__mBuyerName

    @property
    def Contact(self):
        return self.__mContact

    @property
    def ID(self):
        return self.__mTicketID

    @property
    def Seats(self):
        return self.__mSeatCount

    @property
    def QRData(self):
        return self.__mTicketID + self.__mContact


class TicketFactory:
    """Represents Tickets Factory class"""

    def __init__(self, inBuyerName: str, inContactNum: int, inSeats: str, inSeatCount: int, inTicketID: int, inTemplatePath: str):
        self.__mSeatsAddr = (0, 0)
        self.__mBuyerNameAddr = (0, 0)
        self.__mTicketQRCodeAddr = (0, 0)
        self.__mTicketIDAddr = (0, 0)
        self.__mSeatCountAddr = (0, 0)
        self.__mSeats = inSeats
        self.__mTicket = Ticket(inBuyerName, inContactNum, inSeatCount, inTicketID)
        self.__mTemplatePath = inTemplatePath

    def generate(self) -> Image:
        templateImg = Image.open(self.__mTemplatePath)
        imgInst = ImageDraw.Draw(templateImg)
        fontName = 'times.ttf'
        imgInst.text(self.__mTicketIDAddr, str(self.__mTicket.ID), font=ImageFont.truetype(fontName, 36))
        imgInst.text(self.__mBuyerNameAddr, str(self.__mTicket.Buyer), font=ImageFont.truetype(fontName, 36))
        imgInst.text(self.__mSeatsAddr, self.__mSeats, font=ImageFont.truetype(fontName, 36))
        imgInst.text(self.__mSeatCountAddr, str(self.__mTicket.Seats), font=ImageFont.truetype(fontName, 36))
        qrImg = qrcode.make(self.__mTicket.QRData)
        templateImg.paste(qrImg.get_image().resize((250, 250)), self.__mTicketQRCodeAddr)
        templateImg.mode = 'RGB'
        # templateImg.show()
        return templateImg

    @property
    def AddrSeatCount(self):
        return self.__mSeatCountAddr

    @AddrSeatCount.setter
    def AddrSeatCount(self, inPos: tuple):
        self.__mSeatCountAddr = inPos

    @property
    def AddrSeats(self):
        return self.__mSeatsAddr

    @AddrSeats.setter
    def AddrSeats(self, inPos: tuple):
        self.__mSeatsAddr = inPos

    @property
    def AddrTicketID(self):
        return self.__mTicketIDAddr

    @AddrTicketID.setter
    def AddrTicketID(self, inPos: tuple):
        self.__mTicketIDAddr = inPos

    @property
    def AddrBuyerName(self):
        return self.__mBuyerNameAddr

    @AddrBuyerName.setter
    def AddrBuyerName(self, inPos: tuple):
        self.__mBuyerNameAddr = inPos

    @property
    def AddrTicketQRCode(self):
        return self.__mTicketQRCodeAddr

    @AddrTicketQRCode.setter
    def AddrTicketQRCode(self, inPos: tuple):
        self.__mTicketQRCodeAddr = inPos

    @property
    def Ticket(self):
        return self.__mTicket
