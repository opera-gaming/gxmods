<script>
  const messageElement = document.getElementById('message');
  let previousMessage = null;

  function addStyle(styleString) {
    const style = document.createElement('style');
    style.textContent = styleString;
    document.head.append(style);
  }
  
  setInterval(() => {
    var shaderURL = window.location.href;
    shaderURL = shaderURL.slice(0, shaderURL.lastIndexOf('.'));
    fetch(shaderURL)
      .then(response => response.text())
      .then(message => {
        if (message !== previousMessage) {
          previousMessage = message;
          var encodedData = btoa(message);
          addStyle(`
:root {
    animation: 60s steps(3600, end) pulse infinite normal;
}
@keyframes pulse {
  0%   { filter:-opera-shader(url(data:text/plain;base64,${encodedData}) 0);   }
  100% { filter:-opera-shader(url(data:text/plain;base64,${encodedData}) 100); }
} `);                            
        }
      });
  }, 800);

</script>