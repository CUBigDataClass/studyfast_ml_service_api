from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from trainModel import partition

NO_TRANSCRIPT_ERROR=1
INVALID_PARAMS_ERROR=2
VIDEO_PROCESSING_ERROR=3

app = Flask(__name__)

@app.route('/video/<video_id>')
def model(video_id):
	search = request.args.get('search')
	if not search:
		return jsonify({'error':{'code': INVALID_PARAMS_ERROR, 'message':'search parameter required on request'}})
	try:
		data = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
	except YouTubeTranscriptApi.CouldNotRetrieveTranscript:
		return jsonify({'error':{'code': NO_TRANSCRIPT_ERROR, 'message':'transcript could not be retrieved'}})
	try:
		buckets = partition(data, search)
	except Exception:
		return jsonify({'error':{'code': VIDEO_PROCESSING_ERROR, 'message':'error processing video'}})
	payload = {
		"video_id": video_id,
		"search": search,
		"buckets": buckets
	}
	return jsonify(payload)


if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
