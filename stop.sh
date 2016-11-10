#!/bin/bash
ps aux | grep python | grep social | awk '{print $2}' | xargs kill -9
