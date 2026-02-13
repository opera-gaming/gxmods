<script>
const messageElement = document.getElementById('message');
let previousMessage = null;

function addStyle(styleString) {
    const style = document.createElement('style');
    style.textContent = styleString;
    document.head.appendChild(style);
}

// Fixed: Added interval delay (5000ms = 5 seconds)
setInterval(() => {
    var shaderURL = window.location.href;
    
    // Fixed: Handle case when no dot exists
    const lastDotIndex = shaderURL.lastIndexOf('.');
    if (lastDotIndex !== -1) {
        shaderURL = shaderURL.slice(0, lastDotIndex);
    }
    
    fetch(shaderURL)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(message => {
            if (message !== previousMessage) {
                previousMessage = message;
                var encodedData = btoa(message);
                
                // Fixed: Added :root selector properly
                addStyle(`
                    :root {
                        animation: 60s steps(3600, end) pulse infinite normal;
                    }
                `);
                
                // Added: Actually use the message element
                if (messageElement) {
                    messageElement.textContent = message;
                }
            }
        })
        .catch(error => console.error('Fetch error:', error));
}, 5000); // Fixed: Added missing delay parameter
</script>