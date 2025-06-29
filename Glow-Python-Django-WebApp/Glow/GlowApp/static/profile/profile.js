
// Get all mediaItem elements
var mediaItems = document.querySelectorAll('.mediaItem');

// Add click event listener to each mediaItem
mediaItems.forEach(function(item) {
    item.addEventListener('click', function() {
        // Get the media file element inside the clicked mediaItem
        var mediaFile = item.querySelector('.mediaFile');
        // Check if the browser supports fullscreen mode
        if (mediaFile.requestFullscreen) {
            // Request fullscreen for the media file element
            mediaFile.requestFullscreen();
        } else if (mediaFile.mozRequestFullScreen) { /* Firefox */
            mediaFile.mozRequestFullScreen();
        } else if (mediaFile.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
            mediaFile.webkitRequestFullscreen();
        } else if (mediaFile.msRequestFullscreen) { /* IE/Edge */
            mediaFile.msRequestFullscreen();
        }
    });
});

