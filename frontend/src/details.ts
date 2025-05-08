export function updateDetailsContainer(content: string) {
  const detailsContainer = document.querySelector<HTMLDivElement>('.details-container');
  if (detailsContainer) {
    detailsContainer.innerHTML = `<p>${content}</p>`;
  }
}