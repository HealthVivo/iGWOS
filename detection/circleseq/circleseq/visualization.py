import svgwrite
import sys
import os

box_size = 15
v_spacing = 3

colors = {'G': '#F5F500', 'A': '#FF5454', 'T': '#00D118', 'C': '#26A8FF', 'N': '#B3B3B3', '-': '#B3B3B3'}


def parseSitesFile(infile):
    offtargets = []
    with open(infile, 'r') as f:
        # f.readline()
        for line in f:
            line = line.rstrip('\n')
            line_items = line.split('\t')
            offtarget_sequence = line_items[11]
            offtarget_reads = line_items[4]
            ref_seq = line_items[18]
            realigned_ref_seq = line_items[19]
            if offtarget_sequence != '':
                offtargets.append({'seq': offtarget_sequence.strip(),
                                   'reads': int(offtarget_reads.strip()),
                                   'realigned_ref_seq': realigned_ref_seq.strip()})
    offtargets = sorted(offtargets, key=lambda x: x['reads'], reverse=True)
    return offtargets, ref_seq


def visualizeOfftargets(infile, outfile, title=None):

    output_folder = os.path.dirname(outfile)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get offtargets array from file
    offtargets, ref_seq = parseSitesFile(infile)

    # Initiate canvas
    dwg = svgwrite.Drawing(outfile + '.svg', profile='full', size=(u'100%', 100 + len(offtargets)*(box_size + 1)))

    if title is not None:
        # Define top and left margins
        x_offset = 20
        y_offset = 50
        dwg.add(dwg.text(title, insert=(x_offset, 30), style="font-size:20px; font-family:Courier"))
    else:
        # Define top and left margins
        x_offset = 20
        y_offset = 20

    # Draw ticks
    tick_locations = [1, len(ref_seq)]
    tick_locations += range(len(ref_seq) + 1)[::10][1:]
    for x in tick_locations:
        dwg.add(dwg.text(str(x), insert=(x_offset + (x - 1) * box_size + 2, y_offset - 2), style="font-size:10px; font-family:Courier"))

    # Draw reference sequence row
    for i, c in enumerate(ref_seq):
        y = y_offset
        x = x_offset + i * box_size
        dwg.add(dwg.rect((x, y), (box_size, box_size), fill=colors[c]))
        dwg.add(dwg.text(c, insert=(x + 3, y + box_size - 3), fill='black', style="font-size:15px; font-family:Courier"))

    dwg.add(dwg.text('Reads', insert=(x_offset + box_size * len(ref_seq) + 16, y_offset + box_size - 3), style="font-size:15px; font-family:Courier"))

    # Draw aligned sequence rows
    y_offset += 10  # leave some extra space after the reference row
    for j, seq in enumerate(offtargets):
        realigned_ref_seq =  offtargets[j]['realigned_ref_seq']
        k = 0
        y = y_offset + j * box_size
        for i, (c, r) in enumerate(zip(seq['seq'], realigned_ref_seq)):
            x = x_offset + k * box_size
            if r == '-':
                if 0 < k < len(realigned_ref_seq):
                    x = x_offset + (k - 0.25) * box_size
                    dwg.add(dwg.rect((x, box_size * 1.4 + y), (box_size*0.6, box_size*0.6), fill=colors[c]))
                    dwg.add(dwg.text(c, insert=(x+1, 2 * box_size + y - 2), fill='black', style="font-size:10px; font-family:Courier"))

            elif c == r or r == 'N':
                 dwg.add(dwg.text(u"\u2022", insert=(x + 4.5, 2 * box_size + y - 4), fill='black', style="font-size:10px; font-family:Courier"))
                 k += 1
            else:
                dwg.add(dwg.rect((x, box_size + y), (box_size, box_size), fill=colors[c]))
                dwg.add(dwg.text(c, insert=(x + 3, 2 * box_size + y - 3), fill='black', style="font-size:15px; font-family:Courier"))
                k += 1


        reads_text = dwg.text(str(seq['reads']), insert=(box_size * (len(ref_seq) + 1) + 20, y_offset + box_size * (j + 2) - 2), fill='black', style="font-size:15px; font-family:Courier")
        dwg.add(reads_text)

    dwg.save()




# def parseSitesFile(infile):
#     offtargets = []
#     with open(infile, 'r') as f:
#         f.readline()
#         for line in f:
#             line = line.rstrip('\n')
#             line_items = line.split('\t')
#             offtarget_sequence = line_items[11]
#             offtarget_reads = line_items[4]
#             ref_seq = line_items[18]
#             if offtarget_sequence != '':
#                 offtargets.append({'seq': offtarget_sequence.strip(),
#                                    'reads': int(offtarget_reads.strip())})
#     offtargets = sorted(offtargets, key=lambda x: x['reads'], reverse=True)
#     return offtargets, ref_seq
#
# #
# def visualizeOfftargets(infile, outfile, title=None):
#
#     output_folder = os.path.dirname(outfile)
#     if output_folder and not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#
#     # Get offtargets array from file
#     offtargets, ref_seq = parseSitesFile(infile)
#
#     # Initiate canvas
#     dwg = svgwrite.Drawing(outfile + '.svg', profile='full', size=(u'100%', len(offtargets)*(box_size + 1)))
#
#     if title is not None:
#         # Define top and left margins
#         x_offset = 20
#         y_offset = 50
#         dwg.add(dwg.text(title, insert=(x_offset, 30), style="font-size:20px; font-family:Courier"))
#     else:
#         # Define top and left margins
#         x_offset = 20
#         y_offset = 20
#
#     # Draw ticks
#     tick_locations = [1, len(ref_seq)]
#     tick_locations += range(len(ref_seq) +1)[::10][1:]
#     for x in tick_locations:
#         dwg.add(dwg.text(str(x), insert=(x_offset + (x - 1) * box_size + 2, y_offset - 2), style="font-size:10px; font-family:Courier"))
#
#     # Draw reference sequence row
#     for i, c in enumerate(ref_seq):
#         y = y_offset
#         x = x_offset + i * box_size
#         dwg.add(dwg.rect((x, y), (box_size, box_size), fill=colors[c]))
#         dwg.add(dwg.text(c, insert=(x + 3, y + box_size - 3), fill='black', style ="font-size:15px; font-family:Courier"))
#
#
#     dwg.add(dwg.text('Reads', insert=(x_offset + box_size * len(ref_seq) + 16, y_offset + box_size - 3), style="font-size:15px; font-family:Courier"))
#
#     # Draw aligned sequence rows
#     y_offset += 10 # leave some extra space after the reference row
#     for j, seq in enumerate(offtargets):
#         if len(seq['seq']) == len(ref_seq): # mismatches and/or deletions
#             y = y_offset + j * box_size
#             for i, c in enumerate(seq['seq']):
#                 x = x_offset + i * box_size
#                 if c == ref_seq[i] or ref_seq[i] == 'N':
#                     dwg.add(dwg.text(u"\u2022", insert=(x + 4.5, 2 * box_size + y - 4), fill='black', style="font-size:10px; font-family:Courier"))
#                 else:
#                     dwg.add(dwg.rect((x, box_size + y), (box_size, box_size), fill=colors[c]))
#                     dwg.add(dwg.text(c, insert=(x + 3, 2 * box_size + y - 3), fill='black', style="font-size:15px; font-family:Courier"))
#         else: # This is where we would visualize the insertions.
#             pass
#         reads_text = dwg.text(str(seq['reads']), insert=(box_size * (len(ref_seq) + 1) + 20, y_offset + box_size * (j + 2) - 2), fill='black', style="font-size:15px; font-family:Courier")
#         dwg.add(reads_text)
#
#     dwg.save()


def main():
    if len(sys.argv) >= 3:
        if len(sys.argv) == 4:
            title = sys.argv[3]
        else:
            title = None
        visualizeOfftargets(sys.argv[1], sys.argv[2], title=title)
    else:
        print 'Usage: python visualization.py INFILE OUTFILE [TITLE]'


if __name__ == '__main__':
    main()