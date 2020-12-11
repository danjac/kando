import { Controller } from 'stimulus';

export default class extends Controller {
  static targets = ['item'];

  toggle() {
    event.preventDefault();
    event.stopPropagation();
    this.itemTargets.forEach((item) => {
      item.classList.toggle('hidden');
    });
  }

  close(event) {
    this.itemTargets.forEach((item) => {
      item.classList.add('hidden');
    });
  }
}
