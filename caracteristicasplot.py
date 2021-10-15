import numpy as np

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.pyplot import tight_layout


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def example_data():
    # The following data is from the Denver Aerosol Sources and Health study.
    # See doi:10.1016/j.atmosenv.2008.12.017
    #
    # The data are pollution source profile estimates for five modeled
    # pollution sources (e.g., cars, wood-burning, etc) that emit 7-9 chemical
    # species. The radar charts are experimented with here to see if we can
    # nicely visualize how the modeled source profiles change across four
    # scenarios:
    #  1) No gas-phase species present, just seven particulate counts on
    #     Sulfate
    #     Nitrate
    #     Elemental Carbon (EC)
    #     Organic Carbon fraction 1 (OC)
    #     Organic Carbon fraction 2 (OC2)
    #     Organic Carbon fraction 3 (OC3)
    #     Pyrolized Organic Carbon (OP)
    #  2)Inclusion of gas-phase specie carbon monoxide (CO)
    #  3)Inclusion of gas-phase specie ozone (O3).
    #  4)Inclusion of both gas-phase species is present...
    x1 =np.array([[681, 6.16, 5108.60, 7.50, 0, 369.05],
                [964, 8.72, 4916.91, 5.10, 0, 452.28],
                [1316, 11.91, 4661.70, 3.54, 0, 481.67],
                [1552, 14.05, 4444.05, 2.86, 0, 622.31],
                [1779, 16.10, 4213.95, 2.37, 0, 647.79],
                [2041, 18.47, 3894.21, 1.91, 0, 660.62]])
    x2 =np.array([[663, 6.00, 4842.66, 7.30, 41, 289.64],
                [702, 6.35, 4812.36, 6.86, 36, 354.84],
                [869, 7.86, 4691.40, 5.40, 24, 376.11],
                [1266, 11.46, 4338.54, 3.43, 6, 539.14]])
    x3 =np.array([[1834, 16.60, 4263.90, 2.32, 1, 646.80],
                [2239, 20.26, 3824.60, 1.71, 0, 670.42],
                [2526, 22.86, 3412.15, 1.35, 0, 744.29],
                [1211, 10.96, 4493.80, 3.71, 8, 530.00],
                [1539, 13.93, 4093.45, 2.66, 0, 566.54],
                [1780, 16.11, 3673.40, 2.06, 0, 638.14]])
    
    from sklearn.preprocessing import normalize
    
    X1_scaled = normalize(x1, axis=0, norm='l2')
    X2_scaled = normalize(x2, axis=0, norm='l2')
    X3_scaled = normalize(x3, axis=0, norm='l2')

    data = [
        ['Quantidade\nTotal de Áudios','Média de\nÁudios por\nLigação','Duração\nTotal','Média de\nDuração dos\nÁudios','Quantidade\nde Áudios\n>20','Tempo\ntotal de\nrequisições'],
        ('auditok', X1_scaled ),
        ('webrtcvad', X2_scaled ),
        ('pyAudioAnalysis', X3_scaled )
    ]
    return data


if __name__ == '__main__':
    N = 6
    theta = radar_factory(N, frame='polygon')

    data = example_data()
    spoke_labels = data.pop(0)

    fig, axes = plt.subplots(figsize=(10, 10), dpi=300, nrows=1, ncols=3,
                             subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.4, hspace=0.4, top=0.25, bottom=0.05)

    colors = ['b', 'r', 'g', 'm', 'y', 'c', 'tab:blue', 'tab:orange', 'tab:purple', 'tab:pink','black', 'darkolivegreen', 'lime', 'indigo', 'gold', 'darkcyan']
    cont=0
    # Plot the four cases from the example data on separate axes
    for ax, (title, case_data) in zip(axes.flat, data):
        ax.set_rgrids([])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        for d in case_data:
            ax.plot(theta, d, color=colors[cont])
            cont+=1
            ax.fill(theta, d, alpha=0)
        ax.set_varlabels(spoke_labels)
        ax.xaxis.set_tick_params(pad=19)
        
    tight_layout()
    plt.show()

    # Create a color palette
    fig, axes = plt.subplots(dpi=300)
    labels = ['et:30',
            'et:35',
            'et:40',
            'et:45',
            'et:50',
            'et:55',
            'ag:0',
            'ag:1',
            'ag:2',
            'ag:3',
            'sw:0.3|w:0.1',
            'sw:0.3|w:0.2',
            'sw:0.3|w:0.3',
            'sw:0.5|w:0.1',
            'sw:0.5|w:0.2',
            'sw:0.5|w:0.3']
    palette = dict(zip(labels, colors))
    # Create legend handles manually
    handles = [mpatches.Patch(color=palette[x], label=x) for x in palette.keys()]
    # Create legend
    plt.legend(handles=handles)
    # Get current axes object and turn off axis
    plt.gca().set_axis_off()
    plt.show()