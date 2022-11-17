from config import Config
from dla_image import DLAImage
from gui import MainWindow

if __name__ == '__main__':
    config = Config()
    dla_image = DLAImage(config)
    main_frame = MainWindow(dla_image, config)
