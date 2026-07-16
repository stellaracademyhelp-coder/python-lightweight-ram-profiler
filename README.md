Python Lightweight RAM Profiler

A lightweight, zero-dependency, bare-metal RAM profiler written in pure Python. Designed to capture real-time hardware telemetry directly from the system kernel, bypassing C-compiler requirements.
Features

Zero-Dependency: Runs on standard Python libraries.

Bare-Metal Telemetry: Captures data directly from the system kernel.

Platform Agnostic: Native across Linux desktop and Android terminal environments (like Pydroid 3).

CSV Export: Logs data directly to a CSV file for post-analysis and visualization.


Quick Start

Clone this repository:
git clone https://github.com/stellaracademyhelp-coder/python-lightweight-ram-profiler.git


Run the profiler:

python profiler.py
Your RAM telemetry will be exported to ram_telemetry_log.csv.


Why This Project?

Engineered for hardware optimization, this tool provides the data necessary to understand software memory footprints in constrained environments. Part of the Stellar Tech Labs engineering suite.

License
Distributed under the MIT License. See LICENSE for more information.
