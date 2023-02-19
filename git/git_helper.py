# 由于网络不是很好，经常pull，push就挂掉，但是反反复复提交又很麻烦，所以感觉做一些常用操作的封装会比较好

import argparse
import subprocess
from retry import retry
from func_timeout import func_timeout, func_set_timeout, FunctionTimedOut

parser = argparse.ArgumentParser()

parser.add_argument('--pull', action="store_true")
parser.add_argument('--push', action="store_true")

args = parser.parse_args()


@retry(BaseException, delay=5, tries=100)
def git_pull():
    # timeout 15secs or raise FunctionTimedOut exception
    @func_set_timeout(15)
    def _git_pull():
        subprocess.run("git pull", shell=True, check=True)

    try:
        _git_pull()
    except FunctionTimedOut:
        print("git pull timeout...")
        raise FunctionTimedOut


@retry(BaseException, delay=5, tries=100)
def git_push():
    # timeout 15secs or raise FunctionTimedOut exception
    @func_set_timeout(15)
    def _git_push():
        subprocess.run("git push", shell=True, check=True)
    try:
        _git_push()
    except FunctionTimedOut:
        print("git push timeout...")
        raise FunctionTimedOut


if __name__ == "__main__":
    if args.pull:
        git_pull()
    if args.push:
        git_push()
