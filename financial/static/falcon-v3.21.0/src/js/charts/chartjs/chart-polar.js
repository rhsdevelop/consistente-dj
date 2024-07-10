import utils from '../../utils';
import { chartJsDefaultTooltip, chartJsInit } from './chartjs-utils';

/* -------------------------------------------------------------------------- */
/*                            Chart Polar                                  */
/* -------------------------------------------------------------------------- */
const chartPolar = () => {
  const polar = document.getElementById('chartjs-polar-chart');

  const getOptions = () => ({
    type: 'polarArea',
    data: {
      datasets: [
        {
          data: [10, 20, 50, 40, 30],
          backgroundColor: [
            utils.rgbaColor(utils.getColor('facebook'), 0.5),
            utils.rgbaColor(utils.getColor('youtube'), 0.5),
            utils.rgbaColor(utils.getColor('twitter'), 0.5),
            utils.rgbaColor(utils.getColor('linkedin'), 0.5),
            utils.rgbaColor(utils.getColor('success'), 0.5)
          ],
          borderWidth: 1,
          borderColor: utils.getGrays()['400']
        }
      ],

      labels: ['Facebook', 'Youtube', 'Twitter', 'Linkedin', 'Medium']
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
      maintainAspectRatio: false,
      scales: {
        r: {
          grid: {
            color: utils.getGrays()['300']
          }
        }
      }
    }
  });

  chartJsInit(polar, getOptions);
};

export default chartPolar;
