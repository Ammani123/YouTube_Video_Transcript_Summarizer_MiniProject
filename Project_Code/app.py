from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        if youtube_url:
            try:
                # Get the transcript for the YouTube video
                video_id = get_video_id(youtube_url)
                transcript = get_transcript_summary(video_id)

                # Translate the summary into Telugu
                translated_summary = translate_to_telugu(transcript)

                return render_template('index.html', youtube_url=youtube_url, transcript=transcript, translated_summary=translated_summary)

            except Exception as e:
                error_message = "Error: " + str(e)
                return render_template('index.html', error_message=error_message)
        
    return render_template('index.html')

def get_video_id(youtube_url):
    #video_id = None
    if 'youtube.com' in youtube_url:
        video_id = youtube_url.split('v=')[1]
    elif 'youtu.be' in youtube_url:
        video_id = youtube_url.split('/')[-1]
    return video_id

def get_transcript_summary(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    if transcript:
        summary = ' '.join([item['text'] for item in transcript])
        return summary
    else:
        raise Exception("Transcript not found for the provided YouTube video.")

def translate_to_telugu(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='te')
    return translated_text.text


'''def translate_to_hindi(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='hi')
    return translated_text.text'''

if __name__ == '__main__':
    app.run(debug=True)