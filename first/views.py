import os
import numpy as np
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from PIL import Image
import tensorflow_addons as tfa
import tensorflow.keras.backend as K
import tensorflow as tf
# InstanceNormalization 커스텀 객체 등록
def register_tfa_custom_objects():
    K.set_image_data_format('channels_last')
    custom_objects = {
        'InstanceNormalization': tfa.layers.InstanceNormalization,
    }
    return custom_objects

custom_objects = register_tfa_custom_objects()

# 이미지 파일 이름 카운트 변수
img_count = 0

def upload(request):
    global img_count
    img_path = None

    if request.method == 'POST':
        # 모델 선택
        model_name = request.POST.get('model')
        if model_name == 'generator1':
            model_path = os.path.join(settings.BASE_DIR, 'generator.h5')
        else:
            model_path = os.path.join(settings.BASE_DIR, 'generator2.h5')
            model = tf.saved_model.load(pb_path)

            tf.saved_model.save(model, "PATH TO SAVE MODEL")
        # 모델 로드
        model = load_model(model_path, custom_objects=custom_objects)

        # 업로드된 이미지 가져오기
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        image_path = fs.save(uploaded_image.name, uploaded_image)
        image_path = fs.path(image_path)

        # 이미지 전처리
        img = load_img(image_path, target_size=(128, 128), color_mode='grayscale')
        img = img_to_array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        # 이미지 SRGAN 적용
        generated_image = model.predict(img)

        # 생성된 고해상도 이미지 저장
        img_count += 1
        img_name = f"test_image_0.png"
        img_path = os.path.join(settings.STATIC_ROOT, img_name)
        print("##################",img_path)
        # 디렉토리 생성
        os.makedirs(os.path.dirname(img_path), exist_ok=True)

        test_img_sr = (generated_image[0] * 255.0).astype(np.uint8)
        img_sr = Image.fromarray(test_img_sr.squeeze(), mode='L')
        img_sr.save(img_path)

        # 결과 페이지로 전달
        return render(request, 'result.html', {'generated_image': img_path})

    return render(request, 'upload.html')
