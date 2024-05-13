#!/bin/bash


sleep 10

uvicorn src.main:app --host control-gastos --reload