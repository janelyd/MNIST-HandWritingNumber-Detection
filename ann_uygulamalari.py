# -*- coding: utf-8 -*-
"""ANN_uygulamalari.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e1dE821QXIfL6mHzV5YguY6DbWaJgSCy

# 1)İş Problemi
Mnist sayı veri seti

# 2) Veriyi anlamak
"""

pip install tensorflow

# gerekli kütüphaneler
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical, plot_model

import matplotlib.pyplot as plt
import numpy as np

import warnings
from warnings import filterwarnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
filterwarnings('ignore')

#mnist veri setinin yüklenmesi
(x_train,y_train),(x_test,y_test) = mnist.load_data()

print("egitim seti boyutu:", x_train.shape, y_train.shape)

"""ANN, var olan veri üzerinde hangi piksel yoğunlaşmaları hangi sayıya denk geliyor onu öğren

x-->pikseller(28x28 göseller)



y--> çıktı
"""

# etiket(sınıf sayısı) hesaplama vvvv
num_labels = len(np.unique(y_train))
# ^^^^^^ burada 10 rakam oldugunu kendi seçecek, daha sağlıklı yöntem
# ama biz num_labels = 10 da diyebilirdik kendimiz belirtip
""" Ne Zaman Hangisini Kullanmalı?
Otomatik: Genel amaçlı kodlarda, farklı veri setleriyle çalışırken.
Manuel: Sınıf sayısı kesin ve değişmeyecekse, veya performans kritikse. """

# veri setinden örnek gösterilmesi
# 10x10 piksel göster
plt.figure(figsize=(10,10))
# 60k görselden 59k.yı göster:
plt.imshow(x_train[59000], cmap='gray') # gray gösterinin renk tonu

plt.figure(figsize=(10,10))
for n in range(10):
  ax = plt.subplot(5,5,n+1) #5 satır 5 sütun alt alta yaz, eksen bilgisi istemiyoruz OFF
  plt.imshow(x_train[n], cmap='gray')
  plt.axis('off')

def visualize_img(data):
  plt.figure(figsize=(10,10))
  for n in range(10):
    ax = plt.subplot(5,5,n+1) #5 satır 5 sütun alt alta yaz, eksen bilgisi istemiyoruz OFF
    plt.imshow(x_train[n], cmap='gray')
    plt.axis('off')

visualize_img(data=x_train)

# resimlerden sadece birine erişmek için
plt.figure(figsize= (10,10))
plt.imshow(x_train[2], cmap='gray');

# RGB
x_train[2]

# pikseldeki renk
x_train[2][14,10]

# resmin piksellerdeki büütn degerlerin toplamı
x_train[2].sum()

# görseli oluşturan pikseldeki sayıları, görselin üstüne koyma , görselleştirme
def pixel_visualize(img):
  fig = plt.figure(figsize=(12,12))
  ax = fig.add_subplot(111)
  ax.imshow(img, cmap = 'gray')
  width , height = img.shape

  threshold = img.max() / 2.5

  for x in range(width):
    for y in range(height):

      ax.annotate(str(round(img[x][y],2)), xy=(y,x),
                  color =  'white' if img[x][y]<threshold else 'black')

pixel_visualize(x_train[2])

"""# 3) Veriyi Hazırlama
# encoding , bğ.lı değişken için
önce [0 1 2 3 4 5 6 7 8 9]
sonra [ 0 0 1 0 0 0 0 0 0 0]
"""

y_train[0:5]

# encoding işlemi
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

y_train[0:5]

"""# Reshaping İşlemi"""

# asıl odaklandığımız pikselleri ifade etmek için
image_size = x_train.shape[1]

image_size

print(f"x_train boyutu: {x_train.shape}")
print(f"x_test boyutu: {x_test.shape}")
# yeniden şekillendirmemiz lazım

# 1 sayısı görseldeki piksellerin değerlerini tutuyor
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1 )
x_test = x_test.reshape(x_test.shape[0],28,28,1)

"""* elimizdeki pikselleri 0'la 1 arasında yapmalıyız
*  degerleri 255'e bölmeliyiz (standartlaştırma işlemi)



"""

x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255
# performans açısından hızlandırmak için floata dönüştürdük

"""# 4) Modelleme

# ***Sinir ağı mimarisini tanımlamak***

modelin yapısını tanımladık :
"""

# veri setini kendi anlicağımız şekilde reshape etmiştik
# bir de bu veriyi sinir ağının anlaycağı & kullanabileceği formata çevirmek gerek --> flatten
# sıralı katmanlardan oluşan yapay sinir ağı oluşturulacak:
model = tf.keras.Sequential([
    Flatten(input_shape = (28,28,1)), # inputun şekillendiği katman
    Dense(units= 128, activation = 'relu', name = 'layer1'),  # hidden layer, 128 nörondan oluşuyor
    # neden 128 ? aktivasyon fonksiyonu neden relu?
    # relu --> bir nöronu söndürme ya da ateşleme fonksiyonu
    # burada ağırlık & feature belirlenemediğinden kullandık ( araba olsa yaşı düştükçe fiyat artıyo derdik)
    Dense(units= num_labels, activation = 'softmax', name = 'output_layer')
    # çıktı katmanı, sınıflandırma projesindeyiz: 10 farklı sınıf var --> softmax kullandık
    # 2 sınıflı kullansaydık sigma kullanırdık

    ])

# yukarıda yaptıklarımızın bir de loss, mse sini bulacağız
# 2'den fazla sınıf oldugunda optimize edilmesi gerek kayıp fonksiyoun : catg_tropy
# loss'u minimize edecek algoritma : adam algoritması
# temel odaklandığımız metric accuracy metriği

model.compile(loss='categorical_crossentropy',
              optimizer= 'adam',
              metrics =[tf.keras.metrics.Precision(),
                      tf.keras.metrics.Recall(),
                      "accuracy"])

model.summary()

# en son basamakta modeli kurmamız lazım
# epoch sayısı: kaç defa optimizasyon işlemi yapmalı
# batch_Size : opt. işlemleri sırasında, verisetindeki verileri hep göz önünde bulundursun
# yani türev vs hesaplayarak bi sonrakine geçiriyo
model.fit(x_train,y_train, epochs=5, batch_size=128, validation_data=(x_test,y_test))
# validasyon = test aynı anlamda ?


# sınıflandırm başarısı : accuracy: 100 resimden %97sini doğru hesaplıyor gibi

"""# 5) Model başarısını Değerlendirme ( Evaluation)"""

# daha önceki modelin çıktısını historyde sakladık
history = model.fit(x_train,y_train, epochs=5, batch_size=128, validation_data=(x_test,y_test))

# accuracy ve loss değerlerini görsel olaak görmek için
# -------------Grafik 1 Accuracy-----------------
plt.figure(figsize=(20,5))
plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], color = 'b', label='Training Accuracy')
plt.plot(history.history['val_accuracy'], color='r', label='Validiation Accuracy')
plt.legend(loc='lower right')
plt.xlabel('Epoch', fontsize=16)
plt.ylabel('Accuracy', fontsize=16)
plt.ylim([min(plt.ylim()), 1])
plt.title('Egitim ve Test Başarım Grafiği', fontsize=16)

# -------------Grafik 2 Loss --------------------

plt.subplot(1,2,2)
plt.plot(history.history['loss'], color = 'b', label='Training Loss')
plt.plot(history.history['val_loss'], color='r', label='Validiation Loss')
plt.legend(loc='upper right')
plt.xlabel('Epoch', fontsize=16)
plt.ylabel('Loss', fontsize=16)
plt.ylim([0,max(plt.ylim())])
plt.title('Egitim ve Test Başarım Grafiği', fontsize=16)
plt.show()

#validiaton: modelin genelleme yeteneğini değerlendirmek için

loss, precision, recall, acc = model.evaluate(x_test, y_test, verbose=False)
print("\nTest Accuracy: %.lf%%" % (100.0 * acc))
print("\nTest Loss: %.lf%%" % (100.0 * loss))
print("\nTest Precision: %.lf%%" % (100.0 * precision))
print("\nTest Recall: %.lf%%" % (100.0 * recall))


# precision : veri seti dengesiz oldugunda lazım, precision ve recall birbirine yakın çıktığından
# tahmin ettiklerimizin başarısı : precision
# recall : kaç tanesini dogru tahmin ettik

"""# Modelin kalıcı olarak kaydedilmesi
Daha sonra tekrar kullanılmak üzere
"""

model.save('mnist_model.h5')
# modeli kaydettik

# modeli test etmek için:

import random
random = random.randint(0,x_test.shape[0])
random

test_image = x_test[random]

y_test[random]

# random seçtiğimiz --> test_image in veri setinde neye karsılık geldiğini görme
plt.imshow(test_image.reshape(28,28), cmap='gray')

# bunu modele sorma işlemi için:
# test_data az önce seçtiğimiz random sayı yani 6
test_data = x_test[random].reshape(1,28,28,1)

probability = model.predict(test_data)

probability

# içerisinde, olasılığı en yüksek olan sayıyı argmax iile görücez:
predicted_classes = np.argmax(probability)

predicted_classes

# tahmin edilen sınıfı görme:

print(f"Tahmin edilen sınıf: {predicted_classes}\n ")
print(f"Tahmin edilen sınıfın olasılık degeri: {(np.max(probability, axis=-1))[0]}\n ")
print(f"Diğer sınıfların olasılık degerleri: \n{probability} ")
