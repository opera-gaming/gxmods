<script>
  const messageElement = document.getElementById('message');
  let previousMessage = null;
  let isFetching = false;

  // Create one reusable <style> element
  const shaderStyle = document.createElement('style');
  document.head.appendChild(shaderStyle);

  function getShaderURL() {
    const url = new URL(window.location.href);
    return url.pathname.replace(/\.[^/.]+$/, '');
  }

  async function checkForUpdate() {
    if (isFetching) return;
    isFetching = true;

    try {
      const response = await fetch(getShaderURL(), { cache: "no-store" });
      if (!response.ok) throw new Error("Failed to fetch shader");

      const message = await response.text();

      if (message !== previousMessage) {
        previousMessage = message;
        const encodedData = btoa(message);

        shaderStyle.textContent =
          `:root { filter: -opera-shader(url(data:text/plain;base64,${encodedData})); }`;
      }
    } catch (error) {
      console.error("Shader update error:", error);
    } finally {
      isFetching = false;
    }
  }

  setInterval(checkForUpdate, 800);
</script>
