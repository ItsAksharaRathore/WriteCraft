document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const textInput = document.getElementById('text-input');
    const fontSelect = document.getElementById('font-select');
    const fontSize = document.getElementById('font-size');
    const fontSizeValue = document.getElementById('font-size-value');
    const lineSpacing = document.getElementById('line-spacing');
    const lineSpacingValue = document.getElementById('line-spacing-value');
    const randomness = document.getElementById('randomness');
    const randomnessValue = document.getElementById('randomness-value');
    const inkColor = document.getElementById('ink-color');
    const paperColor = document.getElementById('paper-color');
    const pressureVar = document.getElementById('pressure-var');
    const pressureVarValue = document.getElementById('pressure-var-value');
    const showAdvanced = document.getElementById('show-advanced');
    const advancedOptions = document.getElementById('advanced-options');
    const generateBtn = document.getElementById('generate-btn');
    const previewBtn = document.getElementById('preview-btn');
    const downloadBtn = document.getElementById('download-btn');
    const clearBtn = document.getElementById('clear-btn');
    const statusBar = document.getElementById('status-bar');
    const previewImage = document.getElementById('preview-image');
    
    // Current generated image data
    let currentImageData = null;
    
    // Event Listeners
    fontSize.addEventListener('input', () => {
        fontSizeValue.textContent = fontSize.value;
    });
    
    lineSpacing.addEventListener('input', () => {
        lineSpacingValue.textContent = lineSpacing.value;
    });
    
    randomness.addEventListener('input', () => {
        randomnessValue.textContent = randomness.value;
    });
    
    pressureVar.addEventListener('input', () => {
        pressureVarValue.textContent = pressureVar.value;
    });
    
    showAdvanced.addEventListener('change', () => {
        advancedOptions.style.display = showAdvanced.checked ? 'block' : 'none';
    });
    
    generateBtn.addEventListener('click', generateHandwriting);
    previewBtn.addEventListener('click', previewHandwriting);
    downloadBtn.addEventListener('click', downloadImage);
    clearBtn.addEventListener('click', clearText);
    
    // Functions
    function updateStatus(message, isError = false) {
        statusBar.textContent = message;
        statusBar.style.color = isError ? 'var(--danger-color)' : '#666';
    }
    
    async function generateHandwriting() {
        const text = textInput.value.trim();
        if (!text) {
            updateStatus('Please enter some text to convert!', true);
            return;
        }
        
        updateStatus('Generating handwriting...');
        
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    font: fontSelect.value,
                    fontSize: fontSize.value,
                    lineSpacing: lineSpacing.value,
                    inkColor: inkColor.value,
                    paperColor: paperColor.value,
                    randomness: randomness.value,
                    pressureVar: pressureVar.value
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to generate handwriting');
            }
            
            const blob = await response.blob();
            currentImageData = URL.createObjectURL(blob);
            
            // Display the generated image
            previewImage.innerHTML = `<img src="${currentImageData}" alt="Generated Handwriting">`;
            
            updateStatus('Handwriting generated successfully! Click "Download Image" to save it.');
        } catch (error) {
            console.error('Error:', error);
            updateStatus(error.message, true);
        }
    }
    
    function previewHandwriting() {
        const text = textInput.value.trim();
        if (!text) {
            updateStatus('Please enter some text to preview!', true);
            return;
        }
        
        // For preview, we'll just generate the full image but show it in the preview area
        generateHandwriting();
    }
    
    function downloadImage() {
        if (!currentImageData) {
            updateStatus('Please generate handwriting first!', true);
            return;
        }
        
        const a = document.createElement('a');
        a.href = currentImageData;
        a.download = 'handwriting.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        updateStatus('Image downloaded successfully!');
    }
    
    function clearText() {
        textInput.value = '';
        updateStatus('Text cleared');
    }
    
    // Initialize
    updateStatus('Ready to convert text to handwriting');
});