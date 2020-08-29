from io import BytesIO
import json
import random

from ndspy import lz10, narc, rom

from time import time
start_time = time()

chest_contents_list = [10, 10, 10, 10, 10, 10, 10, 25, 1, 1, 25, 12, 25, 15, 125, 35, 129, 119, 34, 118, 19, 0, 47, 125, 46, 125, 6, 6, 6, 45, 125, 20, 45, 125, 117, 98, 84, 125, 126, 34, 45, 126, 47, 35, 46, 126, 21, 9, 105, 117, 26, 125, 6, 6, 27, 106, 126, 22, 135, 135, 125, 126, 45, 1, 8, 46, 9, 33, 15, 45, 125, 47, 25, 97, 14, 134, 15, 134, 25, 45, 46, 117, 119, 1, 46, 32, 15, 1, 118, 15, 47, 125, 7, 45, 125, 31, 15, 9, 1, 1, 47, 25, 47, 9, 47, 45, 113, 46, 126, 9, 125, 126, 45, 47, 3, 60, 103, 47, 99, 133, 133, 45, 47, 125, 38, 45, 46, 79, 125, 13, 9, 45, 77, 47, 45, 47, 46, 102, 10, 27, 46, 47, 27, 47, 82, 25, 121, 122, 123, 124, 46, 45, 25, 25, 9, 45, 78, 47, 46, 86, 46, 45, 46, 47, 26, 9, 46, 46]
random.shuffle(chest_contents_list)

game_rom = rom.NintendoDSRom.fromFile('ph_dpad.nds')

json_file = open('json/chests_v5.json')
chests_json = json.load(json_file)
json_file.close()

narc_files = {}

for location in chests_json:
    for zmb in chests_json[location]:
        map_number = zmb.split('.z')[0][len(zmb.split('.z')[0])-2:]
        narc_filename = f'Map/{location}/map{map_number}.bin'
        narc_file = narc.NARC(lz10.decompress(game_rom.getFileByName(narc_filename)))
        zmb_file = (narc_file.getFileByName(f'zmb/{zmb}'))
        for chest in chests_json[location][zmb]:
            offset = int(chest['location'], 0) + 8
            zmb_file = zmb_file[:offset] + bytes([chest_contents_list.pop(0)]) + zmb_file[offset+1:]
            # zmb_file.seek(offset)
            # zmb_file.write(bytes([chest_contents_list.pop(0)]))
        narc_file.setFileByName(f'zmb/{zmb}', zmb_file)
        narc_files[narc_filename] = narc_file


print('Done!')
        # this line causes 50+ extra seconds of execution time
        # game_rom.setFileByName(narc_filename, lz10.compress(narc_file.save()))
    # game_rom.setFileByName(f'Map/{location}/map{map_number}.bin', lz10.compress(narc_file.save()))
# from pprint import pprint
# pprint(narc_files)

print(f'Runtime: {time() - start_time} seconds')
for narc in narc_files:
    print(narc)
    game_rom.setFileByName(narc, lz10.compress(narc_files[narc].save()))

print(f'Runtime: {time() - start_time} seconds')
game_rom.saveToFile('randomized.nds')
