from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
NO_TRANSCRIPT_ERROR=1

app = Flask(__name__)

#send verbose errors
#send back json
#get video transcript text

@app.route('/<video_id>')
def model(video_id):
	#if not request.view_args.get('video_id'):
	try:
		YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
	except YouTubeTranscriptApi.CouldNotRetrieveTranscript:
		return jsonify({'error':{'code':NO_TRANSCRIPT_ERROR, 'message':'transcript could not be retrieved'}})
	
	return jsonify({"success":True})


if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
