import utils from '../../utils';
import { chartJsDefaultTooltip, chartJsInit } from './chartjs-utils';

/* -------------------------------------------------------------------------- */
/*                                  bar-chart                                 */
/* -------------------------------------------------------------------------- */

const barChartInit = () => {
  const barChartElement = document.getElementById('chartjs-bar-chart');

  const getOptions = () => ({
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [
        {
          label: '# of Votes',
          data: [12, 19, 3, 5, 6, 3],
          backgroundColor: [
            utils.getSubtleColors().secondary,
            utils.getSubtleColors().warning,
            utils.getSubtleColors().info,
            utils.getSubtleColors().success,
            utils.getSubtleColors().info,
            utils.getSubtleColors().primary
          ],
          borderWidth: 0
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

  chartJsInit(barChartElement, getOptions);
};

export default barChartInit;
