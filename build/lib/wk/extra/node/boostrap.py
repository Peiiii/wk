from .node import *

class BoostrapBadgeBase(Span):
    def __init__(self,text,type):
        super().__init__(_class="badge badge-%s"%(type))
        self.__call__(text)
class Badges:
    @staticmethod
    def primary(text):
        return BoostrapBadgeBase(text,type="primary")
    @staticmethod
    def secondary(text):
        return BoostrapBadgeBase(text,type="secondary")
    @staticmethod
    def success(text):
        return BoostrapBadgeBase(text,type="success")
    @staticmethod
    def danger(text):
        return BoostrapBadgeBase(text,type="danger")

    @staticmethod
    def warning(text):
        return BoostrapBadgeBase(text,type="warning")

    @staticmethod
    def info(text):
        return BoostrapBadgeBase(text,type="info")

    @staticmethod
    def light(text):
        return BoostrapBadgeBase(text,type="light")

    @staticmethod
    def dark(text):
        return BoostrapBadgeBase(text,type="dark")

