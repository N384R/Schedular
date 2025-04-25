# -*- coding: utf-8 -*-

import platform
import json
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from .components.pie_chart import PieChart
from .components.matrix import Matrix
from .components.time_control_panel import TimeControlPanel
from .components.font_control_panel import FontControlPanel
from .components.task_control_panel import TaskControlPanel


def register_component(name):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, '_components'):
                self._components = {}
            component = func(self, *args, **kwargs)
            self._components[name] = component
            return component
        return wrapper
    return decorator


def register_panel(name):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, '_panels'):
                self._panels = {}
            panel = func(self, *args, **kwargs)
            self._panels[name] = panel
            return panel
        return wrapper
    return decorator


class Content:
    def __init__(self, fig, task_manager):
        self.fig = fig
        self.task_manager = task_manager
        self._setup_components()

    @register_component('pie_chart')
    def _create_pie_chart(self, ax):
        return PieChart(ax)

    @register_component('matrix')
    def _create_matrix(self, ax):
        matrix = Matrix(ax)
        matrix.setup_interaction(self.task_manager, self._update_plots)
        return matrix

    def _setup_components(self):
        axes = plt.subplots(1, 2, figsize=(17, 10))[1]
        self._create_pie_chart(axes[0])
        self._create_matrix(axes[1])
        plt.subplots_adjust(left=0.05, right=0.95,
                            top=0.95, bottom=0.25, wspace=0.2)

    def _update_plots(self, total_minutes):
        self.task_manager.recalculate_time(total_minutes)
        for component in self._components.values():
            component.update(self.task_manager)
        self.fig.canvas.draw()


class Panel:
    def __init__(self, fig, task_manager, update_plots_callback):
        self.fig = fig
        self.task_manager = task_manager
        self._setup_panels(update_plots_callback)

    @register_panel('time')
    def _create_time_panel(self, update_plots_callback):
        return TimeControlPanel(
            self.fig,
            update_plots_callback,
            self.task_manager.available_minutes
        )

    @register_panel('font')
    def _create_font_panel(self):
        return FontControlPanel(
            self.fig,
            self._update_font_size
        )

    @register_panel('task')
    def _create_task_panel(self):
        return TaskControlPanel(
            self.fig,
            self._add_task,
            self._reset
        )

    def _setup_panels(self, update_plots_callback):
        self._create_time_panel(update_plots_callback)
        self._create_font_panel()
        self._create_task_panel()

    def _update_font_size(self, font_mult):
        plt.rcParams['font.size'] = self._panels['font'].font_size * font_mult
        self.fig.canvas.draw_idle()

    def _add_task(self, task_data):
        self.task_manager.add_task(task_data)
        self._panels['time'].update_minutes(
            self.task_manager.available_minutes)

    def _reset(self):
        self.task_manager.reset()
        self._panels['time'].update_minutes(
            self.task_manager.available_minutes)


class EisenhowerVisualizer:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.fig = None
        self._setup_fonts()

    def _setup_fonts(self):
        config = self._get_config()
        self.base_font_size = config['font_size']

        extension = ".ttf" if platform.system() == "Windows" else ".otf"
        font_path = f"./eisenhower/fonts/Maplestory Light{extension}"
        fm.fontManager.addfont(font_path)
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = self.base_font_size
        plt.rcParams['axes.unicode_minus'] = False

    def _get_config(self):
        config_path = os.path.join(os.path.dirname(
            __file__), 'config', 'properties.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config

    def setup_initial_plot(self):
        self.fig = plt.figure(figsize=(17, 10))
        content = Content(self.fig, self.task_manager)
        panel = Panel(self.fig, self.task_manager, content._update_plots)
        content._update_plots(self.task_manager.available_minutes)

    def show(self):
        self.setup_initial_plot()
        plt.show()
