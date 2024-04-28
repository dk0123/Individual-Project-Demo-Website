// main.js

let videoStream; // variable to store the video stream
let video;

// Getting the modal
var modal = document.getElementById("infoModal");

// Getting the button that opens the modal
var btn = document.getElementById("infoBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When user clicks the button, open the modal 
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on x close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// close the model when user clicks anywhere outside it
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
    let video = document.querySelector('video'); 
    const canvas = document.getElementById('main-canvas');
    const context = canvas.getContext('2d');

    if (!video) { 
        video = document.createElement('video');
        document.body.appendChild(video); 
        video.width = canvas.width;
        video.height = canvas.height;
        video.style.display = 'none'; 
    }

    // Function to continuously capture frames from the video stream
    function captureVideoFrame() {
        if (!video.paused && !video.ended) {
             canvas.width = 720;
             canvas.height = 430;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            requestAnimationFrame(captureVideoFrame);
        }
    }

    //Function to start the video stream
    function startVideo() {
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

// Function to stop the video stream and clear the canvas
function stopVideo() {
    if (videoStream) {
        const tracks = videoStream.getTracks();
        tracks.forEach(track => track.stop());
        videoStream = null; // Clear the videoStream variable
    }

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
    .then(data => {
        if(data.error) {
            console.error('Error from server:', data.error);
        } else {
            console.log('Server response:', data);
            displayDemographics(data.recommendations); 
            displayRecommendations(data.recommendations); 
        }
    })
    .catch(error => console.error('Error uploading image:', error));
}

function displayDemographics(demographics) {
    if (!demographics) return;

    const genderDisplay = document.getElementById('gender');
    const ageDisplay = document.getElementById('age');
    const emotionDisplay = document.getElementById('emotion');

    genderDisplay.textContent += demographics.gender || 'Not detected';
    ageDisplay.textContent += demographics.age || 'Not detected';
    emotionDisplay.textContent += demographics.emotion || 'Not detected';
}

function displayRecommendations(recommendations) {
    const recommendationsDiv = document.querySelector('.recommendations');
    recommendationsDiv.innerHTML = '';  

    recommendations.forEach((recommendation) => {
        const p = document.createElement('p');
        p.textContent = recommendation;
        recommendationsDiv.appendChild(p);
    });
}
    // Event listener for the videocam icon
    const videocamIcon = document.querySelector('.blue-circle');
    videocamIcon.addEventListener('mouseover', () => {
        videocamIcon.style.cursor = 'pointer'; 
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