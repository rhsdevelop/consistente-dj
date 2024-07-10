const orders = [
  {
    id: 1,
    dropdownId: 'order-dropdown-1',
    orderId: '#181',
    mailLink: 'mailto:ricky@example.com',
    name: 'Ricky Antony',
    email: 'ricky@example.com',
    date: '20/04/2019',
    address: 'Ricky Antony, 2392 Main Avenue, Penasauka, New Jersey 02149',
    shippingType: 'Via Flat Rate',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$99'
  },
  {
    id: 2,
    dropdownId: 'order-dropdown-2',
    orderId: '#182',
    mailLink: 'mailto:kin@example.com',
    name: 'Kin Rossow',
    email: 'kin@example.com',
    date: '20/04/2019',
    address: 'Kin Rossow, 1 Hollywood Blvd,Beverly Hills, California 90210',
    shippingType: 'Via Free Shipping',
    status: 'Processing',
    badge: { type: 'primary', icon: 'fas fa-redo' },
    amount: '$120'
  },
  {
    id: 3,
    dropdownId: 'order-dropdown-3',
    orderId: '#183',
    mailLink: 'mailto:merry@example.com',
    name: 'Merry Diana',
    email: 'merry@example.com',
    date: '30/04/2019',
    address: 'Merry Diana, 1 Infinite Loop, Cupertino, California 90210',
    shippingType: 'Via Link Road',
    status: 'On Hold',
    badge: { type: 'secondary', icon: 'fas fa-ban' },
    amount: '$70'
  },
  {
    id: 4,
    dropdownId: 'order-dropdown-4',
    orderId: '#184',
    mailLink: 'mailto:bucky@example.com',
    name: 'Bucky Robert',
    email: 'bucky@example.com',
    date: '30/04/2019',
    address: 'Bucky Robert, 1 Infinite Loop, Cupertino, California 90210',
    shippingType: 'Via Free Shipping',
    status: 'Pending',
    badge: { type: 'warning', icon: 'fas fa-stream' },
    amount: '$92'
  },
  {
    id: 5,
    dropdownId: 'order-dropdown-5',
    orderId: '#185',
    mailLink: 'mailto:rocky@example.com',
    name: 'Rocky Zampa',
    email: 'rocky@example.com',
    date: '30/04/2019',
    address: 'Rocky Zampa, 1 Infinite Loop, Cupertino, California 90210',
    shippingType: 'Via Free Road',
    status: 'On Hold',
    badge: { type: 'secondary', icon: 'fas fa-ban' },
    amount: '$120'
  },
  {
    id: 6,
    dropdownId: 'order-dropdown-6',
    orderId: '#186',
    mailLink: 'mailto:ricky@example.com',
    name: 'Ricky John',
    email: 'ricky@example.com',
    date: '30/04/2019',
    address: 'Ricky John, 1 Infinite Loop, Cupertino, California 90210',
    shippingType: 'Via Free Shipping',
    status: 'Processing',
    badge: { type: 'primary', icon: 'fas fa-redo' },
    amount: '$145'
  },
  {
    id: 7,
    dropdownId: 'order-dropdown-7',
    orderId: '#187',
    mailLink: 'mailto:cristofer@example.com',
    name: 'Cristofer Henric',
    email: 'cristofer@example.com',
    date: '30/04/2019',
    address: 'Cristofer Henric, 1 Infinite Loop, Cupertino, California 90210',
    shippingType: 'Via Flat Rate',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$55'
  },
  {
    id: 8,
    dropdownId: 'order-dropdown-8',
    orderId: '#188',
    mailLink: 'mailto:lee@example.com',
    name: 'Brate Lee',
    email: 'lee@example.com',
    date: '29/04/2019',
    address: 'Brate Lee, 1 Infinite Loop, Cupertino, California 90210',
    shippingType: 'Via Link Road',
    status: 'On Hold',
    badge: { type: 'secondary', icon: 'fas fa-ban' },
    amount: '$90'
  },
  {
    id: 9,
    dropdownId: 'order-dropdown-9',
    orderId: '#189',
    mailLink: 'mailto:Stephenson@example.com',
    name: 'Thomas Stephenson',
    email: 'Stephenson@example.com',
    date: '29/04/2019',
    address: 'Thomas Stephenson, 116 Ballifeary Road, Bamff',
    shippingType: 'Via Flat Rate',
    status: 'Processing',
    badge: { type: 'primary', icon: 'fas fa-redo' },
    amount: '$52'
  },
  {
    id: 10,
    dropdownId: 'order-dropdown-10',
    orderId: '#190',
    mailLink: 'mailto:eviewsing@example.com',
    name: 'Evie Singh',
    email: 'eviewsing@example.com',
    date: '29/04/2019',
    address: 'Evie Singh, 54 Castledore Road, Tunstead',
    shippingType: 'Via Flat Rate',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$90'
  },
  {
    id: 11,
    dropdownId: 'order-dropdown-11',
    orderId: '#191',
    mailLink: 'mailto:peter@example.com',
    name: 'David Peters',
    email: 'peter@example.com',
    date: '29/04/2019',
    address: 'David Peters, Rhyd Y Groes, Rhosgoch, LL66 0AT',
    shippingType: 'Via Link Road',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$69'
  },
  {
    id: 12,
    dropdownId: 'order-dropdown-12',
    orderId: '#192',
    mailLink: 'mailto:jennifer@example.com',
    name: 'Jennifer Johnson',
    email: 'jennifer@example.com',
    date: '28/04/2019',
    address: 'Jennifer Johnson, Rhyd Y Groes, Rhosgoch, LL66 0AT',
    shippingType: 'Via Flat Rate',
    status: 'Processing',
    badge: { type: 'primary', icon: 'fas fa-redo' },
    amount: '$112'
  },
  {
    id: 13,
    dropdownId: 'order-dropdown-13',
    orderId: '#193',
    mailLink: 'mailto:okuneva@example.com',
    name: ' Demarcus Okuneva',
    email: 'okuneva@example.com',
    date: '28/04/2019',
    address: ' Demarcus Okuneva, 90555 Upton Drive Jeffreyview, UT 08771',
    shippingType: 'Via Flat Rate',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$99'
  },
  {
    id: 14,
    dropdownId: 'order-dropdown-14',
    orderId: '#194',
    mailLink: 'mailto:simeon@example.com',
    name: 'Simeon Harber',
    email: 'simeon@example.com',
    date: '27/04/2019',
    address: 'Simeon Harber, 702 Kunde Plain Apt. 634 East Bridgetview, HI 13134-1862',
    shippingType: 'Via Free Shipping',
    status: 'On Hold',
    badge: { type: 'secondary', icon: 'fas fa-ban' },
    amount: '$129'
  },
  {
    id: 15,
    dropdownId: 'order-dropdown-15',
    orderId: '#195',
    mailLink: 'mailto:lavon@example.com',
    name: 'Lavon Haley',
    email: 'lavon@example.com',
    date: '27/04/2019',
    address: 'Lavon Haley, 30998 Adonis Locks McGlynnside, ID 27241',
    shippingType: 'Via Free Shipping',
    status: 'Pending',
    badge: { type: 'warning', icon: 'fas fa-stream' },
    amount: '$70'
  },
  {
    id: 16,
    dropdownId: 'order-dropdown-16',
    orderId: '#196',
    mailLink: 'mailto:ashley@example.com',
    name: 'Ashley Kirlin',
    email: 'ashley@example.com',
    date: '26/04/2019',
    address: 'Ashley Kirlin, 43304 Prosacco Shore South Dejuanfurt, MO 18623-0505',
    shippingType: 'Via Link Road',
    status: 'Processing',
    badge: { type: 'primary', icon: 'fas fa-redo' },
    amount: '$39'
  },
  {
    id: 17,
    dropdownId: 'order-dropdown-17',
    orderId: '#197',
    mailLink: 'mailto:johnnie@example.com',
    name: 'Johnnie Considine',
    email: 'johnnie@example.com',
    date: '26/04/2019',
    address: 'Johnnie Considine, 6008 Hermann Points Suite 294 Hansenville, TN 14210',
    shippingType: 'Via Flat Rate',
    status: 'Pending',
    badge: { type: 'warning', icon: 'fas fa-stream' },
    amount: '$70'
  },
  {
    id: 18,
    dropdownId: 'order-dropdown-18',
    orderId: '#198',
    mailLink: 'mailto:trace@example.com',
    name: 'Trace Farrell',
    email: 'trace@example.com',
    date: '26/04/2019',
    address: 'Trace Farrell, 431 Steuber Mews Apt. 252 Germanland, AK 25882',
    shippingType: 'Via Free Shipping',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$70'
  },
  {
    id: 19,
    dropdownId: 'order-dropdown-19',
    orderId: '#199',
    mailLink: 'mailto:nienow@example.com',
    name: 'Estell Nienow',
    email: 'nienow@example.com',
    date: '26/04/2019',
    address: 'Estell Nienow, 4167 Laverna Manor Marysemouth, NV 74590',
    shippingType: 'Via Free Shipping',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$59'
  },
  {
    id: 20,
    dropdownId: 'order-dropdown-20',
    orderId: '#200',
    mailLink: 'mailto:howe@example.com',
    name: 'Daisha Howe',
    email: 'howe@example.com',
    date: '25/04/2019',
    address: 'Daisha Howe, 829 Lavonne Valley Apt. 074 Stehrfort, RI 77914-0379',
    shippingType: 'Via Free Shipping',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$39'
  },
  {
    id: 21,
    dropdownId: 'order-dropdown-21',
    orderId: '#201',
    mailLink: 'mailto:haley@example.com',
    name: 'Miles Haley',
    email: 'haley@example.com',
    date: '24/04/2019',
    address: 'Miles Haley, 53150 Thad Squares Apt. 263 Archibaldfort, MO 00837',
    shippingType: 'Via Flat Rate',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$55'
  },
  {
    id: 22,
    dropdownId: 'order-dropdown-22',
    orderId: '#202',
    mailLink: 'mailto:watsica@example.com',
    name: 'Brenda Watsica',
    email: 'watsica@example.com',
    date: '24/04/2019',
    address: "Brenda Watsica, 9198 O'Kon Harbors Morarborough, IA 75409-7383",
    shippingType: 'Via Free Shipping',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$89'
  },
  {
    id: 23,
    dropdownId: 'order-dropdown-23',
    orderId: '#203',
    mailLink: 'mailto:ellie@example.com',
    name: "Ellie O'Reilly",
    email: 'ellie@example.com',
    date: '24/04/2019',
    address: "Ellie O'Reilly, 1478 Kaitlin Haven Apt. 061 Lake Muhammadmouth, SC 35848",
    shippingType: 'Via Free Shipping',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$47'
  },
  {
    id: 24,
    dropdownId: 'order-dropdown-24',
    orderId: '#204',
    mailLink: 'mailto:garry@example.com',
    name: 'Garry Brainstrow',
    email: 'garry@example.com',
    date: '23/04/2019',
    address: 'Garry Brainstrow, 13572 Kurt Mews South Merritt, IA 52491',
    shippingType: 'Via Free Shipping',
    status: 'Completed',
    badge: { type: 'success', icon: 'fas fa-check' },
    amount: '$139'
  },
  {
    id: 25,
    dropdownId: 'order-dropdown-25',
    orderId: '#205',
    mailLink: 'mailto:estell@example.com',
    name: 'Estell Pollich',
    email: 'estell@example.com',
    date: '23/04/2019',
    address: 'Estell Pollich, 13572 Kurt Mews South Merritt, IA 52491',
    shippingType: 'Via Free Shipping',
    status: 'On Hold',
    badge: { type: 'secondary', icon: 'fas fa-ban' },
    amount: '$49'
  },
  {
    id: 26,
    dropdownId: 'order-dropdown-26',
    orderId: '#206',
    mailLink: 'mailto:ara@example.com',
    name: 'Ara Mueller',
    email: 'ara@example.com',
    date: '23/04/2019',
    address: 'Ara Mueller, 91979 Kohler Place Waelchiborough, CT 41291',
    shippingType: 'Via Flat Rate',
    status: 'On Hold',
    badge: { type: 'secondary', icon: 'fas fa-ban' },
    amount: '$19'
  },
  {
    id: 27,
    dropdownId: 'order-dropdown-27',
    orderId: '#207',
    mailLink: 'mailto:blick@example.com',
    name: 'Lucienne Blick',
    email: 'blick@example.com',
    date: '23/04/2019',
    address: 'Lucienne Blick, 6757 Giuseppe Meadows Geraldinemouth, MO 48819-4970',
    shippingType: 'Via Flat Rate',
    status: 'On Hold',
    badge: { type: 'secondary', icon: 'fas fa-ban' },
    amount: '$59'
  },
  {
    id: 28,
    dropdownId: 'order-dropdown-28',
    orderId: '#208',
    mailLink: 'mailto:haag@example.com',
    name: 'Laverne Haag',
    email: 'haag@example.com',
    date: '22/04/2019',
    address: 'Laverne Haag, 2327 Kaylee Mill East Citlalli, AZ 89582-3143',
    shippingType: 'Via Flat Rate',
    status: 'On Hold',
    badge: { type: 'secondary', icon: 'fas fa-ban' },
    amount: '$49'
  },
  {
    id: 29,
    dropdownId: 'order-dropdown-29',
    orderId: '#209',
    mailLink: 'mailto:bednar@example.com',
    name: 'Brandon Bednar',
    email: 'bednar@example.com',
    date: '22/04/2019',
    address: 'Brandon Bednar, 25156 Isaac Crossing Apt. 810 Lonborough, CO 83774-5999',
    shippingType: 'Via Flat Rate',
    status: 'On Hold',
    badge: { type: 'secondary', icon: 'fas fa-ban' },
    amount: '$39'
  },
  {
    id: 30,
    dropdownId: 'order-dropdown-30',
    orderId: '#210',
    mailLink: 'mailto:dimitri@example.com',
    name: 'Dimitri Boehm',
    email: 'dimitri@example.com',
    date: '23/04/2019',
    address: 'Dimitri Boehm, 71603 Wolff Plains Apt. 885 Johnstonton, MI 01581',
    shippingType: 'Via Flat Rate',
    status: 'On Hold',
    badge: { type: 'secondary', icon: 'fas fa-ban' },
    amount: '$111'
  }
];

const advanceAjaxTableInit = () => {
  const togglePaginationButtonDisable = (button, disabled) => {
    const updatedButton = button;
    updatedButton.disabled = disabled;
    updatedButton.classList[disabled ? 'add' : 'remove']('disabled');
  };
  // Selectors
  const table = document.getElementById('advanceAjaxTable');

  if (table) {
    const options = {
      page: 10,
      pagination: {
        item: "<li><button class='page' type='button'></button></li>"
      },
      item: values => {
        const { orderId, id, name, email, date, address, shippingType, status, badge, amount } =
          values;
        return `
          <tr class="btn-reveal-trigger">
            <td class="order py-2 align-middle white-space-nowrap">
              <a href="https://prium.github.io/falcon/v3.16.0/app/e-commerce/orders/order-details.html">
                <strong>${orderId}</strong>
              </a>
              by
              <strong>${name}</strong>
              <br />
              <a href="mailto:${email}">${email}</a>
            </td>
            <td class="py-2 align-middle">
              ${date}
            </td>
            <td class="py-2 align-middle white-space-nowrap">
              ${address}
              <p class="mb-0 text-500">${shippingType}</p>
            </td>
            <td class="py-2 align-middle text-center fs-9 white-space-nowrap">
              <span class="badge rounded-pill d-block badge-subtle-${badge.type}">
                ${status}
                <span class="ms-1 ${badge.icon}" data-fa-transform="shrink-2"></span>
              </span>
            </td>
            <td class="py-2 align-middle text-end fs-9 fw-medium">
              ${amount}
            </td>
            <td class="py-2 align-middle white-space-nowrap text-end">
              <div class="dropstart font-sans-serif position-static d-inline-block">
                <button class="btn btn-link text-600 btn-sm dropdown-toggle btn-reveal" type='button' id="order-dropdown-${id}" data-bs-toggle="dropdown" data-boundary="window" aria-haspopup="true" aria-expanded="false" data-bs-reference="parent">
                  <span class="fas fa-ellipsis-h fs-10"></span>
                </button>
                <div class="dropdown-menu dropdown-menu-end border py-2" aria-labelledby="order-dropdown-${id}">
                  <a href="#!" class="dropdown-item">View</a>
                  <a href="#!" class="dropdown-item">Edit</a>
                  <a href="#!" class="dropdown-item">Refund</a>
                  <div class"dropdown-divider"></div>
                  <a href="#!" class="dropdown-item text-warning">Archive</a>
                  <a href="#!" class="dropdown-item text-warning">Archive</a>
                </div>
              </div>
            </td>
          </tr>
        `;
      }
    };
    const paginationButtonNext = table.querySelector('[data-list-pagination="next"]');
    const paginationButtonPrev = table.querySelector('[data-list-pagination="prev"]');
    const viewAll = table.querySelector('[data-list-view="*"]');
    const viewLess = table.querySelector('[data-list-view="less"]');
    const listInfo = table.querySelector('[data-list-info]');
    const listFilter = document.querySelector('[data-list-filter]');

    const orderList = new window.List(table, options, orders);

    // Fallback
    orderList.on('updated', item => {
      const fallback =
        table.querySelector('.fallback') || document.getElementById(options.fallback);

      if (fallback) {
        if (item.matchingItems.length === 0) {
          fallback.classList.remove('d-none');
        } else {
          fallback.classList.add('d-none');
        }
      }
    });

    const totalItem = orderList.items.length;
    const itemsPerPage = orderList.page;
    const btnDropdownClose = orderList.listContainer.querySelector('.btn-close');
    let pageQuantity = Math.ceil(totalItem / itemsPerPage);
    let numberOfcurrentItems = orderList.visibleItems.length;
    let pageCount = 1;

    btnDropdownClose &&
      btnDropdownClose.addEventListener('search.close', () => orderList.fuzzySearch(''));

    const updateListControls = () => {
      listInfo &&
        (listInfo.innerHTML = `${orderList.i} to ${numberOfcurrentItems} of ${totalItem}`);
      paginationButtonPrev && togglePaginationButtonDisable(paginationButtonPrev, pageCount === 1);
      if (paginationButtonNext) {
        togglePaginationButtonDisable(paginationButtonNext, pageCount === pageQuantity);
      }

      if (pageCount > 1 && pageCount < pageQuantity) {
        togglePaginationButtonDisable(paginationButtonNext, false);
        togglePaginationButtonDisable(paginationButtonPrev, false);
      }
    };
    updateListControls();

    if (paginationButtonNext) {
      paginationButtonNext.addEventListener('click', e => {
        e.preventDefault();
        pageCount += 1;

        const nextInitialIndex = orderList.i + itemsPerPage;
        nextInitialIndex <= orderList.size() && orderList.show(nextInitialIndex, itemsPerPage);
        numberOfcurrentItems += orderList.visibleItems.length;
        updateListControls();
      });
    }

    if (paginationButtonPrev) {
      paginationButtonPrev.addEventListener('click', e => {
        e.preventDefault();
        pageCount -= 1;

        numberOfcurrentItems -= orderList.visibleItems.length;
        const prevItem = orderList.i - itemsPerPage;
        prevItem > 0 && orderList.show(prevItem, itemsPerPage);
        updateListControls();
      });
    }

    const toggleViewBtn = () => {
      viewLess.classList.toggle('d-none');
      viewAll.classList.toggle('d-none');
    };

    if (viewAll) {
      viewAll.addEventListener('click', () => {
        orderList.show(1, totalItem);
        pageQuantity = 1;
        pageCount = 1;
        numberOfcurrentItems = totalItem;
        updateListControls();
        toggleViewBtn();
      });
    }
    if (viewLess) {
      viewLess.addEventListener('click', () => {
        orderList.show(1, itemsPerPage);
        pageQuantity = Math.ceil(totalItem / itemsPerPage);
        pageCount = 1;
        numberOfcurrentItems = orderList.visibleItems.length;
        updateListControls();
        toggleViewBtn();
      });
    }
    if (options.pagination) {
      table.querySelector('.pagination').addEventListener('click', e => {
        if (e.target.classList[0] === 'page') {
          pageCount = Number(e.target.innerText);
          updateListControls();
        }
      });
    }
    if (options.filter) {
      const { key } = options.filter;
      listFilter.addEventListener('change', e => {
        orderList.filter(item => {
          if (e.target.value === '') {
            return true;
          }
          return item.values()[key].toLowerCase().includes(e.target.value.toLowerCase());
        });
      });
    }
  }
};

export default advanceAjaxTableInit;
