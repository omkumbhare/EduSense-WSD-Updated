/**
 * EduSense - Interactive Frontend JavaScript Helpers
 */

document.addEventListener('DOMContentLoaded', () => {
    // Synchronize slider value display
    const windowSlider = document.getElementById('window_size');
    const windowValDisplay = document.getElementById('window_val');
    
    if (windowSlider && windowValDisplay) {
        windowSlider.addEventListener('input', (e) => {
            windowValDisplay.textContent = `±${e.target.value} words`;
        });
    }
});

/**
 * Loads pre-packaged sample transcript into analyzer form fields
 */
function loadSample(transcriptText, targetWord) {
    const transcriptInput = document.getElementById('transcript');
    const targetInput = document.getElementById('target_word');
    
    if (transcriptInput && targetInput) {
        transcriptInput.value = transcriptText;
        targetInput.value = targetWord;
        transcriptInput.focus();
        
        // Scroll smoothly to form if needed
        transcriptInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}
