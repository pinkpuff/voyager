import sys
sys.path.append("E:/Projects/Hacking/Gamingway/Source")
#sys.path.append("/home/pinkpuff/Projects/Gamingway/Source/")
from gamingway import FF4Rom
import voyager

#patchpath = "/home/pinkpuff/Projects/Voyager/Resources/"
patchpath = "E:/Projects/Hacking/Voyager/Resources/"

args = sys.argv
if len(args) < 2:
 inputfile = "../Resources/fe.smc"
else:
 inputfile = args[1]
if len(args) < 3:
 outputfile = "../game.smc"
else:
 print(len(args))
 outputfile = args[2]

ff4 = FF4Rom(inputfile)
ff4.text.assign_symbol(0xCB, "+")
ff4.text.assign_symbol(0xCC, "(")
ff4.text.assign_symbol(0xCD, ")")
ff4.read()

voyager.read_item_descriptions(ff4)

voyager.fix_sort_position(ff4)
voyager.rename_spells(ff4)
voyager.customize_spell_effects(ff4)
voyager.customize_spellbooks(ff4)
voyager.rename_equipment(ff4)
voyager.customize_equips(ff4)
voyager.customize_equipment(ff4)
voyager.customize_commands(ff4, patchpath)
voyager.consistent_starting_levels(ff4)
voyager.customize_levelups(ff4)
voyager.customize_monsters(ff4)
voyager.customize_maps(ff4, patchpath)
changed_treasures = voyager.convert_jitems(ff4)
#voyager.procgen(ff4)

#for job in ff4.jobs:
# print(job.display(ff4))

voyager.write_item_descriptions(ff4)

ff4.write("magic")
ff4.write("gear")
ff4.write("party")
ff4.write("combat")
ff4.write("tilemaps")
ff4.write("overworld")
ff4.write("maps", False)

# Only write the triggers we changed.
# Since we're not changing the number of triggers, 
#  the pointers can be left alone.
trigger_address = ff4.rom.TRIGGER_DATA_START
for map in ff4.maps:
 for trigger in map.triggers:
  if trigger in changed_treasures or map == ff4.KAIPO_TOWN:
   trigger.write(ff4.rom, trigger_address)
  trigger_address += 5

ff4.save(outputfile)
