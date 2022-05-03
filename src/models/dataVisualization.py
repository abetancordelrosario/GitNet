import matplotlib.pyplot as plt


class dataVisualization:

    def plot_barChart(data: dict, title: str) -> None:
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
        
        plt.savefig("img/barChart.png", bbox_inches="tight")


    def plot_pieChart(data: dict, title: str) -> None:
        labels: list = [] 
        sizes: list = []
        for key, value in data:
            labels.append(key)
            sizes.append(value)
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#00FFFF',
                  '#A52A2A','#5F9EA0','#7FFF00','#D2691E','#6495ED']
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90)
        
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        
        ax1.axis('equal')  
        plt.tight_layout()
        plt.savefig("img/pieChart.png")
