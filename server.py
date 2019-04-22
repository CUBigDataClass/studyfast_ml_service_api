from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from trainModel import partition

NO_TRANSCRIPT_ERROR=1
INVALID_PARAMS_ERROR=2
VIDEO_PROCESSING_ERROR=3

app = Flask(__name__)

@app.route('/video/<video_id>')
def model(video_id):
	search_param = request.args.get('search')
	if not search_param:
		app.logger.info("request failed without search parameter")
		return jsonify({'error':{'code': INVALID_PARAMS_ERROR, 'message':'search parameter required on request'}})
	try:
		data = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
	except YouTubeTranscriptApi.CouldNotRetrieveTranscript:
		app.logger.exception(f"request failed on transcript lookup, video_id={video_id}")
		return jsonify({'error':{'code': NO_TRANSCRIPT_ERROR, 'message':'transcript could not be retrieved'}})
	try:
		buckets = partition(data, search_param)
	except Exception:
		app.logger.exception(f"video processing failed with exception")
		return jsonify({'error':{'code': VIDEO_PROCESSING_ERROR, 'message':'error processing video'}})
	payload = {
		"video_id": video_id,
		"search": search_param,
		"buckets": buckets
	}
	return jsonify(payload)


if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
