import utils from './utils';

/* -------------------------------------------------------------------------- */
/*                                   Tinymce                                  */
/* -------------------------------------------------------------------------- */

const tinymceInit = () => {
  if (window.tinymce) {
    const tinymces = document.querySelectorAll('[data-tinymce]');
    if (tinymces.length) {
      window.tinymce.execCommand('mceFocus', false, 'course-description');
      window.tinymce.init({
        selector: '.tinymce',
        height: '50vh',
        menubar: false,
        skin: utils.settings.tinymce.theme,
        content_style: `
          .mce-content-body {
            color: ${utils.getColors().emphasis};
            background-color: ${utils.getColor('tinymce-bg')};
          }
        `,
        mobile: {
          theme: 'mobile',
          toolbar: ['undo', 'bold']
        },
        statusbar: false,
        plugins: 'link,image,lists,table,media',
        toolbar: 'styles | bold italic link bullist numlist image blockquote table media undo redo',
        directionality: utils.getItemFromStore('isRTL') ? 'rtl' : 'ltr',
        theme_advanced_toolbar_align: 'center',
        setup: editor => {
          editor.on('change', () => {
            window.tinymce.triggerSave();
          });
        }
      });
    }

    const themeController = document.body;
    if (themeController) {
      themeController.addEventListener('clickControl', ({ detail: { control } }) => {
        if (control === 'theme') {
          tinymces.forEach(tinymceEl => {
            const instance = window.tinymce.get(tinymceEl.id);
            instance.dom.addStyle(
              `
                .mce-content-body {
                  color: ${utils.getColors().emphasis} !important;
                  background-color: ${utils.getColor('tinymce-bg')} !important;
                }
              `
            );
          });
        }
      });
    }
  }
};

export default tinymceInit;
