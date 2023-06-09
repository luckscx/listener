@echo off
for %%f in (*.m4a) do (
  ffmpeg -i "%%f" -vn -acodec pcm_s16le -ar 44100 -ac 2 "%%~nf.wav"
  echo Converted %%f to %%~nf.wav
)