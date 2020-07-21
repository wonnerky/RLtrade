import numpy as np
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc

class Visualizer:

    def __init__(self):
        self.fig = None     # 캔버스 같은 역할을 하는 Matplotlib의 Figure 클래스 객체
        self.axes = None    # 차트를 그리기 위한 Matplotlib의 Axes 클래스 객체

    def prepare(self, chart_data):
        # 캔버스를 초기화하고 4개의 차트를 그릴 준비
        self.fig, self.axes = plt.subplots(nrows=4, ncols=1, facecolor='w', sharex=True)
        for ax in self.axes:
            # 보기 어려운 과학적 표기 비활성화
            ax.get_xaxis().get_major_formatter().set_scientific(False)
            ax.get_yaxis().get_major_formatter().set_scientific(False)
        # 차트 1. 일봉 차트
        self.axes[0].set_ylabel('Env.')     # y 축 레이블 표시
        # 거래량 가시화
        x = np.arange(len(chart_data))
        volume = np.array(chart_data)[:, -1].tolist()
        self.axes[0].bar(x, volume, color='b', alpha=0.3)
        # ohlc란 open, high, low, close의 약자로 이 순서로 구성된 2차원 배열
        ax = self.axes[0].twinx()
        ohlc = np.hstack((x.reshape(-1, 1), np.array(chart_data)[:, 1:-1]))
        # self.axes[0]에 봉 차트 출력
        # 양봉은 빨간색으로, 음봉은 파란색으로 표시
        candlestick_ohlc(ax, ohlc, colorup='r', colordown='b')

    def plot(self, epoch_str=None, num_epochs=None, epsilon=None, action_list=None, actions=None,
             num_stocks=None, outvals=None, exps=None, initial_balance=None, pvs=None):
        x = np.arange(len(actions))     # 모든 차트가 공유할 x축 데이터
        actions = np.array(actions)     # 에이전트의 행동 배열
        outvals = np.array(outvals)     # 정책 신경망의 출력 배열
        pvs_base = np.zeros(len(actions)) + initial_balance     # 초기 자본금 배열
        # 차트 2. 에이전트 상태 (행동, 보유 주식 수)
        colors = ['r', 'b']
        for actiontype, color in zip(action_list, colors):
            for i in x[actions == actiontype]:
                self.axes[1].axvline(i, color=color, alpha=0.1)     # 배경 색으로 행동 표시
        self.axes[1].plot(x, num_stocks, '-k')  # 보유 주식 수 그리기

