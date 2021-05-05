from pytube import YouTube
from pytube.cli import on_progress
import ffmpeg
import os
import subprocess
import re
import shutil


def draw():
    # This Function clears and prints below TEXT

    os.system('cls')
    print("""
    --------------------------------------------
    |            YOUTUBE DOWNLOADER            |
    --------------------------------------------
    [ Welcome to Youtube Downloader ]
    [ website : https://ViKi-R.github.io ] 
    [ Author : ViKi-R ] 
    """)


def video_details(yt):
    # This function outputs the Title, Length, 
    # Description if present, Number of views,
    # Rating of the Youtube Video

    minutes = int(yt.length / 60)
    seconds = int(yt.length % 60)
    if seconds < 10:
        seconds = str(f'0{seconds}')
    print("-"*80)
    print(f"Title: {yt.title}")
    print(f"Video Length: {minutes}:{seconds} ")
    if yt.description == True:
        print(f"Description: {yt.description}")
    print(f"Views: {yt.views:,}")
    print(f"Ratings: {yt.rating:.2f}")
    print("-"*80)


def choose_audio_video():
    # This function gets input from user for 
    # downloading Video or audio

    option_list = ["A", "V", "a", "v"]
    print("Download Audio(a) or Video(v):")
    while True:
        option = str(input("Choose [a / v] >> "))
        if option in option_list:
            break
        else:
            print('Please Enter Valid Option...')
            continue
    print("-"*80)            
    return option  


def download_audio(yt, youtube_title):
    # This function downloads audio from Youtube in MP4 fromat
 
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    audio_save_path = f'{desktop}\\YTMusic\\music\\'
    acodec = 'mp4a.40.2'
    audio = str(yt.streams.filter(only_audio=True, audio_codec=acodec))
    aitag = audio[16:19]
    ad = yt.streams.get_by_itag(aitag)
    audio_name = re.sub(r'[^a-zA-Z0-9 ]', '', youtube_title)
    print(f'Now Downloading Audio : {youtube_title} ...')
    ad.download(audio_save_path, filename=audio_name)
    print()


def convert_audio(aname):
    # This function converts Audio MP4 fromat to MP3 fromat

    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    aname = re.sub(r'[^a-zA-Z0-9 ]', '', aname)
    audio_file = f"{desktop}\\YTMusic\\music\\{aname}.mp4"
    final_audio_file = f"{desktop}\\YTMusic\\{aname}.mp3"
    print('-'*80)
    print("Please Wait...")
    subprocess.call(['ffmpeg', '-i', audio_file, final_audio_file, '-loglevel', 'fatal'])
    print('Done!')
    delete_audio_folder = f'{desktop}\\YTMusic\\music'
    shutil.rmtree(delete_audio_folder)


def replace_format(video_quality):
    # This Function corrects the format of the youtube video

    video_quality = video_quality.replace('720p', ' 720p')
    video_quality = video_quality.replace('480p', ' 480p')
    video_quality = video_quality.replace('360p', ' 360p')
    video_quality = video_quality.replace('240p', ' 240p')
    video_quality = video_quality.replace('144p', ' 144p')
    video_quality = video_quality.replace('webm', 'wem')
    video_quality_list = video_quality.split('>, ')
    return video_quality_list


def remove_av01codec(video_quality_list):
    # This function removes the AV01 video Codec as windows do not have AV01 codec built in

    avcodec = ['av01012M08', 'av01008M08', 'av01005M08', 'av01004M08', 'av01001M08', 'av01000M08']
    avcodec_start = 61      
    avcodec_end = 71     
    vpcodec_end = 64 
    for i in video_quality_list:
        if i[avcodec_start:avcodec_end] in avcodec:
            video_quality_list.remove(i)

    for i in video_quality_list:
        if i[avcodec_start:vpcodec_end] == 'vp9':
            video_quality_list.remove(i)

    return video_quality_list


def remove_vpcodec(video_quality_list):
    # This function removes the VP92 video Codec

    avcodec_start = 61      
    vpcodec_end = 64 
    res_none_start = 38 
    res_none_end = 42 
    for i in video_quality_list:
        if i[avcodec_start:vpcodec_end] != 'vp9':
            video_quality_list.remove(i)

    for i in video_quality_list:
        if i[avcodec_start:65] == 'vp92':
            video_quality_list.remove(i)

    for i in video_quality_list:
        if i[res_none_start:res_none_end] == 'None':
            video_quality_list.remove(i)    

    return video_quality_list


def choose_video_quality(yt):
    # This function outputs Available Video Quality and
    # get input from user of video quality

    res_start = 38
    res_end = 42
    yt_itag_list = []

    video_quality = str(yt.streams.filter(only_video=True))
    video_quality = re.sub(r'[^a-zA-Z0-9=>, ]', '', video_quality)
    video_quality_list = replace_format(video_quality)

    if video_quality[res_start:res_end] >= '2160p':
        video_quality_list = remove_vpcodec(video_quality_list)
    else:
        video_quality_list = remove_av01codec(video_quality_list)

    print("Available Video quality:")
    print(f'\nITAG-ID   QUALITY')
    print("-"*20)
    for i in video_quality_list:
        yt_itag_list.append(i[12:15])
        print(f'{i[12:15]}\t  {i[38:43]}')
    print("-"*20)
    print('Enter the ITAG ID to download preferred Video Quality:')
    while True:
        yt_itag = input('ITAG ID >> ')
        if yt_itag in yt_itag_list:
            break
        else:
            print('Please Enter Valid ITAG ID...')
            continue        
    return yt_itag


def download_audio_for_video(yt, youtube_title):
    # This function downloads audio from Youtube in MP4 fromat for Video

    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    audio_save_path = f'{desktop}\\YTVideo\\music'
    acodec = 'mp4a.40.2'
    audio = str(yt.streams.filter(only_audio=True, audio_codec=acodec))
    aitag = audio[16:19]
    audio_downloader = yt.streams.get_by_itag(aitag)
    audio_name = re.sub(r'[^a-zA-Z0-9 ]', '', youtube_title)
    audio_name = f'{audio_name}'
    audio_downloader.download(audio_save_path, filename=audio_name)
    print()


def combine_av(vname):
    # This function is post processing of video and audio it combines video audio downloaded
    
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    vname = re.sub(r'[^a-zA-Z0-9 ]', '', vname)
    delete_video_folder = f'{desktop}\\YTVideo\\video'
    delete_audio_folder = f'{desktop}\\YTVideo\\music'
    file_list = os.listdir(delete_video_folder)
    for vfile in file_list:
        if vname:
            vid_name = vfile
    video_file = f"{desktop}\\YTVideo\\video\\{vid_name}"
    audio_file = f"{desktop}\\YTVideo\\music\\{vname}.mp4"
    final_video_file = f"{desktop}\\YTVideo\\{vname}.mkv"
    print('Please Wait...')
    subprocess.call(['ffmpeg', '-i', video_file, '-i', audio_file, '-c', 'copy', final_video_file, '-loglevel', 'fatal'])
    print('Done!')
    shutil.rmtree(delete_video_folder)
    shutil.rmtree(delete_audio_folder)


def download_video(yt, yt_itag):
    # This function Downloads Video from Youtube with preffered video quality

    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    video_save_path = f'{desktop}\\YTVideo\\video'
    video_name = re.sub(r'[^a-zA-Z0-9 ]', '', yt.title)
    print("-"*80)
    download_audio_for_video(yt, video_name)
    video_downloader = yt.streams.get_by_itag(yt_itag)
    print(f'Now Downloading Video : {yt.title} ...')
    video_downloader.download(video_save_path, filename=video_name)
    print()
    combine_av(yt.title)


def download_again():
    # This function ask for the user to Download any video or audio again

    os.system('cls')
    print("-"*80)
    print('Do You want to Download Another Video/Audio Again [Y / n]:')
    download_again = str(input('>> '))
    if download_again.lower() == 'y':
        main()
    else:
        print()
        print('Thanks For using Come back again... ')
        print("-"*80)
        input("Press any key to exit... ")
        os.system('cls')


def main():
    # Main Function
    
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    draw()
    print("-"*80)
    url = input('YouTube Video URL(Link): ')
    yt = YouTube(url, on_progress_callback=on_progress)
    video_details(yt)
    title_name = re.sub(r'[^a-zA-Z0-9 ]', '', yt.title)
    opted = choose_audio_video()

    if opted.lower() == "a":
        download_audio(yt, yt.title)
        convert_audio(yt.title)
        print()
        print('>> Download Completed... ')
        print("-"*80)
        print(f'Audio Path: {desktop}\\YTMusic\\{title_name}')
        print("-"*80)
        input("Press any key to continue... ")

    elif opted.lower() == "v":
        yt_itag = choose_video_quality(yt)
        download_video(yt, yt_itag)
        print()
        print('>> Download Completed... ')
        print("-"*80)
        print(f'Video Path: {desktop}\\YTVideo\\{title_name}')
        print("-"*80)
        input("Press any key to continue... ")

    download_again()


if __name__ == "__main__":
    main()