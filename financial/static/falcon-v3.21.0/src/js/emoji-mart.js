import utils from './utils';

/* -------------------------------------------------------------------------- */
/*                                   Popover                                  */
/* -------------------------------------------------------------------------- */

const emojiMartInit = () => {
  const { Picker } = window.EmojiMart || {};
  if (Picker) {
    const emojiMartBtns = document.querySelectorAll('[data-emoji-mart]');
    if (emojiMartBtns) {
      Array.from(emojiMartBtns).forEach(btn => {
        const inputTarget = utils.getData(btn, 'emoji-mart-input-target');
        const input = document.querySelector(inputTarget);
        const picker = new Picker(
          window._.merge(utils.getData(btn, 'emoji-mart'), {
            previewPosition: 'none',
            skinTonePosition: 'none',
            onEmojiSelect: e => {
              if (input) input.innerHTML += e.native;
            },
            onClickOutside: e => {
              if (!picker.contains(e.target) && !btn.contains(e.target)) {
                picker.classList.add('d-none');
              }
            }
          })
        );

        picker.classList.add('d-none');
        btn.parentElement.appendChild(picker);

        btn.addEventListener('click', () => picker.classList.toggle('d-none'));
      });
    }
  }
};
export default emojiMartInit;
