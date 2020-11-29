import { Controller } from 'stimulus';
import axios from 'axios';
import Sortable from 'sortablejs';

export default class extends Controller {
  static targets = ['draggable'];
  connect() {
    // set put: false to prevent
    this.sortable = Sortable.create(this.element, {
      animation: 150,
      draggable: '.draggable',
      group: this.data.get('group') || 'shared',
      onAdd: this.add.bind(this),
      onRemove: this.remove.bind(this),
      onUpdate: this.update.bind(this),
    });
  }

  add(event) {
    this.update();
  }

  remove(event) {
    this.update();
  }

  update(event) {
    if (this.data.has('url')) {
      const items = [];
      this.draggableTargets.forEach((target) => {
        items.push(target.dataset.id);
      });
      axios.post(this.data.get('url'), { items });
    }
  }
}
