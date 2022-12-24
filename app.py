#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 設定ファイル
import configparser

# ログ出力用ライブラリのインポート
from logging import basicConfig, getLogger, StreamHandler, DEBUG, INFO, ERROR
# ロガーのインスタンス作成
logger = getLogger(__name__)
stream_handler = StreamHandler()

# ログレベルを設定
level = DEBUG
logger.setLevel(level)
stream_handler.setLevel(level)

# --------------------------------------------------
# configparserの宣言とiniファイルの読み込み
# --------------------------------------------------
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

# IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/img/'

import os
import numpy as np
from PIL import Image
from astropy.io import fits
import img_scale

dir_path = os.getcwd()

# CONFIG
FITS_DIR = config['FitsImageViewer']['FITS_DIR']
FITS_FILE_NAME = config['FitsImageViewer']['FITS_FILE_NAME']
DIST_DIR = dir_path + '/' + config['FitsImageViewer']['DIST_DIR']
OUTPUT_FILE_NAME = config['FitsImageViewer']['OUTPUT_FILE_NAME']

import cv2
import shutil
import numpy as np

# 終了シグナルをキャッチするライブラリのインポート
import signal
from typing import Sequence
from absl import app

import wx


class Main(wx.Frame):
    def __init__(self):
        super().__init__(None, id=-1, title='FITS image viewer')


        image_data = fits.getdata(FITS_DIR + FITS_FILE_NAME)
        if len(image_data.shape) == 2:
            sum_image = image_data
        else:
            sum_image = image_data[0] - image_data[0]
            for single_image_data in image_data:
                sum_image += single_image_data

        sum_image = img_scale.sqrt(sum_image, scale_min=0, scale_max=np.amax(image_data))
        sum_image = sum_image * 512
        im = Image.fromarray(sum_image)
        if im.mode != 'RGB':
            im = im.convert('RGB')

        im.save(DIST_DIR + OUTPUT_FILE_NAME)
        im.close()

        logger.debug(DIST_DIR + OUTPUT_FILE_NAME)

        bitmap = wx.Image(DIST_DIR + OUTPUT_FILE_NAME).ConvertToBitmap()

        wx.StaticBitmap(parent=self,
                        bitmap=bitmap,
                        size=bitmap.GetSize()
                        )
        self.SetClientSize(bitmap.GetSize())
        self.Show()

# Main関数
def run() -> None:
    app = wx.App()
    main = Main()
    app.MainLoop()


class TerminatedExecption(Exception):
  pass

def raise_exception(*_):
  raise TerminatedExecption()


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  # メインの実行関数
  run()

if __name__ == '__main__':

  # execute
  try:
    # Ctrl + C (SIGINT) で終了
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # set signal handler to detect to be stopped by systemd
    signal.signal(signal.SIGTERM, raise_exception)

    app.run(main)


  # (1) if ctrl-C is pushed, stop program nomally
  except KeyboardInterrupt:
    print("KeyboardInterrupt: stopped by keyboard input (ctrl-C)")

  # (2) if stopped by systemd, stop program nomally
  except TerminatedExecption:
    print("TerminatedExecption: stopped by systemd")

  # (3) if error is caused with network, restart program by systemd
  except OSError as e:
    import traceback
    traceback.print_exc()

    print("NETWORK_ERROR")

    # program will be restarted automatically by systemd (Restart on-failure)
    raise e

  # (4) if other error, restart program by systemd
  except Exception as e:
    import traceback
    traceback.print_exc()

    print("UNKNOWN_ERROR")

    # program will be restarted automatically by systemd (Restart on-failure)
    raise e

  # 終了
  exit()