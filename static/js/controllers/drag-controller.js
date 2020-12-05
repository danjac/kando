import { Controller } from 'stimulus';
import axios from 'axios';
import Sortable from 'sortablejs';

const DEFAULT_GROUP = 'shared';

export default class extends Controller {
  static targets = ['draggable'];

  static values = {
    draggable: String,
    group: String,
    url: String,
  };

  connect() {
    // set put: false to prevent
    this.sortable = Sortable.create(this.element, {
      animation: 150,
      draggable: this.draggableValue || '.draggable',
      group: this.groupValue || DEFAULT_GROUP,
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
    if (this.hasUrlValue) {
      const items = [];
      const group = this.groupValue || DEFAULT_GROUP;
      this.draggableTargets.forEach((target) => {
        if (target.dataset.group === group) {
          items.push(target.dataset.id);
        }
      });
      axios.post(this.urlValue, { items });
    }
  }
}
