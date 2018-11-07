import os
import subprocess
import sys

def main():
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    os.makedirs(output_dir, exist_ok=True)
    os.utime(output_dir)

    curve_directories = ["I/", "V/"]

    [process_dir(input_dir, output_dir, d) for d in curve_directories]

def process_dir(input_dir, output_dir, directory):
    in_dir = os.path.join(input_dir, directory)
    out_dir = os.path.join(output_dir, directory)

    os.makedirs(out_dir, exist_ok=True)
    os.utime(out_dir)

    [process_file(input_dir, output_dir, directory, f) for f in sorted(os.listdir(in_dir))]

def process_file(input_dir, output_dir, directory, f):
    """
    1) Add the header
    2) Remove excess spacing
    3) Replace delimiting spaces with commas
    4) Remove any commas at the end of lines
    5) Remove any commas at beginning of lines
    """
    f = f[:-4]
    in_file = os.path.join(input_dir, directory, f)
    out_file = os.path.join(output_dir, directory, f)

    print(f)

    command = "echo 'time,mag,magerror' > '%s.csv' && cat '%s.dat' | tr -s ' ' | sed 's/ /,/g' | sed 's/,$$//g' | sed 's/^,//g' >> '%s.csv'" % (out_file, in_file, out_file)

    subprocess.call(command, shell=True)

if __name__ == "__main__":
    main()
