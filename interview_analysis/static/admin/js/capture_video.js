/* 
What this needs
(1) something to capture audio
(2) something to capture video
(3) something to start recording
(4) something to stop recording
(5) something to send the recordings
*/

// before everything
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
var constraints = {audio: true, video: true};
var video = document.querySelector("video");
var isFirefox = !!navigator.mozGetUserMedia;
var jsQuestion;
//

/*
When a user clicks "record" this function calls getUserMedia, the callback of which initiates 
the process of collecting the audio and video data.
*/
function record(mediaStream){
  navigator.getUserMedia(constraints, successCallback, errorCallback);
}
document.getElementById("record").onclick = record;

/*
The successCallback is called when getUserMedia is called successfully. This function goes 
through the process of actually collecting the audio and video.
*/
function successCallback(mediaStream){
  playVideo(mediaStream);
  var options_audio = {'sample-rate': 44100};
  var recordAudioRTC = RecordRTC(mediaStream, options_audio);
  var options_video = {type: 'video'};
  var recordVideoRTC = RecordRTC(mediaStream, options_video);
  recordAudioRTC.startRecording();
  recordVideoRTC.startRecording();
  /*
  stop stops the recording and sends it to the server. It must be inside successCallback
  because it needs to use recordAudioRTC and recordVideoRTC.
  */
  function stop(mediaElement){
    // problem: the console logs recordAudioRTC and the blob exists in it, but when you log the blob it fdoesnt exist
    
    // var audioBlob = recordAudioRTC.getBlob();
    video.pause();
    console.log("before stop");
    recordAudioRTC.stopRecording(function(){
      recordVideoRTC.stopRecording(function(){
        console.log("after stop");
        audioBlob = recordAudioRTC.getBlob();
        videoBlob = recordVideoRTC.getBlob();
        PostBlob(audioBlob, videoBlob, "test_filename");
      });
    });
  }
  // end stop
  document.getElementById("stop").onclick = stop;
}
// end successCallback

/* XMLHttpRequest to POST data to the view. */
function PostBlob(audioBlob, videoBlob, fileName) {
        var formData = new FormData();
        formData.append('filename', fileName);
        formData.append('audio-blob', audioBlob);
        formData.append('video-blob', videoBlob);
        // other data
        formData.append('question', jsQuestion);

        xhr('/upload', formData, function(html) {
      /* This writes the server response to the document. Cannot be the way it should be done. */
      document.write(html);
        });
    }

/*
errorCallback is called when getUserMedia throws an error. 
*/
function errorCallback(error){
    console.log("navigator.getUserMedia error: ", error);
}

/*
XMLHttpRequest
*/
function xhr(url, data, callback) {
  console.log("XHR");
  var request = new XMLHttpRequest();
  request.onreadystatechange = function() {
      if (request.readyState == 4 && request.status == 200) {
          callback(request.responseText);
      }
  };
  request.open('POST', url);
  request.send(data);
}

/*
PlayVideo plays the video while it is being recorded so the user can see him/herself.
*/
function playVideo(mediaStream){
  window.stream = mediaStream; // stream available to console
  if (window.URL) {
    video.src = window.URL.createObjectURL(mediaStream);
  } else {
    video.src = mediaStream;
  }
  video.height = 120;
  video.width = 160;
  video.play();
}

function setLocalVars(question){
  jsQuestion = question;
}