from microhack.config import get_settings
from microhack.input import input
from microhack.output import output
from microhack.pipeline import pipeline

import pathway as pw

if __name__ == "__main__":
    get_settings()

    input_table = input()
    output_table = pipeline(input_table)
    output(output_table)

    pw.run(monitoring_level=pw.MonitoringLevel.ALL)
