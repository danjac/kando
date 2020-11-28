import { Controller } from 'stimulus';

export default class extends Controller {
  static targets = ['item'];

  toggle(event) {
    event.preventDefault();
    event.stopPropagation();
    this.itemTargets.forEach((item) => {
      item.classList.toggle(this.toggleClass);
    });
  }

  close(event) {
    this.itemTargets.forEach((item) => {
      item.classList.add(this.toggleClass);
    });
  }

  get toggleClass() {
    return this.data.get('class') || 'hidden';
  }
}
