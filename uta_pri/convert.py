# -*- coding: utf-8 -*-
import sys

# PSPの並び 方向キー= 0x10, 上三角,右丸,下バツ,左四角
# musicaruino
# 方向キー= 0x10,三角=0x1,丸=0x2,バツ=0x4,四角=0x8,LED=0x20
# play.pyのノート(最後に小節区切り)
# template_names = ["arrow_template.png","tri_template.png","o_template.png","x_template.png"]

map_note = [0x10, 0x1, 0x2, 0x4, 0x20]

# 25ms後にフラグをクリアする
time_mergine = 25

for line in open(sys.argv[1],"r"):
    if line[0] == '#':
        continue
    line_split = line.split(':')
    time = int(line_split[0])
    str_arr = line_split[1].replace("[", "").replace("]","").lstrip().rstrip().split(',')
    int_arr = map(lambda note: int(note), str_arr)
    #print "//" + str(time) # for debug
    #print "//" + str(int_arr) # for debug
    bit = 0
    for note in int_arr:
        bit |= map_note[note]
    int_data = bit * 0x1000000
    int_data += time
    #print "//%08x" % (int_data) # for debug
    int_low = int_data & 0xffff
    int_high = (int_data >> 16) & 0xffff
    print "0x%04x, 0x%04x," % (int_high, int_low)
    int_data = time + time_mergine
    int_low = int_data & 0xffff
    int_high = (int_data >> 16) & 0xffff
    print "0x%04x, 0x%04x," % (int_high, int_low)

# エンドマークをつける
int_data = 0xff * 0x1000000
int_data += time
int_low = int_data & 0xffff
int_high = (int_data >> 16) & 0xffff
print "0x%04x, 0x%04x," % (int_high, int_low)
