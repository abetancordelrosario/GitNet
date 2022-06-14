import re
from graph_tool import VertexPropertyMap, graph_tool
import matplotlib.pyplot as plt
import numpy as np

from models.interestGraph import interestGraph


class dataVisualization:
    '''
    Visualize the results unsing graphics generated with
    matplotlib.

    The graphics could be a horinzontal bar chart, pie chart or
    linear regression chart.
    '''

    def plot_barChart(self, data: dict, title: str) -> None:
        fig, ax = plt.subplots(figsize=(12,6))

        data = data[:10]
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
        plt.close(fig)


    def plot_pieChart(self, data: dict) -> None:
        data = data[:10]
        labels: list = [] 
        sizes: list = []
        for key, value in data:
            repo = re.findall(r'(?<=/)[^.]*', key)
            if repo:
                labels.append(repo[0])
                sizes.append(value)
            else:
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
        plt.close(fig1)

    def fork_relationship(self, result_data: list, graph: interestGraph) -> None:
        v_repo_st: VertexPropertyMap = graph.get_repo_st()
        v_name: VertexPropertyMap = graph.get_name()
        v_repo_forks: VertexPropertyMap = graph.get_repo_forks()

        data = dict(result_data[:100])
        repos_names: list = list(data.keys())
        repos = [graph_tool.util.find_vertex(graph.g, v_name, name) for name in repos_names]
        stargazers = [v_repo_st[repo[0]] for repo in repos]
        forks = [v_repo_forks[repo[0]] for repo in repos]
        self.plot_linear_regression(forks, stargazers, "stargazers")

    def plot_linear_regression(self, forks: list, users: list, type: str) -> None:
        (m, b) = np.polyfit(users, forks, 1)

        yp = np.polyval([m, b], users)
        plt.plot(users, yp)
        plt.grid(True)
        plt.scatter(users,forks)
        plt.savefig(f"img/fork-{type}.png")