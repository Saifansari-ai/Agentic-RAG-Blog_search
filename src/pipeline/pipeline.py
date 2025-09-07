from src.logger import logging
from src.exception import MyException 
from src.components.set_sidebar import SetSidebar

class Pipeline:
    """ Run all the components"""

    def __init__(self):
        pass

    def main(self):
        setup = SetSidebar()
        setup.set_sidebar()