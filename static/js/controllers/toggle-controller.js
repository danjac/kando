import { Controller } from 'stimulus';

export default class extends Controller {
  static targets = ['item'];

  toggle() {
    this.itemTargets.forEach((item) => {
      item.classList.toggle('hidden');
    });
  }

  close() {
    this.itemTargets.forEach((item) => {
      item.classList.add('hidden');
    });
  }
}
