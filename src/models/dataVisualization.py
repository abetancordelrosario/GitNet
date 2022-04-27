import matplotlib.pyplot as plt


class dataVisualization:

    def plot_barChart(data: dict, title: str):
        fig, ax = plt.subplots(figsize=(12,6))

        data = dict(data)
        xaxis_list: list = list(data.values())
        yaxis_list: list = list(data.keys())
        ax.barh(yaxis_list, xaxis_list)

        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)

        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')

        ax.xaxis.set_tick_params(pad = 5)
        ax.yaxis.set_tick_params(pad = 10)

        ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)

        ax.invert_yaxis()

        for i in ax.patches:
            plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')

        ax.set_title(title,
             loc ='left', )

        fig.text(0.9, 0.15, 'GitNet', fontsize = 12,
         color ='grey', ha ='right', va ='bottom',
         alpha = 0.7)    
        
        plt.savefig("img/plot.png", bbox_inches="tight")


    