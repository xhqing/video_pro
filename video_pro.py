from moviepy.editor import *
from moviepy.audio.fx import all
from pydub import AudioSegment

def video_cut(input_name, start_time, end_time, output_name):
    """
        功能：视频剪辑(暂时只支持有声视频的剪辑)

        input_name: mp4文件名，例如：'西游记.mp4'
        start_time: 剪辑起始时间，单位：秒
        end_time: 剪辑终止时间，单位：秒
        start_time到end_time之间的视频片段内容为你想要保留的内容
        output_name: 剪辑完成后的视频片段的保存文件名称，如：'西游记-01.mp4'

        示例：
        video_cut('西游记.mp4', 4, 10, '西游记-01.mp4')
    """
    VideoFileClip(input_name).subclip(start_time, end_time).write_videofile(output_name)

def video_concatenate(input_list, output_name):
    """
        功能：视频文件合并

        input_list: mp4文件名的列表，如：['西游记.mp4','西游记-01.mp4']
        output_name: 合并完成后的视频的保存文件名称，如：'西游记-concatenate.mp4'

        示例：
        video_concatenate(['西游记.mp4','西游记-01.mp4'], '西游记-concatenate.mp4')
    """
    concatenate_videoclips(list(map(VideoFileClip, input_list))).to_videofile(output_name)

def add_audio(input_audio, input_video, output_video):
    """
        功能：给视频添加音频

        input_audio: 要添加的音频文件，如：'xxx.mp3' 
        input_video: 要添加音频的视频文件，如：'xxx.mp4'
        output_video: 最终保存的视频文件，如：'xxxx.mp4'

        示例：
        add_audio('xxx.mp3', 'xxx.mp4', 'xxxx.mp4')

        注意：
            1、如果要添加音频的视频时间长度比音频时间长度长，那么添加音频后，超出音频时间长度之后的视频将是无声的。
            2、如果要添加音频的视频时间长度比音频时间长度短，那么添加音频后，视频将定格在最后一帧画面，音频继续播放。
    """
    audio = AudioFileClip(input_audio)
    video = VideoFileClip(input_video)
    video.set_audio(audio).write_videofile(output_video)

def from_video_get_audio(input_video, output_audio):
    """
        功能：获取视频的背景音乐

        input_video: 要获取背景音乐的视频文件，如：'xx.mp4'
        output_audio: 获取到的背景音乐音频文件——你要保存的名字，如：'xxx.mp3'

        示例：
        from_video_get_audio('xx.mp4', 'xxx.mp3')
    """
    
    video = VideoFileClip(input_video)
    audio = video.audio
    try:
        audio.write_audiofile(output_audio)
    except AttributeError:
        print('您输入的视频是无声的，请输入有声视频，谢谢！')

def audio_segment(input_audio, start_time, stop_time, output_audio):
    """
        功能：音频分割——获取你想要的音频片段
    
        input_audio: 输入的音频文件，如：'xxx.mp3'
        start_time: 你想要的音频片段的起始时间，如：'0:00'代表0分0秒
        stop_time: 你想要的音频片段的终止时间，如：'0:42'代表0分42秒
        output_audio: 你想要的音频片段——保存文件名， 如：'my_audio.mp3'
    """
    audio = AudioSegment.from_mp3(input_audio)
    start_time = (int(start_time.split(':')[0])*60 + int(start_time.split(':')[1]))*1000
    stop_time = (int(stop_time.split(':')[0])*60 + int(stop_time.split(':')[1]))*1000
    audio[start_time:stop_time].export(output_audio, format="mp3")

def audio_concatenate(input_list, output_name):
    """
        功能：音频文件合并

        input_list: mp3文件名的列表，如：['西游记.mp3','西游记-01.mp3']
        output_name: 合并完成后的音频的保存文件名称，如：'西游记-concatenate.mp3'

        示例：
        audio_concatenate(['西游记.mp3','西游记-01.mp3'], '西游记-concatenate.mp3')
    """
    from tqdm import tqdm 
    audio_files = list(map(lambda x: open(x, 'rb'), input_list))
    out = open(output_name, 'wb')
    for audio_file in tqdm(audio_files, total=len(audio_files)):
        out.write(audio_file.read())
        audio_file.close()
    out.flush()
    out.close()

def extract_video_without_audio(input_video, output_video):
    """
        功能：删掉视频中的音频，提取无声视频

        input_video: 输入的有声视频，如：'with_audio.mp4'
        output_video: 删除音频后的视频，如：'without_audio.mp4'

        示例：
        extract_video_without_audio('with_audio.mp4', 'without_audio.mp4')
    """
    VideoFileClip(input_video).without_audio().write_videofile(output_video)

def video_acceleration(input_video, output_video, n=2):
    """
        功能：视频加速

        input_video: 输入视频文件，如：'xxx.mp4'
        n: 加速倍速，默认值为2(加速2倍) (测试n为2、4、8没有问题)
        output_video: 加速后的视频文件——你想保存的文件名，如：'v_acc.mp4'

        示例：
        video_acceleration('xxx.mp4', 'v_acc.mp4', n=2)
    """
    if n < 1:
        print('请输入大于等于1的加速倍数！')
        return 0
    import os
    if VideoFileClip(input_video).audio is None:
        os.system(f'ffmpeg -i {input_video} -r 16 -filter:v "setpts=(1/{n})*PTS" {output_video}')
    else:
        os.system(f'ffmpeg -i {input_video} -filter_complex "[0:v]setpts={1/n}*PTS[v];[0:a]atempo={n}[a]" -map "[v]" -map "[a]" {output_video}')

def audio_acceleration(input_audio, output_audio, n=2):
    """
        功能：音频加速

        input_audio: 输入的音频文件，如：'xxx.mp3'
        output_audio: 输出的音频文件，你的保存命名，如：'yyy.mp3'
        n: 加速倍数，默认值2 (测试n为2、4、8没有问题)

        示例：
        audio_acceleration('xxx.mp3', 'yyy.mp3', n=4)
    """
    if n < 1:
        print('请输入大于等于1的加速倍数！')
        return 0
    from ffmpeg import audio
    audio.a_speed(input_audio, str(n), output_audio)

def audio_slowdown(input_audio, output_audio, n=0.5):
    """
        功能：音频减速

        input_audio: 输入的音频文件，如：'xxx.mp3'
        output_audio: 输出的音频文件，你的保存命名，如：'yyy.mp3'
        n: 减速分数，默认值0.5(表示减速为原来的一半) 取值范围[0.5, 1] (测试n为0.5、0.75、1没有问题)

        示例：
        audio_slowdown('xxx.mp3', 'yyy.mp3', n=0.75)
    """
    if n > 1 or n < 0.5:
        print('请输入区间在[0.5, 1]的数！')
        return 0
    from ffmpeg import audio
    audio.a_speed(input_audio, str(n), output_audio)

def video_slowdown(input_video, output_video, n=0.5):
    """
        功能：视频减速

        input_video: 输入视频文件，如：'xxx.mp4'
        n: 减速分数，默认值为0.5(减速一半) (有声视频测试n为0.5、0.75、1没有问题，无声视频测试增加0.1、0.2、0.4没有问题)
        output_video: 减速后的视频文件——你想保存的文件名，如：'v_sl.mp4'

        示例：
        video_slowdown('xxx.mp4', 'v_sl.mp4', n=0.5)
    """
    import os
    if VideoFileClip(input_video).audio is None:
        if n > 1 or n <= 0:
            print('请输入在区间(0, 1]的数！')
            return 0
        os.system(f'ffmpeg -i {input_video} -r 16 -filter:v "setpts=(1/{n})*PTS" {output_video}')
    else:
        if n < 0.5 or n > 1:
            print('请输入在区间[0.5, 1]的数！')
            return 0 
        os.system(f'ffmpeg -i {input_video} -filter_complex "[0:v]setpts={1/n}*PTS[v];[0:a]atempo={n}[a]" -map "[v]" -map "[a]" {output_video}')

if __name__ == '__main__':
    """
        1、以上所有函数采用mp4和mp3的视频文件和音频文件亲测可用，未测试过除mp4、mp3以外的视频文件和音频文件，理论上其他格式的视频和音频文件也可用。
        2、开发测试环境：Windows 10、Python 3.6.8
    """
    """=============================
        只需修改以下内容即可直接使用
    ============================="""
    video_cut('Elon.mp4', 0.5, 14*60+6, 'out.mp4')
    # video_concatenate(['西游记.mp4','西游记-01.mp4'], '西游记-concatenate.mp4')
    # add_audio('ar_audio.mp3', 'out.mp4', 'out_with_audio.mp4')
    # from_video_get_audio('游戏王AR软件.mp4', 'AR.mp3')
    # audio_segment('AR.mp3', '0:00', '0:58', 'ar_audio.mp3')
    # audio_concatenate(['my_audio.mp3','ts.mp3'], 'concatenate.mp3')
    # audio_acceleration('my_audio.mp3', 'acc_audio.mp3', n=1)
    # video_acceleration('WeChat.mp4', 'v_acc.mp4', n=2)
    # extract_video_without_audio('show.mp4', 'without_audio.mp4')
    # audio_slowdown('my_audio.mp3', 'yyy.mp3', n=1)
    # video_slowdown('show.mp4', 'v_sl.mp4', n=1)


