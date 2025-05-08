import './style.css'

const imageElement = document.querySelector<HTMLImageElement>('#dynamic-image');

async function fetchAndUpdateImage() {
  try {
    // Append a timestamp to bypass browser cache
    const response = await fetch(`http://localhost:8000/api/image?timestamp=${Date.now()}`);
    if (!response.ok) {
      throw new Error('Failed to fetch image');
    }
    const imageBlob = await response.blob();
    const imageUrl = URL.createObjectURL(imageBlob);

    if (imageElement) {
      imageElement.src = imageUrl;

      // Optional: revoke the previous blob URL to free memory
      imageElement.onload = () => {
        URL.revokeObjectURL(imageUrl);
      };
    }
  } catch (error) {
    console.error('Error fetching image:', error);
  }
}

// Fetch the image initially
fetchAndUpdateImage();

// Optionally, set up a periodic update (e.g., every 10 seconds)
setInterval(fetchAndUpdateImage, 100);
