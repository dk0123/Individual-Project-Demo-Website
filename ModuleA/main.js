// main.js

let videoStream; // Variable to store the video stream
let video;


// Get the modal
var modal = document.getElementById("infoModal");

// Get the button that opens the modal
var btn = document.getElementById("infoBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}




// Function to handle the runtime initialization of OpenCV
function openCvReady() {
    cv['onRuntimeInitialized'] = () => {
        console.log('OpenCV is ready');

        // Call a function to initialize video streaming when OpenCV is ready
        initializeVideo();
    };
}

// Function to initialize video streaming
function initializeVideo() {
    let video = document.querySelector('video'); // Try to get an existing video element
    const canvas = document.getElementById('main-canvas');
    const context = canvas.getContext('2d');

    if (!video) { // If no video element exists, create and configure a new one
        video = document.createElement('video');
        document.body.appendChild(video); // Append it somewhere in your document; adjust as needed
        video.width = canvas.width;
        video.height = canvas.height;
        video.style.display = 'none'; // Hide the video element as it's not directly displayed
    }

    // Function to continuously capture frames from the video stream
    function captureVideoFrame() {
        if (!video.paused && !video.ended) {
             // Set canvas width and height outside of drawImage
             canvas.width = 920;
             canvas.height = 630;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            requestAnimationFrame(captureVideoFrame);
        }
    }

    // Function to start the video stream
    function startVideo() {
        // Ensure the canvas is displayed
        const canvas = document.getElementById('main-canvas');
        canvas.style.display = 'block';
    
        const video = document.querySelector('video');
        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
            .then((stream) => {
                videoStream = stream;
                video.srcObject = stream;
                video.play();
                captureVideoFrame();
            })
            .catch((error) => {
                console.error('Error accessing camera:', error);
            });
    }

    // Function to stop the video stream
// Function to stop the video stream and clear the canvas
function stopVideo() {
    if (videoStream) {
        const tracks = videoStream.getTracks();
        tracks.forEach(track => track.stop());
        videoStream = null; // Clear the videoStream variable
    }
    // Hide the video element or handle as needed
    if (video) {
        video.pause();
        video.srcObject = null;
        video.load();
    }
}




    // Convert dataURL to Blob
    function dataURLToBlob(dataURL) {
    const byteString = atob(dataURL.split(',')[1]);
    const mimeString = dataURL.split(',')[0].split(':')[1].split(';')[0]
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], {type: mimeString});
}



function captureFrame() {
    if (!videoStream || !video) {
        console.error('Video stream is not active.');
        return;
    }
    
    const canvas = document.getElementById('main-canvas');
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth; // Adjust canvas size to match video frame
    canvas.height = video.videoHeight;

    // Draw the current video frame onto the canvas.
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Optional: Display feedback that a photo was taken
    flashFeedback();

    // Convert canvas content to a data URL and proceed with Blob conversion and upload
    const dataURL = canvas.toDataURL("image/png");
    const blob = dataURLToBlob(dataURL);
    const formData = new FormData();
    formData.append('image', blob, 'captured_image.png');
    uploadImage(formData);

    // Stop the video stream after capturing the frame
    stopVideo();
}



    // Event listener for the capture icon/button
const captureIcon = document.querySelector('.capture-icon');
captureIcon.addEventListener('click', () => {
    captureFrame();
});

function flashFeedback() {
    const canvas = document.getElementById('main-canvas');
    canvas.style.opacity = '0.5';
    setTimeout(() => canvas.style.opacity = '1', 500); // Adjust timing as needed
}

function uploadImage(formData) {
    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => console.log('Server response:', data))
    .catch(error => console.error('Error uploading image:', error));
}


    // Event listener for the videocam icon
    const videocamIcon = document.querySelector('.blue-circle');
    videocamIcon.addEventListener('mouseover', () => {
        videocamIcon.style.cursor = 'pointer'; // Change cursor to pointer on hover
    });
    
    videocamIcon.addEventListener('click', () => {
        if (video.paused) {
            startVideo();
        } else {
            stopVideo();
        }
    });
}

// Call the openCvReady function when the OpenCV script is loaded
openCvReady();