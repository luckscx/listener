import time
import speech_recognition as sr
from pynput.keyboard import Controller, Key
import librosa
from fastdtw import fastdtw
import os

keyboard = Controller()

# 预录制的命令音频文件
command_files = ['call', 'fold', 'check', 'allin', 'rise']

# 为每个文件名和预加载的音频信号构建命令列表
commands = []
for file in command_files:
    f = os.path.join("media", file + ".wav")
    print(f)
    y, res = librosa.load(f)
    mfcc = librosa.feature.mfcc(y=y, sr=res)
    commands.append((os.path.splitext(file)[0], mfcc))

# 创建 Recognizer 对象
recognizer = sr.Recognizer()


def closest_command(in_mfcc):
    min_distance = float('inf')
    min_command = None
    for command, command_mfcc in commands:
        distance, _ = fastdtw(in_mfcc.T, command_mfcc.T)
        if distance < min_distance:
            min_distance = distance
            min_command = command
    return min_command


def input_cmd(cmd):
    for char in cmd:
        keyboard.type(char)
        time.sleep(0.05)
    keyboard.tap(Key.enter)


# 实时监听麦克风输入
with sr.Microphone() as source:
    while True:
        print('Listening...')
        audio = recognizer.listen(source)

        print("done")
        # 获取音频帧率
        frame_rate = audio.sample_rate

        output_file_path = "output.wav"

        # 将音频数据保存到 wav 文件
        with open(output_file_path, 'wb') as output_file:
            output_file.write(audio.get_wav_data())

        # 使用 librosa 加载 NumPy 音频数据
        samples, res = librosa.load(output_file_path)
        # 将音频转换成 librosa 音频信号及对应的 MFCC 特征
        recording_mfcc = librosa.feature.mfcc(y=samples, sr=res)

        # 查找最接近的命令
        closest_cmd = closest_command(recording_mfcc)
        print(f"Recognized command: {closest_cmd}")
        input_cmd(closest_cmd)
