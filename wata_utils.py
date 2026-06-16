import os
import re
import glob
import time
import shutil
import datetime
import yt_dlp
import json
import requests
import pickle
import winsound
import pyautogui
import subprocess
import pandas as pd
import win32clipboard
from bs4 import BeautifulSoup
from pythumb import Thumbnail
from datetime import datetime, timedelta

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# Python Volume Adjustment
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

sessions = AudioUtilities.GetAllSessions()
python_process = os.path.basename(os.sys.executable)
for session in sessions:
    if session.Process and session.Process.name() == python_process:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume.SetMasterVolume(0.1, None)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# Global Variables
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

current_year = 2026
thumbnails_path = r'E:\Vids\nl clips\thumbnail resources\thumbnail faces'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# Alarm
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

def task_complete_alarm():
    winsound.PlaySound(r".\resources\tuturu.wav",winsound.SND_ASYNC)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# Premiere Pro
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

def daily_highlights_rename(date):
    time.sleep(2)
    x_pos,y_pos = pyautogui.position()

    pyautogui.click(x_pos,y_pos)
    time.sleep(0.5)
    pyautogui.click(x_pos,y_pos)
    time.sleep(0.5)
    pyautogui.write('{} - 1.'.format(date))

    for i in range(1,20):
        time.sleep(0.1)
        pyautogui.press('enter')
        pyautogui.write('{} - {}.'.format(date,i+1))

    time.sleep(0.1)
    pyautogui.press('enter')
    pyautogui.write('{} - {}'.format(date,'bandle'))

    time.sleep(0.1)
    pyautogui.press('enter')
    pyautogui.write('{} - {}'.format(date,'fantasy football'))

    time.sleep(0.1)
    pyautogui.press('enter')
    pyautogui.write('{} - {}'.format(date,'chicken jockey'))

    pyautogui.press('enter')
    task_complete_alarm()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# YouTube Download
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

def get_playlist_video_urls(playlist_url):
    ydl_opts = {
        'no_warnings': True,
        'quiet': True,
        'extract_flat': 'in_playlist',  # Don't download videos
        'force_generic_extractor': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        entries = info.get('entries', [])
        return [entry['url'] for entry in entries]

def download_youtube_video(URL,mute=False):
    youtube_dl_options = {'no_warnings': True,"quiet": "True",'cookiesfrombrowser': ('firefox',)}
    with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download(URL)
    list_of_files = glob.glob('*')
    latest_file = max([i for i in list_of_files if ((".mp4" in i) or (".webm" in i) or (".mkv" in i)) ], key=os.path.getctime)
    handbrake_command = [r".\resources\HandBrakeCLI.exe","--preset-import-file",r".\resources\presets.json","-Z","statcher convert","-i",latest_file,"-o","downloads/"+latest_file[:-4]+"conv"+".mp4"]
    subprocess.run(handbrake_command)
    os.remove(latest_file)

    if not mute:
        task_complete_alarm()

def download_youtube_video_clipboard():
    win32clipboard.OpenClipboard()
    URL = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    youtube_dl_options = {'no_warnings': True,"quiet": "True"}
    with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download(URL)
    list_of_files = glob.glob('*')
    latest_file = max([i for i in list_of_files if ((".mp4" in i) or (".webm" in i) or (".mkv" in i)) ], key=os.path.getctime)
    handbrake_command = [r".\resources\HandBrakeCLI.exe","--preset-import-file",r".\resources\presets.json","-Z","statcher convert","-i",latest_file,"-o","downloads/"+latest_file[:-4]+"conv"+".mp4"]
    subprocess.run(handbrake_command)
    os.remove(latest_file)

    task_complete_alarm()

def download_youtube_audio_clipboard():
    win32clipboard.OpenClipboard()
    URL = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    youtube_dl_options = {
        'format': 'bestaudio/best',      # best audio stream only
        'outtmpl': f'downloads/%(title)s.%(ext)s',  # save to downloads folder
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}
        ],
        'quiet': True,
        'no_warnings': True
    }
    with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download(URL)
    
    task_complete_alarm()

def download_youtube_audio(URL,mute=False):
    youtube_dl_options = {
        'format': 'bestaudio/best',      # best audio stream only
        'outtmpl': f'downloads/%(title)s.%(ext)s',  # save to downloads folder
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}
        ],
        'quiet': True,
        'no_warnings': True
    }
    with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download(URL)
    if not mute:
        task_complete_alarm()

def calc_time(time1,time2):
    truetime1 = (int(time1.split(":")[0])*60*60)+(int(time1.split(":")[1])*60)+int(time1.split(":")[2])
    truetime2 = (int(time2.split(":")[0])*60*60)+(int(time2.split(":")[1])*60)+int(time2.split(":")[2])
    return truetime1, truetime2-truetime1

def download_youtube_video_partial(URL,time1,time2):
    youtube_dl_options= {'no_warnings': True,"quiet": "True"}
    with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download(URL)

    truetime1,truetime2_handbrake = calc_time(time1,time2)
    list_of_files = glob.glob('*')
    latest_file = max([i for i in list_of_files if ((".mp4" in i) or (".webm" in i) or (".mkv" in i)) ], key=os.path.getctime)
    handbrake_command = [r".\resources\HandBrakeCLI.exe","--preset-import-file",r".\resources\presets.json","-Z","statcher convert","--start-at","duration:{}".format(truetime1),"--stop-at","duration:{}".format(truetime2_handbrake),"-i",latest_file,"-o","downloads/"+latest_file[:-4]+"conv"+".mp4"]
    subprocess.run(handbrake_command)
    os.remove(latest_file)
    task_complete_alarm()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# VOD Download
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

def download_vod(vod_id):
    subprocess.run('twitch-dl download https://www.twitch.tv/videos/{0} -q source '.format(id)+'-f mp4 -o "downloads/{0}.mp4'.format(vod_id))
    task_complete_alarm()

def download_vod_by_channel(channel_name):
    id = int(re.findall(r'Video \d+\.?\d*',str(subprocess.run('twitch-dl videos {0}'.format(channel_name),capture_output=True).stdout))[0].split(" ")[1])
    subprocess.run('twitch-dl download https://www.twitch.tv/videos/{0} -q source '.format(id)+'-f mp4 -o "downloads/{0}.mp4'.format(id,channel_name+'_'+str(id)))
    task_complete_alarm()

def get_vod_id_by_channel(channel_name):
    id = int(re.findall(r'Video \d+\.?\d*',str(subprocess.run('twitch-dl videos {0}'.format(channel_name),capture_output=True).stdout))[0].split(" ")[1])
    print(id)

def download_vod_northernlion():
    id = int(re.findall(r'Video \d+\.?\d*',str(subprocess.run('twitch-dl videos northernlion',capture_output=True).stdout))[0].split(" ")[1])
    subprocess.run('twitch-dl download https://www.twitch.tv/videos/{0} -q source '.format(id)+'-f mp4 -o "downloads/{0}.mp4'.format(id))
    time.sleep(2)
    subprocess.run('ffmpeg -i "downloads/{0}.mp4" -vn -c:a libmp3lame -b:a 192k "downloads/{0}.mp3"'.format(id))
    task_complete_alarm()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# Chat File Render
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

def refresh_vod_summaries():
    resp = requests.get("https://clickityclack.co.uk/content/vod-summaries.json")
    with open("resources/vod-summaries.json", "w", encoding="utf-8") as my_file:
            my_file.write(resp.text)

def download_chat_file(vod_id):
    resp = requests.get("https://clickityclack.co.uk/content/videos/{0}.json".format(vod_id))
    with open("chat_vod_download/{0}.json".format(vod_id), "w", encoding="utf-8") as my_file:
        my_file.write(resp.text)
    
def render_chat_file_partial(vod_id,start,end,file_name):
    subprocess.run(r".\resources\TwitchDownloaderCLI.exe chatrender -i chat_vod_download/{0}.json -h 1500 -w 400 --background-color #00FFFFFF -b {1} -e {2} --outline True --outline-size 8 -f Regan --font-size 24 --generate-mask True -o chat_vod_download/b{3}.mp4".format(vod_id,start,end,file_name))

def render_chat_file(vod_id,file_name):
    subprocess.run(r".\resources\TwitchDownloaderCLI.exe chatrender -i chat_vod_download/{0}.json -h 1500 -w 400 --background-color #00FFFFFF --outline True --outline-size 8 -f Regan --font-size 24 --generate-mask True -o chat_vod_download/b{1}.mp4".format(vod_id,file_name))

def download_main_stream_chat_file(date):
    with open(r".\resources\vod-summaries.json", 'r', encoding="cp866") as input_file:
        data = input_file.read()
        structure = json.loads(data)

    id = ""
    duration = 0

    for chat in structure:
        if date in chat["created_at"]:
            if "h" in chat["duration"]:
                if int(chat["duration"].split("h")[0]) > duration:
                    id = chat["id"]
                    duration = int(chat["duration"].split("h")[0])
    
    download_chat_file(id)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# File Management
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

def rename_bnb(root_dir):
    for current_dir, subdirs, files in os.walk(root_dir):
        if os.path.basename(current_dir) == "clips":
            parent_dir = os.path.basename(os.path.dirname(current_dir))
            for filename in files:
                if '.mp4' in filename:
                    old_path = os.path.join(current_dir, filename)
                    ext = os.path.splitext(filename)[1]
                    new_filename = f"{parent_dir}{ext}"
                    new_path = os.path.join(current_dir, new_filename)

                    if old_path == new_path:
                        continue

                    if os.path.exists(new_path):
                        continue

                    os.rename(old_path, new_path)
    task_complete_alarm()

def weekly_startfile_gen(main_path):
    for i in range(5):
        date = (datetime.today()+ timedelta(days=i)).strftime("%m-%d-%Y")
        date_path = os.path.join(main_path,date)
        template_path = os.path.join(main_path,'date_temp')
        shutil.copytree(template_path,date_path)
        os.rename(os.path.join(date_path,'proj','all_projects_template.prproj'), os.path.join(date_path,'proj',date.replace("-","")+'.prproj'))
        task_complete_alarm()

def weekly_cleanup(main_path):
    for f in os.listdir(main_path):
        folder_path = os.path.join(main_path,f)
        if (len(re.findall(r'\d\d-\d\d-\d\d\d\d',f))>0) and (str(current_year) in f):
            try:
                shutil.rmtree(os.path.join(folder_path,'source'))
            except:
                pass
            for vid in os.listdir(os.path.join(folder_path,'clips')):
                if ('nl_sequence' not in vid) and (f not in vid):
                    os.remove(os.path.join(os.path.join(folder_path,'clips'),vid))
                else:
                    os.rename(os.path.join(os.path.join(folder_path,'clips'),vid), os.path.join(os.path.join(folder_path,'clips'),f+'.mp4'))
    task_complete_alarm()


def refresh_youtube_thumbnails():

    playlist_url = 'https://www.youtube.com/playlist?list=UU3tNpTOHsTnkmbwztCs30sA'

    video_urls = get_playlist_video_urls(playlist_url)

    done = ['https://www.youtube.com/watch?v='+ i[:-4] for i in os.listdir(thumbnails_path)] + ['https://www.youtube.com/watch?v='+ i[:-4] for i in os.listdir(r'E:\Vids\nl clips\thumbnail resources\shorts')]

    with open(r".\resources\finished_thumbs.pkl", 'rb') as f:
        old_done = pickle.load(f)[:20000]

    done += old_done

    video_urls = list(set(video_urls) - set(done))

    for video in video_urls:
        t = Thumbnail(video)
        t.fetch()
        try:
            t.save(thumbnails_path)
        except FileExistsError:
            continue

    task_complete_alarm()


# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# File Readers
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

def master_chat_file_reader(search_term):
    with open(r".\resources\vod-summaries.json", 'r', encoding="cp866") as input_file:
        data = input_file.read()
        structure = json.loads(data)

    titles = []
    ids = []
    durations = []
    for chat in structure:
        if search_term in chat['title'].lower():
            titles.append(chat["title"])
            ids.append(chat["id"])
            durations.append(chat["duration"])

    df= pd.DataFrame()
    df["titles"] = titles
    df["ids"] = ids
    df["durations"] = durations
    df.to_csv("titles.csv")

def generate_memberships():
    df = pd.read_csv(r".\input_files\members.csv")

    names = []

    for link in df['Link to profile'].values:
        if not pd.isna(link):
            a = requests.get(link)
            if len(re.findall(r'<title>(.*)</title>',a.text)) == 0:
                print(link)
            else:
                name = re.findall(r'<title>(.*)</title>',a.text)[0][:-10]
                if name != '':
                    names.append(name)
    
    names.sort(key=lambda s: len(s))
    for i in names:
        print(i.replace("&#39;","'"))

def adjust_markers(seconds_adjust):
    markers = open(r'.\input_files\markers.txt', 'r').readlines()
    for marker in markers:
        time = marker[:-1].split(" ")[0]
        marker = ' '.join(marker[:-1].split(" ")[1:])

        adjusted_time = datetime.strptime(time, "%H:%M:%S") + timedelta(seconds=seconds_adjust)
        print(f"{adjusted_time.strftime("%H:%M:%S")} {marker}")


# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# Caption Payment
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

def monthly_caption_summary(playlist_url):

    urls = get_playlist_video_urls(playlist_url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    titles = []
    durations = []

    for url in urls:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("meta", property="og:title")
        title = title_tag["content"] if title_tag else "Unknown Title"

        duration_tag = soup.find("meta", itemprop="duration")
        if duration_tag:
            # Format looks like "PT3M33S" (ISO 8601)
            iso_str = duration_tag["content"]
            # Quick regex trick to extract numbers for minutes/seconds
            numbers = [int(s) for s in re.findall(r"\d+", iso_str)]
            if len(numbers) == 3:  # Hours, Minutes, Seconds
                duration = f"{numbers[0]:02d}:{numbers[1]:02d}:{numbers[2]:02d}"
            elif len(numbers) == 2:  # Minutes, Seconds
                duration = f"{numbers[0]:02d}:{numbers[1]:02d}:00"
            elif len(numbers) == 1:  # Only Seconds
                duration = f"00:{numbers[0]:02d}:00"
            else:
                duration = "00:00"
        else:
            duration = "Unknown Length"
        
        titles.append(title)
        durations.append(duration)


    df = pd.DataFrame(columns=["title","duration"])
    df["title"] = titles
    df["duration"] = durations
    return df