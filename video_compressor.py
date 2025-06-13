import os
import ffmpeg
import subprocess

def install_ffmpeg_python():
    """Checks if ffmpeg-python is installed and installs it if not."""
    try:
        import ffmpeg
        print("ffmpeg-python is already installed.")
    except ImportError:
        print("ffmpeg-python not found. Installing...")
        try:
            subprocess.check_call(['pip', 'install', 'ffmpeg-python'])
            print("ffmpeg-python installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing ffmpeg-python: {e}")
            print("Please install it manually: pip install ffmpeg-python")
            return False
    return True

def compress_video(input_path, output_path, target_bitrate_factor=0.1):
    """
    Compresses a video by reducing its resolution and bitrate.

    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the compressed video file.
        target_bitrate_factor (float): Factor to reduce the original bitrate by.
                                      Aims for roughly 1/10th of the size by targeting bitrate.
    """
    try:
        print(f"Starting compression for: {input_path}")
        # Get original video information
        probe = ffmpeg.probe(input_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if not video_stream:
            print(f"No video stream found in {input_path}")
            return False

        original_width = int(video_stream['width'])
        original_height = int(video_stream['height'])
        original_bitrate_str = video_stream.get('bit_rate')
        if original_bitrate_str:
            original_bitrate = int(original_bitrate_str)
        else: # if bit_rate is not available, estimate based on file size and duration
            duration_str = video_stream.get('duration', probe.get('format', {}).get('duration'))
            if duration_str and float(duration_str) > 0:
                file_size_bytes = os.path.getsize(input_path)
                original_bitrate = int((file_size_bytes * 8) / float(duration_str))
                print(f"Original bitrate not found, estimated to: {original_bitrate / 1000:.0f} kbps")
            else:
                original_bitrate = 1000000 # Default to 1Mbps if not found and cannot estimate
                print(f"Original bitrate and duration not found, defaulting to: {original_bitrate / 1000:.0f} kbps")

        # Calculate new dimensions
        if original_width > 1280: # For HD content, scale down more significantly
            scale_width = 640
        elif original_width > 640:
            scale_width = 480
        else:
            scale_width = original_width // 2 if original_width > 320 else original_width # Halve if already small, but not too small
            if scale_width < 240: scale_width = 240 # Minimum width
        
        # Target video bitrate for significant size reduction
        # Ensure bitrate is in kbps for ffmpeg
        target_video_bitrate_value = int((original_bitrate / 1000) * target_bitrate_factor)
        if target_video_bitrate_value < 50: # Set a minimum sensible bitrate like 50kbps
            target_video_bitrate_value = 50
        target_video_bitrate_str = str(target_video_bitrate_value) + 'k'
        
        print(f"Original resolution: {original_width}x{original_height}, Original Bitrate: {original_bitrate / 1000:.0f} kbps")
        print(f"Targeting width: {scale_width}, Target video bitrate: {target_video_bitrate_str}")

        (ffmpeg
         .input(input_path)
         .output(output_path, vf=f'scale={scale_width}:-2', vcodec='libx264', preset='medium', video_bitrate=target_video_bitrate_str, acodec='aac', audio_bitrate='128k')
         .overwrite_output()
         .run(capture_stdout=True, capture_stderr=True))
        
        print(f"Successfully compressed {input_path} to {output_path}")
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        print(f"Original size: {original_size / (1024*1024):.2f} MB")
        print(f"Compressed size: {compressed_size / (1024*1024):.2f} MB")
        print(f"Reduction: {((original_size - compressed_size) / original_size) * 100:.2f}%")
        return True
    except ffmpeg.Error as e:
        print(f"Error compressing {input_path}:")
        print(f"FFmpeg stdout: {e.stdout.decode('utf8') if e.stdout else 'N/A'}")
        print(f"FFmpeg stderr: {e.stderr.decode('utf8') if e.stderr else 'N/A'}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred with {input_path}: {e}")
        return False

def main():
    if not install_ffmpeg_python():
        return

    input_folder = 'downloads' # Assumes videos are in 'downloads' folder
    output_folder = 'compressed_videos'

    if not os.path.exists(input_folder):
        print(f"Input folder '{input_folder}' not found. Please create it and add videos.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    processed_files = 0
    failed_files = 0
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.mp4'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_name = f"{os.path.splitext(filename)[0]}_compressed.mp4"
            output_file_path = os.path.join(output_folder, output_file_name)
            
            if compress_video(input_file_path, output_file_path):
                processed_files += 1
            else:
                failed_files += 1
            print("---")

    print(f"Video compression complete.")
    print(f"Successfully processed: {processed_files} files.")
    print(f"Failed to process: {failed_files} files.")
    if failed_files > 0:
        print("Check logs above for error details for failed files.")

if __name__ == '__main__':
    main()