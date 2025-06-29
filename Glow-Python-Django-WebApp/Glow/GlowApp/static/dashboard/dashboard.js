document.addEventListener('DOMContentLoaded', function () {
    const mediaFiles = document.querySelectorAll('.mediaFile');

    mediaFiles.forEach(mediaFile => {
        mediaFile.addEventListener('click', function () {
            // Check if the media file is an image
            if (mediaFile.tagName === 'IMG') {
                if (!document.fullscreenElement) {
                    mediaFile.requestFullscreen().catch(err => {
                        console.error(`Error attempting to enable full-screen mode: ${err.message}`);
                    });
                } else {
                    document.exitFullscreen();
                }
            }
        });
    });
});


