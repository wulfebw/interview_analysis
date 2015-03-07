/* 
What this needs
(1) something to capture audio
(2) something to capture video
(3) something to start recording
(4) something to stop recording
(5) something to send the recordings
*/
console.log("START");
// before everything
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
var constraints = {audio: true, video: true};
var video = document.querySelector("video");
var isFirefox = !!navigator.mozGetUserMedia;
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
    // recordVideoRTC.stopRecording();
    // console.log("after stop");
    // console.log(recordAudioRTC);

    // audioBlob = recordAudioRTC.getBlob();
    // videoBlob = recordVideoRTC.getBlob();
    // console.log("audio blob:");
    // console.log(audioBlob);
    // console.log("video blob:");
    // console.log(videoBlob);

    // // postFiles(audioBlob, videoBlob);
    // PostBlob(audioBlob, videoBlob, "test_filename");


    // recordAudioRTC.getBlob(function(audioBlob){
    //   console.log("after audio")
    //   recordVideoRTC.getBlob(function(videoBlob){
    //     console.log("after video")
    //     console.log("audio URL")
    //     console.log(audioBlob)
    //     console.log("video URL")
    //     console.log(videoBlob)
    //     postFiles(aduioBlob, videoBlob);
    //   })
    // })

    // recordAudioRTC.getDataURL(function(audioURL){
    //   console.log("after audio")
    //   recordVideoRTC.getDataURL(function(videoURL){
    //     console.log("after video")
    //     video.pause();
    //     console.log("audio URL")
    //     console.log(audioURL)
    //     console.log("video URL")
    //     console.log(videoURL)
    //     postFiles(aduioURL, videoURL);
    //   })
    // })
    
    // console.log("audio URL")
    // console.log(audioURL)
    // recordAudioRTC.stopRecording(function(url){   // what's this do?
    //   mediaElement.src = url;
    // });
    // // var videoBlob = recordVideoRTC.getBlob();
    // var videoURL = recordVideoRTC.getDataURL()
    // console.log("video URL")
    // console.log(videoURL)
    // recordVideoRTC.stopRecording(function(url){   // what's this do?
    //   mediaElement.src = url;
    // });
    // // formData = new FormData();
    // // formData.append('audio', audioBlob);
    // // formData.append('video', videoBlob);

    // // xhr('/upload', formData, function(){})
    // // onStopRecording();

    // // function onStopRecording(){
    // //  recordAudioRTC.getDataURL(function(audioDataURL){
    // //    recordVideoRTC.getDataURL(function(videoDataURL){
    // //      postFiles(audioDataURL, videoDataURL);
    // //    })
    // //  })
    // // }
    // video.pause();

    // postFiles(aduioURL, videoURL);


  }
  // end stop
  document.getElementById("stop").onclick = stop;

}
// end successCallback


function PostBlob(audioBlob, videoBlob, fileName) {
        var formData = new FormData();
        formData.append('filename', fileName);
        formData.append('audio-blob', audioBlob);
        formData.append('video-blob', videoBlob);
        xhr('/upload', formData, function(html) {
	    document.write(html);


            // document.querySelector('h1').innerHTML = ffmpeg_output.replace(/\\n/g, '<br />');
            // preview.src = 'uploads/' + fileName + '-merged.webm';
            // preview.play();
            // preview.muted = false;
        });
    }





var fileName;
function postFiles(audioDataURL, videoDataURL){
  console.log("POST FILES")
  fileName = "test";

  var files = {};
  files.audio = {
            name: fileName + (isFirefox ? '.webm' : '.wav'),
                type: isFirefox ? 'video/webm' : 'audio/wav',
                contents: audioDataURL
                  };
    files.video = {
                        name: fileName + '.webm',
                        type: 'video/webm',
                        contents: videoDataURL
                    };

    // JSON.stringify(files)
    // document.getElementById('id_audio_file').value = files.audio;
    // document.getElementById('id_video_file').value = files.video;

    // xhr('/upload', JSON.stringify(files), function(_fileName) {
    //   $.get('/upload');
    // });
  // console.log('AJAX likes bunnies')
  // $.ajax({
  //  type: "POST", 
  //  url: '/playback/',
  //  data:   {
 //                 'video': files.video, // from form
 //                 'audio': files.audio
 //             },
 //        success: function(){ $('#message').html("<h2>Contact Form Submitted!</h2>")}
  // });

  xhr('/upload', JSON.stringify(files), function(_doNothing){});


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


