import utils from '../../utils';
import { chartJsDefaultTooltip, chartJsInit, getBubbleDataset } from './chartjs-utils';
/* -------------------------------------------------------------------------- */
/*                            Chart Bubble                                    */
/* -------------------------------------------------------------------------- */

const chartBubble = () => {
  const pie = document.getElementById('chartjs-bubble-chart');
  const getOptions = () => ({
    type: 'bubble',
    data: {
      datasets: [
        {
          label: 'Dataset 1',
          data: getBubbleDataset(5, 5, 15, 0, 100),
          backgroundColor: utils.getColor('info'),
          hoverBackgroundColor: utils.getColor('info')
        },
        {
          label: 'Dataset 2',
          data: getBubbleDataset(5, 5, 15, 0, 100),
          backgroundColor: utils.getColor('success'),
          hoverBackgroundColor: utils.getColor('success')
        },
        {
          label: 'Dataset 3',
          data: getBubbleDataset(5, 5, 15, 0, 100),
          backgroundColor: utils.getColor('warning'),
          hoverBackgroundColor: utils.getColor('warning')
        }
      ]
    },
    options: {
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: utils.getGrays()['500']
          }
        },
        tooltip: chartJsDefaultTooltip()
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

  chartJsInit(pie, getOptions);
};

export default chartBubble;
