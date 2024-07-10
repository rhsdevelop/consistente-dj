import utils from '../../utils';
import { chartJsDefaultTooltip, chartJsInit } from './chartjs-utils';

/* -------------------------------------------------------------------------- */
/*                            Chart Doughnut                                  */
/* -------------------------------------------------------------------------- */
const chartDoughnut = () => {
  const doughnut = document.getElementById('chartjs-doughnut-chart');

  const getOptions = () => ({
    type: 'doughnut',
    data: {
      datasets: [
        {
          data: [5, 3, 2, 1, 1],
          backgroundColor: [
            utils.rgbaColor(utils.getColor('facebook'), 0.75),
            utils.rgbaColor(utils.getColor('youtube'), 0.75),
            utils.rgbaColor(utils.getColor('twitter'), 0.75),
            utils.rgbaColor(utils.getColor('linkedin'), 0.75),
            utils.rgbaColor(utils.getColor('github'), 0.75)
          ],
          borderWidth: 1,
          borderColor: utils.getGrays()['100']
        }
      ],

      labels: ['Facebook', 'Youtube', 'Twitter', 'Linkedin', 'GitHub']
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
      maintainAspectRatio: false
    }
  });

  chartJsInit(doughnut, getOptions);
};

export default chartDoughnut;
