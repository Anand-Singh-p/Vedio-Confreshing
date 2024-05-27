// toggleMedia.js

function toggleCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            const videoTracks = stream.getVideoTracks();
            if (videoTracks.length === 0) {
                console.log('No video tracks found');
                return;
            }
            videoTracks[0].enabled = !videoTracks[0].enabled; // Toggle camera
        })
        .catch(error => {
            console.error('Error accessing camera:', error);
        });
}

function toggleMicrophone() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const audioTracks = stream.getAudioTracks();
            if (audioTracks.length === 0) {
                console.log('No audio tracks found');
                return;
            }
            audioTracks[0].enabled = !audioTracks[0].enabled; // Toggle microphone
        })
        .catch(error => {
            console.error('Error accessing microphone:', error);
        });
}
