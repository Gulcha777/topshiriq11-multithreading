#!/usr/bin/env bash
set -e
git init -b main
git add .
git commit -m "Topshiriq 11: Multithreading, Race Condition, ThreadPool va Deadlock"
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Gulcha777/topshiriq11-multithreading.git
git push -u origin main
