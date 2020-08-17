import os
import subprocess
import sys

src_dir = os.path.abspath("../")
icons_dir = os.path.abspath("../icons")
qrc = os.path.abspath("../icons.qrc")
out = os.path.abspath("../gui/rc/icons_rc.py")
ui_folder = os.path.abspath("../gui/ui/")
python = sys.executable

wrapper = """
<RCC>
    <qresource prefix="/icon">
        {file_list}
    </qresource>
</RCC>
"""

file_list_item = """
        <file alias="{alias}">{filepath}</file>
"""


if __name__ == "__main__":

    print("Compiling icons.qrc file")

    file_list = ""
    for root, dirs, files in os.walk(icons_dir):
        for file in files:
            fpath = os.path.join(root, file)
            from_src = os.path.relpath(fpath, src_dir)
            file_list += file_list_item.format(alias=from_src, filepath=from_src)

    qrc_contents = wrapper.format(file_list=file_list).replace("\\", "/")

    with open(qrc, "w") as icons_file:
        icons_file.write(qrc_contents)

    print("Compiling Resource Files... ")

    d = os.path.dirname(out)
    if not os.path.exists(d):
        os.makedirs(d)

    rcc = python[:-len('python.exe')] + os.path.join('pyside2-rcc.exe')

    with open(out, 'w') as fout:
        proc = subprocess.Popen([rcc, qrc], stdout=fout)
        return_code = proc.wait()

    print("Reworking Resource Files...")
    # read in all lines from the rc file
    with open(out, 'r') as f:
        lines = f.readlines()

    # write out only the non-empty lines back to the rc file
    with open(out, 'w') as f:
        for line in lines:
            if line.strip():
                f.write(line)

    uic = python[:-len('python.exe')] + os.path.join('pyside2-uic.exe')

    print("Removing existing compiled UI files...")
    for file in os.listdir(ui_folder):
        if file.startswith("ui_") and file.endswith(".py"):
            print("\t" + file)
            os.remove(os.path.join(ui_folder, file))

    print("Compiling UI files... ")
    for file in os.listdir(ui_folder):
        if file.endswith(".ui"):
            srcFile = os.path.join(ui_folder, file)
            dstFile = os.path.join(ui_folder, "ui_{}.py".format(file[:-3]))
            print("\t" + file)

            with open(dstFile, 'w') as fout:
                if python:
                    args = [python, uic, srcFile]
                else:
                    args = [uic, srcFile]
                proc = subprocess.Popen(args, stdout=fout)
                return_code = proc.wait()

            with open(dstFile, 'r') as fin:
                contents = fin.read()

            with open(dstFile, 'w') as fout:
                fout.write(contents.replace("import icons_rc", "import gui.rc.icons_rc as icons_rc"))

    print("Done")
