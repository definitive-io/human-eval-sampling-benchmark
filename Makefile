.PHONY: default clean install run-bench plot

# Specify the shell to use
SHELL := /bin/bash

default: clean install run-bench plot

clean:
	rm -r data || true
	mkdir -p data

install:
	if [ ! -d "human-eval" ]; then \
		git clone https://github.com/definitive-io/human-eval; \
	fi
	pip install -r requirements.txt

run-bench:
	python 1_run_eval.py

plot:
	python 2_plot_performance.py
