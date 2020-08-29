# pluck = temple of courage

import io
import os
import random
import sys
import ndspy.lz10
import ndspy.narc
import ndspy.rom

def enable_print():
	sys.stdout = sys.__stdout__

def disable_print():
	sys.stdout = open(os.devnull, 'w')

banlist = {"battle00", "battle01", "battle02", "battle03", "battle04",
		   "battle05", "battle06", "battle07", "battle08", "battle09",
		   "battle10", "battle11", "player_dngn", "demo_op", "demo_chase",
		   "demo_end", "demo_title", "isle_first", "isle_ice", "seatest",
		   "mtest2", "enemytest", "eventtest", "roomtest"}
whitelist = []
# whitelist = ['dngn_wisdom', 'dngn_wisdom2', 'dngn_wisdom3', 'dngn_wisdom4']
wooden_chest_id = 10
white_gold_chest_id = 92
chest_ids = [10, 11, 12, 90, 91, 92] # 105

chest_contents_list = [10, 10, 10, 10, 10, 10, 10, 25, 1, 1, 25, 12, 25, 15, 125, 35, 129, 119, 34, 118, 19, 0, 47, 125, 46, 125, 6, 6, 6, 45, 125, 20, 45, 125, 117, 98, 84, 125, 126, 34, 45, 126, 47, 35, 46, 126, 21, 9, 105, 117, 26, 125, 6, 6, 27, 106, 126, 22, 135, 135, 125, 126, 45, 1, 8, 46, 9, 33, 15, 45, 125, 47, 25, 97, 14, 134, 15, 134, 25, 45, 46, 117, 119, 1, 46, 32, 15, 1, 118, 15, 47, 125, 7, 45, 125, 31, 15, 9, 1, 1, 47, 25, 47, 9, 47, 45, 113, 46, 126, 9, 125, 126, 45, 47, 3, 60, 103, 47, 99, 133, 133, 45, 47, 125, 38, 45, 46, 79, 125, 13, 9, 45, 77, 47, 45, 47, 46, 102, 10, 27, 46, 47, 27, 47, 82, 25, 121, 122, 123, 124, 46, 45, 25, 25, 9, 45, 78, 47, 46, 86, 46, 45, 46, 47, 26, 9, 46, 46]
random.shuffle(chest_contents_list)

object_ids = {
	"0": "Tree",
	"1": "Two Horizontal Grass Patches",
	"2": "Boulder",
	"3": "Blue Pot",
	"4": "Fence Post",
	"5": "Brown Floor Switch",
	"6": "Game Crash (Bad Parameter Maybe?)",
	"7": "Grey and Blue Stone Door",
	"8": "Small Stone Slab",
	"9": "Large Wooden/Stone Key Door",
	"10": "Wooden Treasure Chest",
	"11": "Spawning Chest ???",
	"12": "Entering the area spawns a treasure chest (Conditional Treasure Chest Spawn?)",
	"13": "Game Crash",
	"14": "Blue Pot Again",
	"15": "Game Crash",
	"16": "Game Crash",
	"17": "Red Campfire",
	"18": "Game crash",
	"19": "Game Crash",
	"20": "Game Crash",
	"21": "Stone Triangle Base With Pyramid and Entrance",
	"22": "Game Crash",
	"23": "Game Crash",
	"24": "Game Crash",
	"31": "Sign",
	"47": "Main Island NPC House",
	"90": "Big (White/Gold) Chest (Wind Temple/Bombs), (Courage Temple/Bow)",
	"91": "Big (White/Gold) Chest (Goron Temple/Bombchus/BigKey), (Ice Temple/GrapplingHook/BigKey)",
	"92": "Big (White/Gold) Chest (Flame Temple/Boomerang)",
	"136": "Stone Pyramid With Front Entrance",
	"60": "Collisionless Vertical Grass Tile"
}
chest_item_ids = {
	0: 'Nothing! (\'Nothing is here\')',
	1: 'Key',
	2: 'Green Rupee (1)',
	3: 'Sword',
	4: 'Shield',
	5: 'Key (Textbox: "NO MESSAGE" (No Key Received!))',
	6: 'Force Gem (No Textbox)',
	7: 'Bombs',
	8: 'Bow (No TB (TextBox))',
	9: 'Big Green Rupee (100)',
	10: 'Heart Container',
	11: 'Key (Textbox: "NO MESSAGE" (No Key Received!))',
	12: 'Boomerang',
	13: 'Shovel (No TB)',
	14: 'Bombchus (No TB)',
	15: 'Boss Key',
	16: 'Red Potion (Textbox: "NO MESSAGE")',
	17: 'Key (Textbox: "NO MESSAGE" (No Key Received!))',
	18: 'Key (Textbox: "NO MESSAGE" (No Key Received!))',
	19: 'Treasure Chart (No TB)',
	20: 'Treasure Chart (No TB)',
	21: 'Treasure Chart (No TB)',
	22: 'Treasure Chart (No TB)',
	23: 'Key (Textbox: "NO MESSAGE" (No Key Received!))',
	24: 'Blue Rupee (5)',
	25: 'Red Rupee (20)',
	26: 'Big Red Rupee (200)',
	27: 'Big Gold Rupee (300)',
	28: 'Force Gem (Textbox: "NO MESSAGE" , No Force Gem in hands afterwards)',
	29: 'Red Force Gem (Textbox: "NO MESSAGE" , No Force Gem in hands afterwards)',
	30: 'Blue Force Gem (Textbox: "NO MESSAGE" , No Force Gem in hands afterwards)',
	31: 'Hammer (No TB)',
	32: 'Grappling Hook (No TB)',
	33: 'Square Crystal',
	34: 'Round Crystal',
	35: 'Triangle Crystal',
	36: 'Fishing Rod (No TB)',
	37: 'Cannon',
	38: 'Sun Key',
	39: 'Key (Textbox: "NO MESSAGE")',
	40: 'Quiver Upgrade',
	41: 'Bomb Bag Upgrade',
	42: 'Bombchu Bag Upgrade',
	43: 'Treasure (Textbox = "You got the ship part")',
	44: "King's Key",
	45: 'Power Gem',
	46: 'Wisdom Gem',
	47: 'Courage Gem',
	48: 'Treasure (Pink Coral)',
	49: 'Treasure (White Pearl Loop)',
	50: 'Treasure (Dark Pearl Loop)',
	51: 'Treasure (Zora Scale)',
	52: 'Treasure (Goron Amber)',
	53: 'Treasure (Ruto Crown)',
	54: 'Treasure (Helmaroc Plume)',
	55: 'Treasure (Regal Ring)',
	56: 'Ghost Key',
	57: 'Freebie Card',
	58: 'Compliment Card',
	59: 'Complimentary Card',
	60: 'Regal Necklace (No TB)',
	61: 'Boat Crane',
	62: "Hero's New Clothes",
	63: 'Telescope',
	64: 'guard notebook',
	65: "Jolene's Letter",
	66: 'Prize Postcard',
	67: 'Wood Heart',
	68: 'Sword (No TB)',
	69: 'Key ("You got the Phantom Sword ...")',
	70: 'Key (No TB)',
	71: 'Key (No TB)',
	72: 'Key (No TB)',
	73: 'Key (No TB)',
	74: 'Key (No TB)',
	75: 'Treasure Map (SWQ) [South West Quadrant]',
	76: 'Treasure Map (SWQ)',
	77: 'Treasure Map (SWQ)',
	78: 'Treasure Map (SWQ)',
	79: 'Treasure Map (SWQ)',
	80: 'Treasure Map (SWQ)',
	81: 'Treasure Map (SWQ)',
	82: 'Treasure Map (SWQ)',
	83: 'Treasure Map (NWQ) [North West Quadrant]',
	84: 'Treasure Map (NWQ)',
	85: 'Treasure Map (NWQ)',
	86: 'Treasure Map (NWQ)',
	87: 'Treasure Map (NWQ)',
	88: 'Treasure Map (NWQ)',
	89: 'Treasure Map (NWQ)',
	90: 'Treasure Map (NWQ)',
	91: 'Treasure Map (SEQ) [South East Quadrant]',
	92: 'Treasure Map (SEQ)',
	93: 'Treasure Map (SEQ)',
	94: 'Treasure Map (SEQ)',
	95: 'Treasure Map (SEQ)',
	96: 'Treasure Map (SEQ)',
	97: 'Treasure Map (SEQ)',
	98: 'Treasure Map (SEQ)',
	99: 'Treasure Map (NEQ) [North East Quadrant]',
	100: 'Treasure Map (NEQ)',
	101: 'Treasure Map (NEQ)',
	102: 'Treasure Map (NEQ)',
	103: 'Treasure Map (NEQ)',
	104: 'Treasure Map (NEQ)',
	105: 'Treasure Map (NEQ)',
	106: 'Treasure Map (NEQ)',
	107: 'Nothing ?',
	108: 'Nothing ?',
	109: 'Nothing ?',
	110: 'Nothing ?',
	111: 'Nothing ?',
	112: 'Nothing ?',
	113: 'Swordsman Scroll',
	114: 'Crimsonine',
	115: 'Azurine',
	116: 'Aquanine',
	117: 'Red Potion',
	118: 'Purple Potion',
	119: 'Yellow Potion',
	120: 'Sand of Hours (One Minute)',
	121: 'Golden Chimney',
	122: 'Golden Handrail',
	123: 'Golden Cannon',
	124: 'Golden Hull',
	125: 'Random Treasure', #'Ruto Crown',
	126: 'Ship Part (Random)',
	127: 'Stone Tablet / Slate',
	128: 'Bait (No TB)',
	129: 'Rupoor (10)',
	130: 'Rupoor (50)',
	131: 'Key ("You got some Sand of Hours (30 Seconds)")',
	132: 'Key ("You got some Sand of Hours (10 Seconds)")',
	133: 'Ship Part (Random)',
	134: 'Common Treasure',
	135: 'Ship Part (Random)',
	136: 'Key (No TB)',
	137: 'Key (No TB)',
	138: 'Key (No TB)',
	139: 'Key (No TB)',
	140: 'Key (No TB)',
	141: 'Key (No TB)',
	142: 'Key (No TB)',
	143: 'Key (No TB)',
	144: 'Key (No TB)',
	145: 'Key (No TB)',
	146: 'Key (No TB)',
	147: 'Key (No TB)',
	148: 'Key (No TB)',
	149: 'Key (No TB)',
	150: 'Key (No TB)',
	151: 'Key (No TB)',
	152: 'Key (No TB)',
	153: 'Key (No TB)',
	154: 'Key (No TB)',
	155: 'Key (No TB)',
	156: 'Key (No TB)',
	157: 'Key (No TB)',
	158: 'Key (No TB)',
	159: 'Key (No TB)',
	255: 'Key (No TB)'
}

chest_list = []
# chest_list = [125, 129, 118, 6, 1, 34, 35, 6, 125, 9, 125, 47, 45, 46, 46, 47, 1, 45, 125, 9, 1, 25, 9, 46, 126, 126, 45, 3, 103, 1, 47, 45, 47, 38, 125, 13, 9, 45, 47, 45, 46, 1, 47, 82, 46, 45, 45, 78, 47, 46, 46, 45, 46, 1, 46, 46]
random.shuffle(chest_list)

rom = ndspy.rom.NintendoDSRom.fromFile('ph_dpad.nds')
dpad_patch = True
map_folder = rom.filenames.subfolder('Map').folders

starting_id = 432 if dpad_patch else 433 # 0433
narc_id = starting_id
# print(rom.filenames.subfolder('Map'))
print("{")
for folder in map_folder:
	folder_name = folder[0]
	folder = folder[1]
	if (folder_name not in whitelist and len(whitelist) > 0) or folder_name in banlist:
		starting_id += len(folder.files)
		continue
	print("    " * 1, end="")
	print(f'"{folder_name}": ' + '{')
	for file in folder.files:
		if 'map' not in file:
			starting_id += 1
			continue
		# if '19' not in file:
		# 	starting_id += 1
		# 	continue
		# else:
		# 	starting_id = 596 if dpad_patch else 597
		# print("    " * 2, end="")
		# print(f'"{rom.filenames.filenameOf(starting_id)}": ' + '{')
		narc_file = ndspy.narc.NARC(ndspy.lz10.decompress(rom.files[starting_id]))
		narc_id = starting_id
		zmb_folder = narc_file.filenames.subfolder('zmb')
		if zmb_folder is None:
			starting_id += 1
			continue
		zmb_files = zmb_folder.files
		for zmb_file in zmb_files:
			print("    " * 3, end="")
			print(f'"{zmb_file}": ' + '[')
			f = io.BytesIO(narc_file.getFileByName(f'zmb/{zmb_file}'))
			start_mpob = f.read().find(b'BOPM')
			if start_mpob < 0:
				continue
			f.seek(start_mpob)
			f.read(4)
			length = f.read(4)
			length = int.from_bytes(length, 'little')
			element_count = f.read(2)
			element_count = int.from_bytes(element_count, "little")
			f.read(2)
			for i in range(element_count):
				current_location = hex(f.tell())
				map_object_id = int.from_bytes(f.read(4), 'little')
				enable_print()
				# disable_print()
				if map_object_id not in chest_ids:
					disable_print()
				f.read(4)
				chest_item_id = int.from_bytes(f.read(1), 'little')

				# if map_object_id in chest_ids:
				# 	chest_list.append(chest_item_id)

				print("    " * 4, end="")
				print('{')
				print("    " * 5, end="")
				print(f'"object_id": "{map_object_id}",')
				print("    " * 5, end="")
				print(f'"object_type": "{object_ids.get(str(map_object_id))}",')
				print("    " * 5, end="")
				print(f'"location": "{current_location}",')
				print("    " * 5, end="")
				print('"object_metadata": {')
				print("    " * 6, end="")
				print(f'"chest_item_id": "{chest_item_id}",')
				print("    " * 6, end="")
				print(f'"chest_item_type": "{chest_item_ids.get(chest_item_id)}"')
				# if map_object_id in chest_ids:
				# 	f.seek(-1, 1)
				# 	f.write(bytes([chest_contents_list.pop(0)]))
				f.read(19)
				print("    " * 5, end="")
				print('}')
				print("    " * 4, end="")
				if i == element_count - 1:
					print('}')
				else:
					print('},')
				enable_print()
			f.seek(0)
			narc_file.setFileByName(f'zmb/{zmb_file}', f.read())
			f.close()
			print("    " * 3, end="")
			print("],")
		rom.files[narc_id] = ndspy.lz10.compress(narc_file.save())
		starting_id += 1
		# print("    " * 2, end="")
		# print("},")
	print('    ' * 1, end="")
	print('},')
rom.saveToFile('testinggg.nds')
print('}')

enable_print()
print(chest_list)