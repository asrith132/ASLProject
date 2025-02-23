import json
import os
import yt_dlp

def extract_video_info(file_path, target_word):
    result = []
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)  # Load the entire JSON file
            for entry in data:
                if entry.get('clean_text', '').lower() == target_word.lower():
                    result.append([
                        entry.get('url', ''),
                        entry.get('start_time', 0),
                        entry.get('end_time', 0)
                    ])
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    return result

def download_video(url, start_time, end_time, output_path):
    ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': output_path,
    'ffmpeg_location': r"C:\ytdl\ffmpeg-N-118521-gd1ed5c06e3-win64-gpl\bin",  
    'postprocessors': [{
        'key': 'FFmpegVideoRemuxer',
        'preferedformat': 'mp4',
    }],
    'download_ranges': lambda info, ydl: [{'start_time': start_time, 'end_time': end_time}],
}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Successfully downloaded: {output_path}")
    except Exception as e:
        print(f"Failed to download {url}: {str(e)}")

def main():
    json_file = "C:\\Users\\rohan\\Downloads\\MS-ASL\\MS-ASL\\MSASL_train.json"  # Replace with your JSON file path
    target_word = "no"   # Replace with your target word
    output_directory = os.path.join(os.getcwd(), "videos")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    video_segments = extract_video_info(json_file, target_word)

    for i, segment in enumerate(video_segments):
        url, start_time, end_time = segment
        output_filename = f"{target_word}_{i+1}.mp3"
        output_path = os.path.join(output_directory, output_filename)

        print(f"Attempting to download segment {i+1} from {url}")
        download_video(url, start_time, end_time, output_path)

if __name__ == "__main__":
    main()