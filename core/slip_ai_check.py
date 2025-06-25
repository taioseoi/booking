from fastai.vision.all import *

def train_slip_classifier(data_path):
    """
    ใช้เทรนโมเดลตรวจจับสลิปจริง/ปลอม
    - data_path = path ที่มีโฟลเดอร์ real_slips/ และ fake_slips/
    """
    dls = ImageDataLoaders.from_folder(
        data_path, valid_pct=0.2, item_tfms=Resize(224), batch_tfms=aug_transforms()
    )
    learn = vision_learner(dls, resnet18, metrics=accuracy)
    learn.fine_tune(3)
    learn.export('slip_classifier.pkl')
    return learn

def predict_slip(img_path, model_path='slip_classifier.pkl'):
    """
    โหลดโมเดลและทำนายภาพสลิปว่าเป็นของจริงหรือปลอม
    - img_path = path ของไฟล์ภาพ
    - model_path = path ของไฟล์โมเดลที่ export ไว้
    """
    learn = load_learner(model_path)
    pred, pred_idx, probs = learn.predict(img_path)
    return pred, float(probs[pred_idx])