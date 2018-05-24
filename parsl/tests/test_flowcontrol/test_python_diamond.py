import time

import pytest

from parsl.app.app import App
from parsl.dataflow.dflow import DataFlowKernel
from parsl.tests.configs.local_ipp import config

config["sites"][0]["execution"]["block"]["init_blocks"] = 0
config["sites"][0]["execution"]["block"]["min_blocks"] = 0
config["sites"][0]["execution"]["block"]["max_blocks"] = 4
dfk = DataFlowKernel(config=config)


@App("python", dfk)
def diamond(sleep=0, inputs=[]):
    import time
    time.sleep(sleep)
    return sum(inputs)


@pytest.mark.local
@pytest.mark.skip('slow and does not assert anything')
def test_python(width=10):
    """Diamond pattern to scale from 0 -> 1 -> N -> 1 -> 0 """

    stage_1 = [diamond(sleep=60, inputs=[0])]

    stage_2 = []
    for i in range(0, width):
        stage_2.extend([diamond(sleep=20, inputs=stage_1)])

    stage_3 = [diamond(sleep=30, inputs=stage_2)]

    if not stage_3[0].done():
        time.sleep(30)
        for sitename in dfk.executors:
            print(dfk.executors[sitename].status())


if __name__ == "__main__":
    test_python()
