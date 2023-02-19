import logging
import multiprocessing
import os
import pathlib
import sys

exc_path = pathlib.Path(sys.executable if getattr(sys, 'frozen', False) else __file__).absolute().parent
os.environ['ExcPath'] = str(exc_path)

from nylib.logging import install
from nylib.utils.win32.process import enable_privilege, pid_by_executable, is_admin, runas
from ff_draw.main import FFDraw

install()
logging.debug(f'current Pid:%s', os.getpid())

def main():
    try:
        if not is_admin():
            runas()
            exit()
        enable_privilege()
        instance = FFDraw(next(pid_by_executable(b'ffxiv_dx11.exe')))
        instance.start_sniffer()
        instance.start_gui_thread()
        instance.start_http_server()
    except Exception as e:
        logging.critical('critical error occurred', exc_info=e)
        os.system('pause')


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        multiprocessing.freeze_support()
    main()
