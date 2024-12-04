import subprocess


def run_ffmpeg_zoom(image_path, output_file, screensize, duration=5, fps=25, zoom_ratio=0.0015, zoom_smooth=5):
    ffmpeg_command = f"""ffmpeg -framerate {fps} -loop 1 -i {image_path} -filter_complex "[0:v]scale={screensize[0] * zoom_smooth}x{screensize[1] * zoom_smooth},zoompan=z='min(zoom+{zoom_ratio},1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={duration * fps},trim=duration={duration}[v1];[v1]scale={screensize[0]}:{screensize[1]}[v]" -map "[v]" -y {output_file}"""
    print(ffmpeg_command)
    process = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE)
    process.wait()


if __name__ == "__main__":
    W = 1080
    H = 1920
    S = 0.5
    SIZE = (int(W*S), int(H*S))
    run_ffmpeg_zoom("./images/recovery_and_naturalized_spirituality.webp", "./zoom.mp4", SIZE)