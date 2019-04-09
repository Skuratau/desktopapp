# -*- coding: utf-8 -*-
# kivy.require('1.10.1') # replace with your current kivy version !


import os

os.environ['KIVY_IMAGE'] = 'pil,sdl2'
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from scipy.optimize import fsolve, root
from numpy import linspace, zeros, fromiter
from pprint import pprint
from pandas import DataFrame
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt




def split_float_into_parts(number, n_parts):
    return linspace(0, number, n_parts + 1)[1:]


# refactor
def set_of_dict_to_dict(initial_list, set_of_keys=[]):
    data_set = {}
    for key in set_of_keys:
        data_set[key] = []
    for data_frame in initial_list:
        for key in set_of_keys:
            data_set[key].append(data_frame[key])
    return data_set


class AppGrid(GridLayout):
    ds = {}

    def get_chart_data(self):
        '''
        a = float(self.ids.a.text)
        b = float(self.ids.b.text)
        d = float(self.ids.d.text)
        px = float(self.ids.px.text)
        py = float(self.ids.py.text)
        f = float(self.ids.f.text)
        p1 = float(self.ids.p1.text)
        p2 = float(self.ids.p2.text)
        m = float(self.ids.m.text)
        chunks = float(self.ids.chunks.text)

        a = 2.9
        b = 0.67
        d = 1.78
        px = -9500
        py = -11500
        f = 0.6
        p1 = 16958
        p2 = 23030
        m = -4360
        chunks = 1000

        '''

        a = 3
        b = 0.5
        d = 3
        px = 1000
        py = -11150
        f = 0.5
        p1 = 16958
        p2 = 23030
        m = -4360
        chunks = 10


        px_chart_data = []
        for chunk in split_float_into_parts(px, chunks):
            px_chart_data.append({
                'a': a,
                'b': b,
                'd': d,
                'px': chunk,
                'py': py,
                'f': f,
                'p1': p1,
                'p2': p2,
                'm': m
            })
        py_chart_data = []
        for chunk in split_float_into_parts(py, chunks):
            py_chart_data.append({
                'a': a,
                'b': b,
                'd': d,
                'px': px,
                'py': chunk,
                'f': f,
                'p1': p1,
                'p2': p2,
                'm': m
            })
        m_chart_data = []
        for chunk in split_float_into_parts(m, chunks):
            m_chart_data.append({
                'a': a,
                'b': b,
                'd': d,
                'px': px,
                'py': py,
                'f': f,
                'p1': p1,
                'p2': p2,
                'm': chunk
            })
        return {
            'px_chart_data': px_chart_data,
            'py_chart_data': py_chart_data,
            'm_chart_data': m_chart_data
        }

    def equations(self, p):
        e1x = p[0]
        e2x = p[1]
        ey = p[2]
        f = zeros(3)
        f[0] = self.ds['px'] + \
               self.ds['p1'] * self.ds['f'] * self.ds['a'] * self.ds['b'] / 3 * (
                   (self.ds['a'] / 3 + ey) / ((self.ds['a'] / 3 + ey) ** 2 + e1x ** 2) ** (1 / 2) +
                   ey / (ey ** 2 + e1x ** 2) ** (1 / 2) -
                   (self.ds['a'] / 3 - ey) / ((self.ds['a'] / 3 - ey) ** 2 + e1x ** 2) ** (1 / 2)) + \
               self.ds['p2'] * self.ds['f'] * self.ds['a'] * self.ds['b'] / 3 * (
                   (self.ds['a'] / 3 + ey) / ((self.ds['a'] / 3 + ey) ** 2 + e2x ** 2) ** (1 / 2) +
                   ey / (ey ** 2 + e2x ** 2) ** (1 / 2) -
                   (self.ds['a'] / 3 - ey) / ((self.ds['a'] / 3 - ey) ** 2 + e2x ** 2) ** (1 / 2))

        f[1] = self.ds['py'] - \
               self.ds['p1'] * self.ds['f'] * self.ds['a'] * self.ds['b'] / 3 * (
                   e1x / ((self.ds['a'] / 3 + ey) ** 2 + e1x ** 2) ** (1 / 2) +
                   e1x / (ey ** 2 + e1x ** 2) ** (1 / 2) +
                   e1x / ((self.ds['a'] / 3 - ey) ** 2 + e1x ** 2) ** (1 / 2)) + \
               self.ds['p2'] * self.ds['f'] * self.ds['a'] * self.ds['b'] / 3 * (
                   e2x / ((self.ds['a'] / 3 + ey) ** 2 + e2x ** 2) ** (1 / 2) +
                   e2x / (ey ** 2 + e2x ** 2) ** (1 / 2) +
                   e2x / ((self.ds['a'] / 3 - ey) ** 2 + e2x ** 2) ** (1 / 2))

        f[2] = self.ds['m'] + \
               self.ds['d'] * self.ds['p2'] * self.ds['f'] * self.ds['a'] * self.ds['b'] / 6 * (
                   e2x / ((self.ds['a'] / 3 + ey) ** 2 + e2x ** 2) ** (1 / 2) +
                   e2x / (ey ** 2 + e2x ** 2) ** (1 / 2) +
                   e2x / ((self.ds['a'] / 3 - ey) ** 2 + e2x ** 2) ** (1 / 2)) + \
               self.ds['d'] * self.ds['p1'] * self.ds['f'] * self.ds['a'] * self.ds['b'] / 6 * (
                   e1x / ((self.ds['a'] / 3 + ey) ** 2 + e1x ** 2) ** (1 / 2) +
                   e1x / (ey ** 2 + e1x ** 2) ** (1 / 2) +
                   e1x / ((self.ds['a'] / 3 - ey) ** 2 + e1x ** 2) ** (1 / 2)) - \
               self.ds['a'] * self.ds['p1'] * self.ds['f'] * self.ds['a'] * self.ds['b'] / 9 * (
                   (self.ds['a'] / 3 + ey) / ((self.ds['a'] / 3 + ey) ** 2 + e1x ** 2) ** (1 / 2) +
                   (self.ds['a'] / 3 - ey) / ((self.ds['a'] / 3 - ey) ** 2 + e1x ** 2) ** (1 / 2)) - \
               self.ds['a'] * self.ds['p1'] * self.ds['f'] * self.ds['a'] * self.ds['b'] / 9 * (
                   (self.ds['a'] / 3 + ey) / ((self.ds['a'] / 3 + ey) ** 2 + e2x ** 2) ** (1 / 2) +
                   (self.ds['a'] / 3 - ey) / ((self.ds['a'] / 3 - ey) ** 2 + e2x ** 2) ** (1 / 2))
        return f

    def execute(self):
        try:
            self.ids.chart_data.clear_widgets()
        except:
            pass
        data_lake = self.get_chart_data()
        for source in ['px_chart_data', 'py_chart_data', 'm_chart_data']:
            counter = 0
            for chunk in data_lake[source]:
                self.ds = chunk
                system_result = fsolve(self.equations, (-1, -1, -1), factor=0.1,
                                       xtol=0.00001)  # xtol=float(self.ids.accuracy.text))
                pprint("Result:")
                pprint(system_result)
                pprint("Check:")
                pprint(self.equations(system_result))
                p_e1x_f = "%.3f" % system_result[0]
                p_e2x_f = "%.3f" % system_result[1]
                p_ey_f = "%.3f" % system_result[2]
                data_lake[source][counter].update({
                    'p_e1x_f': p_e1x_f,
                    'p_e2x_f': p_e2x_f,
                    'p_ey_f': p_ey_f})
                counter += 1
        px_data_frame = set_of_dict_to_dict(data_lake['px_chart_data'], ['px', 'p_e1x_f', 'p_e2x_f', 'p_ey_f'])
        py_data_frame = set_of_dict_to_dict(data_lake['py_chart_data'], ['py', 'p_e1x_f', 'p_e2x_f', 'p_ey_f'])
        m_data_frame = set_of_dict_to_dict(data_lake['m_chart_data'], ['m', 'p_e1x_f', 'p_e2x_f', 'p_ey_f'])


        gs = plt.GridSpec(3, 3)
        plt.subplot(gs[0, :])
        plt.tight_layout()
        plt.title('px')
        plt.plot('px', 'p_e1x_f', data=px_data_frame, marker='', color='m', linewidth=1, alpha=0.9, label='p_e1x_f')
        plt.plot('px', 'p_e2x_f', data=px_data_frame, marker='', color='y', linewidth=1, alpha=0.9,
                 label='p_e2x_f')
        plt.plot('px', 'p_ey_f', data=px_data_frame, marker='', color='k', linewidth=1, alpha=0.9,
                 label='p_ey_f')
        plt.subplot(gs[1, :])
        plt.title('py')
        plt.plot('py', 'p_e1x_f', data=py_data_frame, marker='', color='m', linewidth=1, alpha=0.9, label='p_e1x_f')
        plt.plot('py', 'p_e2x_f', data=py_data_frame, marker='', color='y', linewidth=1, alpha=0.9,
                 label='p_e2x_f')
        plt.plot('py', 'p_ey_f', data=py_data_frame, marker='', color='k', linewidth=1, alpha=0.9,
                 label='p_ey_f')
        plt.subplot(gs[2, :])
        plt.title('m')
        plt.plot('m', 'p_e1x_f', data=m_data_frame, marker='', color='m', linewidth=1, alpha=0.9, label='p_e1x_f')
        plt.plot('m', 'p_e2x_f', data=m_data_frame, marker='', color='y', linewidth=1, alpha=0.9,
                 label='p_e2x_f')
        plt.plot('m', 'p_ey_f', data=m_data_frame, marker='', color='k', linewidth=1, alpha=0.9,
                 label='p_ey_f')
        self.ids.chart_data.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        self.display.text = str('e1x = {}, e2x = {}, ey = {}'.format(p_e1x_f, p_e2x_f, p_ey_f))


'''
        #        try:
# except:
#            self.display.text = "Set all fields in correct format"
'''


class FmeeApp(App):
    def build(self):
        return AppGrid()


if __name__ == '__main__':
    FmeeApp().run()

