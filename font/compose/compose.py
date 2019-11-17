import os
import subprocess

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
TTF_FILE= f'{MODULE_DIR}/NotoColorEmoji.ttf'
BUILD_DIR = f'{MODULE_DIR}/png'

def run_cmd(args, cwd=None):
    result = subprocess.run(args, cwd=cwd)
    # print(result.stdout.decode('utf-8'))
    result.check_returncode()

def add_to_build(codepoint, path):
    print(f"add img for codepoint {codepoint}")
    run_cmd(['cp',path,f'{BUILD_DIR}/emoji_u{codepoint}.png'])

def build(outpath):
    print("copy imgs...")
    run_cmd(['make','clean'], cwd=MODULE_DIR)
    print("build font...")
    run_cmd(['make'], cwd=MODULE_DIR)
    run_cmd(['cp', TTF_FILE, outpath])

def build_font(pairs, outpath):
    for (codepoint, path) in pairs:
        add_to_build(codepoint, path)

    build(outpath)
