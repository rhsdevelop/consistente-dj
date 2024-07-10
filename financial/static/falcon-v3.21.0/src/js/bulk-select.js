import DomNode from './node';
import utils from './utils';

/*-----------------------------------------------
|   Bulk Select
-----------------------------------------------*/

const elementMap = new Map();

class BulkSelect {
  constructor(element, option) {
    this.element = element;
    this.option = {
      displayNoneClassName: 'd-none',
      ...option
    };
    elementMap.set(this.element, this);
  }

  // Static
  static getInstance(element) {
    if (elementMap.has(element)) {
      return elementMap.get(element);
    }
    return null;
  }

  init() {
    this.attachNodes();
    this.clickBulkCheckbox();
    this.clickRowCheckbox();
  }

  getSelectedRows() {
    return Array.from(this.bulkSelectRows)
      .filter(row => row.checked)
      .map(row => utils.getData(row, 'bulk-select-row'));
  }

  attachNodes() {
    const { body, actions, replacedElement } = utils.getData(this.element, 'bulk-select');
    this.actions = new DomNode(document.getElementById(actions));
    this.replacedElement = new DomNode(document.getElementById(replacedElement));
    this.bulkSelectRows = document.getElementById(body).querySelectorAll('[data-bulk-select-row]');
  }

  attachRowNodes(elms) {
    this.bulkSelectRows = elms;
  }

  clickBulkCheckbox() {
    // Handle click event in bulk checkbox
    this.element.addEventListener('click', () => {
      if (this.element.indeterminate === 'indeterminate') {
        this.actions.addClass(this.option.displayNoneClassName);
        this.replacedElement.removeClass(this.option.displayNoneClassName);

        this.removeBulkCheck();

        this.bulkSelectRows.forEach(el => {
          const rowCheck = new DomNode(el);
          rowCheck.setProp('checked', false);
          rowCheck.setAttribute('checked', false);
        });
        return;
      }

      this.toggleDisplay();
      this.bulkSelectRows.forEach(el => {
        el.checked = this.element.checked;
      });
    });
  }

  clickRowCheckbox() {
    // Handle click event in checkbox of each row
    this.bulkSelectRows.forEach(el => {
      const rowCheck = new DomNode(el);
      rowCheck.on('click', () => {
        if (this.element.indeterminate !== 'indeterminate') {
          this.element.indeterminate = true;
          this.element.setAttribute('indeterminate', 'indeterminate');
          this.element.checked = true;
          this.element.setAttribute('checked', true);

          this.actions.removeClass(this.option.displayNoneClassName);
          this.replacedElement.addClass(this.option.displayNoneClassName);
        }

        if ([...this.bulkSelectRows].every(element => element.checked)) {
          this.element.indeterminate = false;
          this.element.setAttribute('indeterminate', false);
        }

        if ([...this.bulkSelectRows].every(element => !element.checked)) {
          this.removeBulkCheck();
          this.toggleDisplay();
        }
      });
    });
  }

  removeBulkCheck() {
    this.element.indeterminate = false;
    this.element.removeAttribute('indeterminate');
    this.element.checked = false;
    this.element.setAttribute('checked', false);
  }

  toggleDisplay() {
    this.actions.toggleClass(this.option.displayNoneClassName);
    this.replacedElement.toggleClass(this.option.displayNoneClassName);
  }
}

function bulkSelectInit() {
  const bulkSelects = document.querySelectorAll('[data-bulk-select');

  if (bulkSelects.length) {
    bulkSelects.forEach(el => {
      const bulkSelect = new BulkSelect(el);
      bulkSelect.init();
    });
  }
}

export default bulkSelectInit;

window.BulkSelect = BulkSelect;
