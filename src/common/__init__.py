# coding: UTF-8
import os
import logging
import tempfile


def get_logger():
    logger = logging.getLogger("DoubanFMGUI")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s]: %(message)s')

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    fh = logging.FileHandler(os.path.join(index_dir, "douban_fm.log"))
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

def ms_to_hms(time_ms):
    s = int(round(time_ms / 1000))
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return h, m, s

index_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
favicon = os.path.join(index_dir, 'ui/resources/doubanfm-0.xpm')
tmp_dir = tempfile.mkdtemp(prefix='doubanfm-tmp')
logger = get_logger()
phonon_state_label = {
        0: 'LoadingState'
        ,1: 'StoppedState'
        ,2: 'PlayingState'
        ,3: 'BufferingState'
        ,4: 'PausedState'
        ,5: 'ErrorState'
}
