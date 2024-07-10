import utils from '../../utils';
import { chartJsDefaultTooltip, chartJsInit } from './chartjs-utils';

/* -------------------------------------------------------------------------- */
/*                            Chart Line                                  */
/* -------------------------------------------------------------------------- */
const chartLine = () => {
  const line = document.getElementById('chartjs-line-chart');

  const getOptions = () => ({
    type: 'bar',
    data: {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        {
          type: 'line',
          label: 'Dataset 1',
          borderColor: utils.getColor('primary'),
          borderWidth: 2,
          fill: false,
          data: [55, 80, 60, 22, 50, 40, 90],
          tension: 0.3
        }
      ]
    },
    options: {
      plugins: {
        tooltip: chartJsDefaultTooltip(),
        legend: {
          labels: {
            color: utils.getGrays()['500']
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: utils.getGrays()['500']
          },
          grid: {
            color: utils.getGrays()['300'],
            drawBorder: false
          }
        },
        y: {
          ticks: {
            color: utils.getGrays()['500']
          },
          grid: {
            color: utils.getGrays()['300'],
            drawBorder: false
          }
        }
      }
    }
  });

  chartJsInit(line, getOptions);
};

export default chartLine;
