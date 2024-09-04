export class Item {
  #htmlElement;
  #coords;

  constructor(itemId, pprint = false) {
    this.#htmlElement = document.getElementById(itemId);
    if (!this.#htmlElement) {
      throw new Error(`Element with id ${itemId} not found`);
    }
    this.#coords = this.#htmlElement.getBoundingClientRect();
    if (pprint) {
      console.log(this.#coords);
    }
  }

  showItem() { 
    console.log("removing hidden attribute")
    this.#htmlElement.removeAttribute('hidden');
  }
  hideItem() { this.#htmlElement.setAttribute('hidden', true);}

  updatePosition(x, y) {
    this.#htmlElement.style.position = 'absolute';
    this.#htmlElement.style.left = `${x}px`;
    this.#htmlElement.style.top = `${y}px`;
    this.#coords = this.#htmlElement.getBoundingClientRect();
  }

  updateText(content) {
    this.#htmlElement.textContent = content;
  }

  setInnerHtml(html) {
    this.#htmlElement.innerHTML = html;
  }

  setCoords(coords) {
    this.#coords = coords;
  }

  getInnerHtml() {
    return this.#htmlElement.innerHTML;
  }

  getCoords() {
    return this.#coords;
  }

  setDimensions(width, height) {
    this.#htmlElement.style.width = `${width}px`;
    this.#htmlElement.style.height = `${height}px`;
    this.#coords = this.#htmlElement.getBoundingClientRect();
  }
}
