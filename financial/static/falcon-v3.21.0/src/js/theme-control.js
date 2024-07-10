import { setItemToStore, getData, getItemFromStore, getSystemTheme } from './utils';
import DomNode from './node';
import CONFIG from './config';

/* -------------------------------------------------------------------------- */
/*                                Theme Control                               */
/* -------------------------------------------------------------------------- */
const initialDomSetup = element => {
  if (!element) return;
  const dataUrlDom = element.querySelector('[data-theme-control = "navbarPosition"]');
  const hasDataUrl = dataUrlDom ? getData(dataUrlDom, 'page-url') : null;

  element.querySelectorAll('[data-theme-control]').forEach(el => {
    const inputDataAttributeValue = getData(el, 'theme-control');
    const localStorageValue = getItemFromStore(inputDataAttributeValue);

    if (
      inputDataAttributeValue === 'navbarStyle' &&
      !hasDataUrl &&
      (getItemFromStore('navbarPosition') === 'top' ||
        getItemFromStore('navbarPosition') === 'double-top')
    ) {
      el.setAttribute('disabled', true);
    }
    if (el.type === 'select-one' && inputDataAttributeValue === 'navbarPosition') {
      el.value = localStorageValue;
    }
    if (el.type === 'checkbox') {
      if (inputDataAttributeValue === 'theme') {
        if (
          localStorageValue === 'auto' ? getSystemTheme() === 'dark' : localStorageValue === 'dark'
        ) {
          el.setAttribute('checked', true);
        }
      } else {
        localStorageValue && el.setAttribute('checked', true);
      }
    } else if (el.type === 'radio') {
      const isChecked = localStorageValue === el.value;
      isChecked && el.setAttribute('checked', true);
    } else {
      const isActive = localStorageValue === el.value;
      isActive && el.classList.add('active');
    }
  });
};

const changeTheme = element => {
  element.querySelectorAll('[data-theme-control = "theme"]').forEach(el => {
    const inputDataAttributeValue = getData(el, 'theme-control');
    const localStorageValue = getItemFromStore(inputDataAttributeValue);

    if (el.type === 'checkbox') {
      if (localStorageValue === 'auto') {
        getSystemTheme() === 'dark' ? (el.checked = true) : (el.checked = false);
      } else {
        localStorageValue === 'dark' ? (el.checked = true) : (el.checked = false);
      }
    } else if (el.type === 'radio') {
      localStorageValue === el.value ? (el.checked = true) : (el.checked = false);
    } else {
      localStorageValue === el.value ? el.classList.add('active') : el.classList.remove('active');
    }
  });
};

const handleThemeDropdownIcon = value => {
  document.querySelectorAll('[data-theme-dropdown-toggle-icon]').forEach(el => {
    el.classList.toggle('d-none', value !== getData(el, 'theme-dropdown-toggle-icon'));
  });
};

handleThemeDropdownIcon(getItemFromStore('theme'));

const themeControl = () => {
  const themeController = new DomNode(document.body);

  const navbarVertical = document.querySelector('.navbar-vertical');
  initialDomSetup(themeController.node);

  themeController.on('click', e => {
    const target = new DomNode(e.target);

    if (target.data('theme-control')) {
      const control = target.data('theme-control');
      let value = e.target[e.target.type === 'checkbox' ? 'checked' : 'value'];

      if (control === 'theme') {
        typeof value === 'boolean' && (value = value ? 'dark' : 'light');
      }
      if (control !== 'navbarPosition') {
        Object.prototype.hasOwnProperty.call(CONFIG, control) && setItemToStore(control, value);
        switch (control) {
          case 'theme': {
            document.documentElement.setAttribute(
              'data-bs-theme',
              value === 'auto' ? getSystemTheme() : value
            );
            const clickControl = new CustomEvent('clickControl', {
              detail: { control, value }
            });
            e.currentTarget.dispatchEvent(clickControl);
            changeTheme(themeController.node);
            break;
          }
          case 'navbarStyle': {
            navbarVertical.classList.remove('navbar-card');
            navbarVertical.classList.remove('navbar-inverted');
            navbarVertical.classList.remove('navbar-vibrant');
            if (value !== 'transparent') {
              navbarVertical.classList.add(`navbar-${value}`);
            }
            break;
          }
          case 'reset': {
            Object.keys(CONFIG).forEach(key => {
              localStorage.setItem(key, CONFIG[key]);
            });
            window.location.reload();
            break;
          }
          default:
            window.location.reload();
        }
      }
    }
  });

  // control navbar position
  themeController.on('change', e => {
    const target = new DomNode(e.target);

    if (target.data('theme-control') === 'navbarPosition') {
      Object.prototype.hasOwnProperty.call(CONFIG, 'navbarPosition') &&
        setItemToStore('navbarPosition', e.target.value);

      const pageUrl = getData(target.node.selectedOptions[0], 'page-url');
      pageUrl
        ? window.location.replace(pageUrl)
        : window.location.replace(window.location.href.split('#')[0]);
    }
  });

  themeController.on('clickControl', ({ detail: { control, value } }) => {
    if (control === 'theme') {
      handleThemeDropdownIcon(value);
    }
  });
};

export default themeControl;
