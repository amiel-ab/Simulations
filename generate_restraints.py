import os
import argparse

parser = argparse.ArgumentParser(description = "Take an input gro structure, from which you can select multiple residues using -r. These residues will have restraint coordinates for x, y and z written. These are written at 0 by default, but this can be changed using the -x, -y and -z flags.", epilog = "Please note that this script cannot distinguish between partially provided residue names. If, for example, you simple provide the letter 'A', every residue containing that letter will have restraint coordinates set.")

# -c INPUTFILE -o OUTPUTFILE -x DIM -y DIM -z DIM --help
parser.add_argument("-c", "--input", help = "<.gro> input structure file", required = True)
parser.add_argument("-o", "--output", help = "<.gro> desired output .gro file (default = 'restraints.gro') (opt.)", default = "restraints.gro")
parser.add_argument("-r", "--residue", action = "append", help = "<str> residues to restrain (call multiple times if needed)", required = True)
parser.add_argument("-x", "--x", help = "<float> nm coordinate (default = 0) (opt.)", type=float, default = 0)
parser.add_argument("-y", "--y", help = "<float> nm coordinate (default = 0) (opt.)", type=float, default = 0)
parser.add_argument("-z", "--z", help = "<float> nm coordinate (default = 0) (opt.)", type=float, default = 0)


args = parser.parse_args()

reader = open(args.input, "r").read()
if any(residue not in reader for residue in args.residue):
    raise ValueError("One or more of your selected residues was not found in the input .gro file.")

line_no = 0
changes = 0
with open(args.output, "w") as writer:
    for line in open(args.input, "r").readlines():
        if line_no < 2:
            writer.write(line)
            line_no += 1
            continue
        else:
            if any(residue in line for residue in args.residue):
                restrained_line=[]
                restrained_line.append(line[0:20])
                restrained_line.append("{:06.3f}".format(args.x))
                restrained_line.append("{:06.3f}".format(args.y))
                restrained_line.append("{:06.3f}".format(args.z))
                s = "  "
                writer.write(s.join(restrained_line) + "\n")
                changes += 1
                line_no+=1
            else:
                line_no+=1
                writer.write(line)

print("\nRestraints saved as " + args.output + ". " + str(changes) + " atoms were restrained at x=" + str(args.x) + ", y=" + str(args.y) + ", and z=" + str(args.z) + ".\n")
