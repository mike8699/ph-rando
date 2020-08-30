import sys, getopt, json
from ndspy import lz10, narc, rom


def generate_rom(randomized_json, rom_path, output_path):
   game_rom = rom.NintendoDSRom.fromFile(rom_path)

   for location in randomized_json:
      for zmb in randomized_json[location]:
         map_number = zmb.split('.z')[0][len(zmb.split('.z')[0])-2:]
         narc_path = f"Map/{location}/map{map_number}.bin"
         narc_file = narc.NARC(lz10.decompress(game_rom.getFileByName(narc_path)))
         zmb_file = (narc_file.getFileByName(f'zmb/{zmb}'))
         for chest in randomized_json[location][zmb]:
            offset = int(chest['location'], 0) + 8
            zmb_file = zmb_file[:offset] + bytes([int(chest['object_metadata']['chest_item_id'])]) + zmb_file[offset+1:]
         narc_file.setFileByName(f'zmb/{zmb}', zmb_file)
         game_rom.setFileByName(narc_path, lz10.compress(narc_file.save()))
   game_rom.saveToFile(output_path)


def main(argv):
   randomized_json = None
   rom_location = None
   rom_output_location = None
   try:
      opts, args = getopt.getopt(argv,"do:r:",["data", "output=", "rom="])
   except getopt.GetoptError:
      print('rom_functions.py --data <stringified json object> --output <output_folder>')
      sys.exit(2)
   for opt, arg in opts:   
      if opt in ('-o', '--output'):
         rom_output_location = arg
      elif opt in ('-r', '--rom'):
         rom_location = arg

   randomized_json = json.loads(input())
   if randomized_json is None or rom_output_location is None or rom_location is None:
      raise "error, missing required parameter"

   generate_rom(randomized_json, rom_location, rom_output_location)
   

if __name__ == "__main__":
   main(sys.argv[1:])