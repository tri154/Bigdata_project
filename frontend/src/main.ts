import './style.css'

const imageElement = document.querySelector<HTMLImageElement>('#dynamic-image');

let previousImageUrl: string | null = null;

async function fetchAndUpdateImage() {
  try {
    const response = await fetch(`http://localhost:8000/get_image?timestamp=${Date.now()}`);
    if (!response.ok) {
      throw new Error('Failed to fetch image');
    }

    const imageBlob = await response.blob();
    const imageUrl = URL.createObjectURL(imageBlob);

    if (imageElement) {
      imageElement.onload = () => {
        // Revoke the previous URL after the new image has loaded
        if (previousImageUrl) {
          URL.revokeObjectURL(previousImageUrl);
        }
        previousImageUrl = imageUrl;
      };
      imageElement.src = imageUrl;
    }
  } catch (error) {
    console.error('Error fetching image:', error);
  }
}



// Fetch the image initially
fetchAndUpdateImage();

// Optionally, set up a periodic update (e.g., every 10 seconds)
setInterval(fetchAndUpdateImage, 100);
