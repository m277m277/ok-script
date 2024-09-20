from paddleocr import PaddleOCR

import os

if __name__ == '__main__':
    lang = 'ch'
    paddle_model_dir = os.path.join(os.getcwd(), 'paddle_model', lang)
    PaddleOCR(det_model_dir=os.path.join(paddle_model_dir, 'det'),
              cls_model_dir=os.path.join(paddle_model_dir, 'cls'),
              rec_model_dir=os.path.join(paddle_model_dir, 'rec'), use_angle_cls=False,
              lang=lang, use_gpu=True)
