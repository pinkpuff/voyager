import sys

# This utility requires the Gamingway library to be installed somewhere
# on your computer. Replace the path below with the path to the folder
# containing the gamingway.py file.
sys.path.append("C:/Path/To/Gamingway/Source")

from gamingway import FF4Rom
import voyager

# This utility uses command line arguments to determine the file to
# patch and the output file to generate. Usage:
#
#   python patch.py <input rom name> <output rom name>
#
# But replace the above <input rom name> with the filename (including
# path) to the already-patched Free Enterprise rom, and replace
# <output rom name> with the filename (including path) to save the
# patched file as.
#
# You can omit either of those arguments, in which case it will use the
# names below. (By default "fe.smc" and "out.smc")

args = sys.argv
if len(args) < 2:
 inputfile = "fe.smc"
else:
 inputfile = args[1]
if len(args) < 3:
 outputfile = "out.smc"
else:
 print(len(args))
 outputfile = args[2]

# You can move the included IPS patch files to a different folder, but
# if you do, make sure to put the new path in the quotes here.
# (Keep the slash symbol at the end.)

patchpath = "ips/"

ff4 = FF4Rom(inputfile)
ff4.text.assign_symbol(0xCB, "+")
ff4.text.assign_symbol(0xCC, "(")
ff4.text.assign_symbol(0xCD, ")")
ff4.read()

voyager.read_item_descriptions(ff4)

# =====================================================================
# These lines contain the main functionality of the patch. You can skip
# any of them by putting a hashtag symbol # in front of the line(s) you
# want to skip.
# =====================================================================

# This puts -Sort- and TrashCan at the top of your inventory instead of
# the bottom as the game begins.
voyager.fix_sort_position(ff4)

# This changes the spell names to something more closely resembling the
# naming convention of the rest of the FF series. The 1s, 2s, and 3s
# are not changed to ra's and ga's etc, but Nuke becomes Flare, White
# becomes Holy, etc.
voyager.rename_spells(ff4)

# This makes some changes to certain spell effects to make them more
# useful and/or balanced (at least in my opinion):
#  * Venom becomes shadow damage + sap (and doesn't apply Poison)
#  * Virus (Bio) becomes shadow element
#  * Drain gets its spell power buffed to 13
#  * Dispel becomes reflectable and able to hit bosses
#  * Sight removes the same statuses as the unicorn horn (full party)
#  * Peep becomes usable on bosses
#  * Stone gets its MP cost bumped up to 45
voyager.customize_spell_effects(ff4)

# This changes the spell learning progressions of various characters:
#  * Cecil learns more white spells
#  * Rosa learns "effect" spells like Berserk and Haste earlier
#  * Porom learns healing spells earlier
#  * Palom learns spells at the same levels as Porom all the way down
#  * Child Rydia learns more white spells
voyager.customize_spellbooks(ff4)

# This changes the item names to something more closely resembling the
# naming convention of the rest of the FF series.
voyager.rename_equipment(ff4)

# This changes some equip permissions:
#  * Dark Knight Cecil can equip the items shared by Cid and Kain
#  * Porom can equip hammers
#  * Cid loses the ability to use bows
voyager.customize_equips(ff4)

# This makes changes to certain pieces of equipment:
#  * Fairy Harp is a new item for Edward (replaces Drain Sword)
#  * Sledge Hammer is a new hammer item (replaces Drain Spear)
#  * Silver Staff no longer casts Dispel
#  * Venom Axe hurts slimes instead of giants
#  * Black Robe gives Wis +10
#  * Wizard Robe gives Wis/Wil +3 instead of Wis +5
#  * Crystal gear set gives Wil +5 instead of Wil +3
#  * Gaia Gear can be used by most characters, not just the wizards
voyager.customize_equipment(ff4)

# This makes changes to certain battle commands:
#  * Pray works 75% of the time and heals 10% of max HP
#  * Recall picks better spells, and only ones he doesn't already know
#  * Salve lets you pick an item (Life potion is slightly buggy)
#  * Rage causes Cid to berserk himself (replaces Yang's Bear)
voyager.customize_commands(ff4, patchpath)

# This changes some characters' levelups:
#  * Yang continues to get HP gains all the way to the end
#  * Tellah gains MP (slow at first, then ramps up) and better stat-ups
#  * Dark Knight Cecil gets better HP gains
voyager.customize_levelups(ff4)

# This changes various properties of some of the monsters:
#  * Pale Dim is weak to shadow element and resists holy
#  * Mist Dragon is a dragon type and weak to shadow
#  * Bahamut is a dragon type
#  * A bunch of monsters are now robot/construct type
#     - Including CPU, EvilWall, TrapDoor, Balnab, dolls, bombs, golems
#  * A bunch of monsters that seem like they should float now do
voyager.customize_monsters(ff4)

# Allows Exit to work on Mount Ordeals and the Sealed Cave, adds a tile
# of grass next to Kaipo, and prevents the black chocobo from going
# home when you remount it; you just get back on it and can fly again.
voyager.customize_maps(ff4, patchpath)

# Turns all the J-Items into various normal items like potions and
# tents. Why not just turn off the J-Items flag? Because then I don't
# get enough consumables in chests for my liking. Only works/matters
# when the J-Items flag is set.
voyager.convert_jitems(ff4)

voyager.write_item_descriptions(ff4)

ff4.write()
ff4.save(outputfile)
