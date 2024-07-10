import utils from './utils';

/* -------------------------------------------------------------------------- */
/*                                 SortableJS                                 */
/* -------------------------------------------------------------------------- */

const sortableInit = () => {
  const { getData } = utils;

  const sortableEl = document.querySelectorAll('[data-sortable]');

  const defaultOptions = {
    animation: 150,
    group: {
      name: 'shared'
    },
    delay: 100,
    delayOnTouchOnly: true,
    forceFallback: true,
    onStart() {
      document.body.classList.add('sortable-dragging');
    },
    onEnd() {
      document.body.classList.remove('sortable-dragging');
    }
  };

  sortableEl.forEach(el => {
    const userOptions = getData(el, 'sortable');
    const options = window._.merge(defaultOptions, userOptions);

    return window.Sortable.create(el, options);
  });
};

export default sortableInit;
