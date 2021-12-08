import librosa
import soundfile
import numpy as np

RESAMPLE_RATE = 8000
TRUNCATION_FREQUENCY = 3400
NEW_FREQUENCY = 48000
TIME = 30
EPSILON = 1e-6
N = 30 # frame_length
origin_audio_name = ["mohe", "shijiazhuang", "clannad", "phoenix"]
name_to_truncation_time = {
  "mohe": [190, 220],
  "clannad": [60, 90],
  "phoenix": [45, 75],
  "shijiazhuang": [45, 75]
}

def audio_preprocessing():
  for name in origin_audio_name:
    raw_data, sampling_rate = librosa.load("audio/" + name + ".wav")
    truncated_data = raw_data[name_to_truncation_time[name][0] * sampling_rate : name_to_truncation_time[name][1] * sampling_rate]
    resampled_data = librosa.resample(truncated_data, sampling_rate, RESAMPLE_RATE)
    soundfile.write("audio/" + name + "_resample.wav", resampled_data, RESAMPLE_RATE)

def encode():
  all_data = np.zeros(TIME * NEW_FREQUENCY, dtype=complex)
  frame_len = N * TRUNCATION_FREQUENCY
  for i, name in enumerate(origin_audio_name): 
    resampled_data, sampling_rate = librosa.load("audio/" + name + "_resample.wav", sr=RESAMPLE_RATE)
    for frame_index in range(TIME // N):
      resampled_frame = resampled_data[frame_index * N * RESAMPLE_RATE: (frame_index + 1) * N * RESAMPLE_RATE]
      fft_data = np.fft.fft(resampled_frame)
      base = frame_index * len(origin_audio_name) * N * TRUNCATION_FREQUENCY
      all_data[base + i * frame_len : base + (i + 1) * frame_len] = fft_data[0 : frame_len]
  all_data[TIME * NEW_FREQUENCY - len(origin_audio_name) * TIME * TRUNCATION_FREQUENCY + 1 : TIME * NEW_FREQUENCY] = np.conjugate(all_data[1: len(origin_audio_name) * TIME * TRUNCATION_FREQUENCY][::-1])
  all_time_data = np.fft.ifft(all_data)
  for data in all_time_data:
    assert -EPSILON < data.imag < EPSILON
  all_time_real_data = np.array(all_time_data, dtype="float64")
  soundfile.write("audio/" + "merged_" + str(N) + ".wav", all_time_real_data, NEW_FREQUENCY)
  return all_data

def decode(frequency_domain_data):
  frame_len = N * TRUNCATION_FREQUENCY
  for i, name in enumerate(origin_audio_name):
    recovered_data = np.array([])
    for frame_index in range(TIME // N):
      base = frame_index * len(origin_audio_name) * N * TRUNCATION_FREQUENCY
      frequency_single_data = np.zeros(N * RESAMPLE_RATE, dtype=complex)
      frequency_single_data[0 : frame_len] = frequency_domain_data[base + i * frame_len : base + (i + 1) * frame_len]
      frequency_single_data[N * RESAMPLE_RATE - frame_len + 1 : N * RESAMPLE_RATE] = np.conjugate(frequency_single_data[1 : frame_len][::-1])
      ifft_data = np.fft.ifft(frequency_single_data)
      for data in ifft_data:
        assert -EPSILON < data.imag < EPSILON
      ifft_real_data = np.array(ifft_data, dtype="float64")
      recovered_data = np.concatenate((recovered_data, ifft_real_data))
    raw_data, sampling_rate = librosa.load("audio/" + name + "_resample.wav", sr=RESAMPLE_RATE)
    print(name + " error: ")
    print(np.average((recovered_data - raw_data) ** 2))
    soundfile.write("audio/" + name + "_recover_" + str(N) + ".wav", recovered_data, RESAMPLE_RATE)

if __name__ == "__main__":
  # audio_preprocessing()
  freq_data = encode()
  decode(freq_data)
  print("finish!")
