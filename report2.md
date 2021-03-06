# 频分复用 实验报告

2019011265 计93 丁韶峰

## 实现心得

### 音频预处理

只需使用 librosa 库，将音频读进来，在相应的时间截断 30s，然后进行 8000Hz 的重采样再保存即可。

### 编码

由于对整段音频进行频分复用等同于帧长度 N = 30s，下面只对分帧的情形进行说明。

对于每段音频，按帧长度切分成 TIME / N 段，然后对切分后的帧做 FFT，将得到的频域结果填充到相应位置即可。填充完数据后进行共轭对称，以满足 DFT 的性质。做一次 IFFT 可得到合并后的音频，听起来会有尖锐的噪音。

### 解码

对每段音频，找到频域中相应帧的位置，移到 8000Hz 的频域上进行共轭对称，再做 IFFT 得到时域上的一帧，将各帧拼起来即得到音频，听起来和重采样后的音频没什么区别。

## 附件说明

原始音频为《漠河舞厅》，《杀死那个石家庄人》，《時を刻む唄》，《Phoenix》四首歌曲。

我提交了共 33 段音频：

截取 30s，未改变采样率的 4 段音频。为 *_30s.wav，

截取 30s，重采样至 8000Hz 的 4 段音频，为 *_resample.wav，

在 N = 1, 2, 5, 10, 30 下，经合并和恢复的共 25 段音频，为 *_N.wav。