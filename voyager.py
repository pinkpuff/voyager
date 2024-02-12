def read_item_descriptions(ff4):

 # The item descriptions in Free Enterprise are located at 0x120000
 # (0x120200 with header) and are encoded as four "lines" of text.
 # Each line starts with 00 FA and ends with FB 00 00.
 # The first line has the item name left-aligned and some other 
 # information like property symbols (ranged, magnetic, etc), then has
 # its main stats (attack, defense, etc) right aligned.
 # The remaining three lines describe the item's other properties like
 # elements, racial properties, etc.
 # The character faces representing the equipabilities seem to be
 # auto-generated so that doesn't need updating in the description.
 if len(ff4.rom.data) < 0x120200:
  print("ERROR: Not a Free Enterprise rom.")
 else:
  descriptions = []
  for index, item in enumerate(ff4.items):
   lines = ["", "", "", ""]
   for y in range(4):
    line = ""
    for x in range(2, 29):
     line += chr(ff4.rom.data[0x120200 + index * 0x80 + y * 0x20 + x])
    lines[y] = ff4.text.asciitext(line)
   item.description = lines

def write_item_descriptions(ff4):
 for index, item in enumerate(ff4.items):
  if len("".join(item.description).strip()) > 0:
   for y in range(4):
    address = 0x120200 + index * 0x80 + y * 0x20
    line = ff4.text.ff4text(item.description[y])
    if len(line) > 27:
     line = line[0:27]
    if len(line) < 27:
     line = line.ljust(27, ff4.text.ff4text(" "))
    bytes = ff4.text.to_bytes(line)
    bytes = [0x00, 0xFA] + bytes + [0xFB, 0x00, 0x00]
    ff4.rom.inject(address, bytes)

def display_description(item):
 return "\n".join(item.description)

def rename_spells(ff4):

 # In order to rename the spells properly, we need to know both the old
 # name and the new name. Thus, it seems easier and more maintainable
 # to just make a dictionary and have the rest of the code process it.
 renames = {
  ff4.HOLD_SPELL:  "[WHT]Stun",
  ff4.ARMOR_SPELL: "[WHT]Prtct",
  ff4.SHELL_SPELL: "[WHT]Shell",
  ff4.FAST_SPELL:  "[WHT]Haste",
  ff4.WALL_SPELL:  "[WHT]Rflct",
  ff4.WHITE_SPELL: "[WHT]Holy",
  ff4.PEEP_SPELL:  "[WHT]Scan",
  ff4.CURE1_SPELL: "[WHT]Cure",
  ff4.HEAL_SPELL:  "[WHT]Esuna",
  ff4.LIFE1_SPELL: "[WHT]Raise",
  ff4.LIFE2_SPELL: "[WHT]Arise",
  ff4.SIZE_SPELL:  "[WHT]Mini",
  ff4.TOAD_SPELL:  "[BLK]Frog",
  ff4.PIGGY_SPELL: "[BLK]Pig",
  ff4.VENOM_SPELL: "[BLK]Poisn",
  ff4.FIRE1_SPELL: "[BLK]Fire",
  ff4.ICE1_SPELL:  "[BLK]Ice",
  ff4.ICE2_SPELL:  "[BLK]Ice2",
  ff4.ICE3_SPELL:  "[BLK]Ice3",
  ff4.LIT1_SPELL:  "[BLK]Bolt",
  ff4.LIT2_SPELL:  "[BLK]Bolt2",
  ff4.LIT3_SPELL:  "[BLK]Bolt3",
  ff4.VIRUS_SPELL: "[BLK]Bio",
  ff4.WEAK_SPELL:  "[BLK]Tnado",
  ff4.STONE_SPELL: "[BLK]Break",
  ff4.FATAL_SPELL: "[BLK]Death",
  ff4.PSYCH_SPELL: "[BLK]Osmos",
  ff4.NUKE_SPELL:  "[BLK]Flare",
  ff4.CHOCB_SPELL: "[SUM]Choco",
  ff4.INDRA_SPELL: "[SUM]Ramuh",
  ff4.JINN_SPELL:  "[SUM]Ifrit"
 }
 
 # Rename the spells and update the descriptions accordingly.
 for spell, newname in renames.items():
  
  # Check the item descriptions first, because in order to do the
  # replacement, we need to know both the old name and the new name;
  # replacing the spell name first would cause us to lose the old name.
  for item in ff4.items:
   for index in range(4):
    item.description[index] = item.description[index].replace(spell.name, newname)
  
  # Once we're done updating the descriptions, we can replace the name.
  spell.name = newname

# Makes Poisn/Venom like a smaller version of Bio/Virus.
def customize_venom_spell(ff4):
 ff4.VENOM_SPELL.power = 4
 ff4.VENOM_SPELL.hit = 100
 ff4.VENOM_SPELL.mp = 4
 ff4.VENOM_SPELL.delay = 0
 ff4.VENOM_SPELL.hitsboss = True
 ff4.VENOM_SPELL.effect = ff4.config.spell_effects.index("Damage, Sap")
 ff4.VENOM_SPELL.attributes = 0

def venom_virus_shadow_element(ff4):
 ff4.VIRUS_SPELL.attributes = ff4.SHADOWSWORD.attributes
 ff4.VENOM_SPELL.attributes = ff4.SHADOWSWORD.attributes

 # The other changes to venom done by customize_venom_spell assume it's
 # non-elemental; by making it Shadow element, it should probably be
 # slightly stronger because so many things resist/absorb Shadow.
 ff4.VENOM_SPELL.power += 1

# The vanilla drain spell is kinda weak to the point of near
# unusability. This buffs its power to make it an interesting
# alternative attack spell to Bio/Virus. While this does make certain
# enemies slightly more dangerous, I feel like it's a worthwhile
# tradeoff.
def customize_drain_spell(ff4):
 ff4.DRAIN_SPELL.power = 13
 
# The vanilla Dispel is reflectable, which makes it kind of hard for
# it to remove Reflect the way it should. This makes it so it has some
# pretty interesting uses, especially as it can now hit bosses.
def customize_dispel_spell(ff4):
 ff4.DISPL_SPELL.reflectable = False
 ff4.DISPL_SPELL.hitsboss = True

# Sight is useless when you know the map by heart, but maybe it can be
# be usable as a "Basuna" type spell that heals temporary statuses.
def customize_sight_spell(ff4):
 ff4.SIGHT_SPELL.power = ff4.HEAL_SPELL.power
 ff4.SIGHT_SPELL.hit = ff4.HEAL_SPELL.hit
 ff4.SIGHT_SPELL.effect = ff4.HEAL_SPELL.effect
 ff4.SIGHT_SPELL.attributes = ff4.UNIHORN.utility.attributes
 ff4.SIGHT_SPELL.target = ff4.config.target_types.index("All allies")
 ff4.SIGHT_SPELL.palette = ff4.HEAL_SPELL.palette
 ff4.SIGHT_SPELL.sprites = ff4.HEAL_SPELL.sprites
 ff4.SIGHT_SPELL.visual1 = ff4.HEAL_SPELL.visual1
 ff4.SIGHT_SPELL.visual2 = ff4.HEAL_SPELL.visual2
 ff4.SIGHT_SPELL.sound = ff4.HEAL_SPELL.sound

# I don't see any reason why Peep/Scan shouldn't work on bosses.
# Not sure if that makes it useful per se, but it can't make it worse.
def customize_peep_spell(ff4):
 ff4.PEEP_SPELL.hitsboss = True

# In vanilla, "Stone" only costs 15 MP, which despite being pretty much
# better than the Fatal/Death spell in every way (faster, can work on
# undeads, can multi-target, etc) somehow costs less MP! So let's
# make it cost 45 instead of 15. That seems a bit more fair, given the
# costs of other insta-kill spells.
def customize_stone_spell(ff4):
 ff4.STONE_SPELL.mp = 45

# This is basically a shortcut to apply all the spell customizations in
# a single function call.
def customize_spell_effects(ff4):
 customize_venom_spell(ff4)
 venom_virus_shadow_element(ff4)
 customize_drain_spell(ff4)
 customize_dispel_spell(ff4)
 customize_sight_spell(ff4)
 customize_peep_spell(ff4)
 customize_stone_spell(ff4)

def customize_spellbooks(ff4):

 # Paladin Cecil
 ff4.CECIL_WHITE.clear()
 ff4.CECIL_WHITE.teach_spell(0, ff4.CURE1_SPELL)
 ff4.CECIL_WHITE.teach_spell(5, ff4.SIGHT_SPELL)
 ff4.CECIL_WHITE.teach_spell(10, ff4.ARMOR_SPELL)
 ff4.CECIL_WHITE.teach_spell(15, ff4.EXIT_SPELL)
 ff4.CECIL_WHITE.teach_spell(20, ff4.CURE2_SPELL)
 ff4.CECIL_WHITE.teach_spell(25, ff4.HEAL_SPELL)
 ff4.CECIL_WHITE.teach_spell(35, ff4.LIFE1_SPELL)
 ff4.CECIL_WHITE.teach_spell(45, ff4.FLOAT_SPELL)
 ff4.CECIL_WHITE.teach_spell(55, ff4.CURE3_SPELL)

 # Rosa
 ff4.ROSA_WHITE.clear()
 ff4.ROSA_WHITE.teach_spell(0, ff4.CURE1_SPELL)
 ff4.ROSA_WHITE.teach_spell(0, ff4.SLOW_SPELL)
 ff4.ROSA_WHITE.teach_spell(0, ff4.HOLD_SPELL)
 ff4.ROSA_WHITE.teach_spell(0, ff4.SIGHT_SPELL)
 ff4.ROSA_WHITE.teach_spell(0, ff4.PEEP_SPELL)
 ff4.ROSA_WHITE.teach_spell(11, ff4.ARMOR_SPELL)
 ff4.ROSA_WHITE.teach_spell(12, ff4.MUTE_SPELL)
 ff4.ROSA_WHITE.teach_spell(13, ff4.BERSK_SPELL)
 ff4.ROSA_WHITE.teach_spell(15, ff4.LIFE1_SPELL)
 ff4.ROSA_WHITE.teach_spell(18, ff4.CURE2_SPELL)
 ff4.ROSA_WHITE.teach_spell(20, ff4.BLINK_SPELL)
 ff4.ROSA_WHITE.teach_spell(23, ff4.SHELL_SPELL)
 ff4.ROSA_WHITE.teach_spell(24, ff4.FAST_SPELL)
 ff4.ROSA_WHITE.teach_spell(28, ff4.CHARM_SPELL)
 ff4.ROSA_WHITE.teach_spell(29, ff4.FLOAT_SPELL)
 ff4.ROSA_WHITE.teach_spell(30, ff4.HEAL_SPELL)
 ff4.ROSA_WHITE.teach_spell(31, ff4.WALL_SPELL)
 ff4.ROSA_WHITE.teach_spell(33, ff4.SIZE_SPELL)
 ff4.ROSA_WHITE.teach_spell(35, ff4.DISPL_SPELL)
 ff4.ROSA_WHITE.teach_spell(36, ff4.CURE3_SPELL)
 ff4.ROSA_WHITE.teach_spell(38, ff4.WHITE_SPELL)
 ff4.ROSA_WHITE.teach_spell(45, ff4.LIFE2_SPELL)
 ff4.ROSA_WHITE.teach_spell(55, ff4.CURE4_SPELL)

 # Porom
 ff4.POROM_WHITE.clear()
 ff4.POROM_WHITE.teach_spell(0, ff4.CURE1_SPELL)
 ff4.POROM_WHITE.teach_spell(0, ff4.SLOW_SPELL)
 ff4.POROM_WHITE.teach_spell(0, ff4.HOLD_SPELL)
 ff4.POROM_WHITE.teach_spell(0, ff4.SIGHT_SPELL)
 ff4.POROM_WHITE.teach_spell(0, ff4.PEEP_SPELL)
 ff4.POROM_WHITE.teach_spell(11, ff4.CURE2_SPELL)
 ff4.POROM_WHITE.teach_spell(12, ff4.LIFE1_SPELL)
 ff4.POROM_WHITE.teach_spell(13, ff4.ARMOR_SPELL)
 ff4.POROM_WHITE.teach_spell(14, ff4.SHELL_SPELL)
 ff4.POROM_WHITE.teach_spell(15, ff4.HEAL_SPELL)
 ff4.POROM_WHITE.teach_spell(19, ff4.EXIT_SPELL)
 ff4.POROM_WHITE.teach_spell(22, ff4.SIZE_SPELL)
 ff4.POROM_WHITE.teach_spell(23, ff4.MUTE_SPELL)
 ff4.POROM_WHITE.teach_spell(26, ff4.CHARM_SPELL)
 ff4.POROM_WHITE.teach_spell(29, ff4.FAST_SPELL)
 ff4.POROM_WHITE.teach_spell(31, ff4.CURE3_SPELL)
 ff4.POROM_WHITE.teach_spell(32, ff4.BLINK_SPELL)
 ff4.POROM_WHITE.teach_spell(33, ff4.BERSK_SPELL)
 ff4.POROM_WHITE.teach_spell(36, ff4.FLOAT_SPELL)
 ff4.POROM_WHITE.teach_spell(40, ff4.CURE4_SPELL)
 ff4.POROM_WHITE.teach_spell(46, ff4.LIFE2_SPELL)
 ff4.POROM_WHITE.teach_spell(48, ff4.WALL_SPELL)
 ff4.POROM_WHITE.teach_spell(50, ff4.DISPL_SPELL)
 ff4.POROM_WHITE.teach_spell(52, ff4.WHITE_SPELL)

 # Palom
 ff4.PALOM_BLACK.clear()
 ff4.PALOM_BLACK.teach_spell(0, ff4.ICE1_SPELL)
 ff4.PALOM_BLACK.teach_spell(0, ff4.FIRE1_SPELL)
 ff4.PALOM_BLACK.teach_spell(0, ff4.LIT1_SPELL)
 ff4.PALOM_BLACK.teach_spell(0, ff4.VENOM_SPELL)
 ff4.PALOM_BLACK.teach_spell(0, ff4.SLEEP_SPELL)
 ff4.PALOM_BLACK.teach_spell(11, ff4.ICE2_SPELL)
 ff4.PALOM_BLACK.teach_spell(12, ff4.FIRE2_SPELL)
 ff4.PALOM_BLACK.teach_spell(13, ff4.LIT2_SPELL)
 ff4.PALOM_BLACK.teach_spell(14, ff4.STOP_SPELL)
 ff4.PALOM_BLACK.teach_spell(15, ff4.PIGGY_SPELL)
 ff4.PALOM_BLACK.teach_spell(19, ff4.VIRUS_SPELL)
 ff4.PALOM_BLACK.teach_spell(22, ff4.TOAD_SPELL)
 ff4.PALOM_BLACK.teach_spell(23, ff4.DRAIN_SPELL)
 ff4.PALOM_BLACK.teach_spell(26, ff4.QUAKE_SPELL)
 ff4.PALOM_BLACK.teach_spell(29, ff4.WARP_SPELL)
 ff4.PALOM_BLACK.teach_spell(31, ff4.ICE3_SPELL)
 ff4.PALOM_BLACK.teach_spell(32, ff4.FIRE3_SPELL)
 ff4.PALOM_BLACK.teach_spell(33, ff4.LIT3_SPELL)
 ff4.PALOM_BLACK.teach_spell(36, ff4.PSYCH_SPELL)
 ff4.PALOM_BLACK.teach_spell(40, ff4.WEAK_SPELL)
 ff4.PALOM_BLACK.teach_spell(46, ff4.FATAL_SPELL)
 ff4.PALOM_BLACK.teach_spell(48, ff4.STONE_SPELL)
 ff4.PALOM_BLACK.teach_spell(50, ff4.METEO_SPELL)
 ff4.PALOM_BLACK.teach_spell(52, ff4.NUKE_SPELL)

 # Rydia
 ff4.RYDIA_WHITE.teach_spell(18, ff4.LIFE1_SPELL)
 ff4.RYDIA_WHITE.teach_spell(24, ff4.CURE2_SPELL)
 ff4.RYDIA_WHITE.teach_spell(30, ff4.HEAL_SPELL)
 ff4.RYDIA_WHITE.teach_spell(36, ff4.BLINK_SPELL)
 ff4.RYDIA_WHITE.teach_spell(42, ff4.CURE3_SPELL)
 ff4.RYDIA_WHITE.teach_spell(48, ff4.WALL_SPELL)

# This is just a straight up ASM hack that puts -Sort- and Trashcan at
# the top of the inventory list (WHERE THEY BELONG! :P).
def fix_sort_position(ff4):

 # In the original rom, there is a code subroutine that puts the Sort
 # and TrashCan items into positions 47 and 48 in your inventory.
 # This changes the positions it puts those items (and their
 # quantities) in to 00 and 01.
 ff4.rom.data[0x4F2] = 0x40 # Address for item 00 ID (low byte)
 ff4.rom.data[0x4F3] = 0x14 # Address for item 00 ID (high byte)
 ff4.rom.data[0x4F7] = 0x42 # Address for item 01 ID (low byte)
 ff4.rom.data[0x4F8] = 0x14 # Address for item 01 ID (high byte)
 ff4.rom.data[0x4FC] = 0x41 # Address for item 00 Quantity (low byte)
 ff4.rom.data[0x4FD] = 0x14 # Address for item 00 Quantity (high byte)
 ff4.rom.data[0x4FF] = 0x43 # Address for item 01 Quantity (low byte)
 ff4.rom.data[0x500] = 0x14 # Address for item 01 Quantity (high byte)
 
# This renames the items to suit my personal preferences. Most (but
# certainly not all) of the renames are in the spirit of consistency
# with other FF games.
def rename_equipment(ff4):

 # Like the spell renames, the item renames are encoded as a dictionary
 # first and then batch processed in order to make it easier to update.
 renames = {
  ff4.THUNDERCLAW:   "[CLW]BoltClaw",
  ff4.CHARMCLAW:     "[CLW]Fairy",
  ff4.POISONCLAW:    "[CLW]Hellclaw",
  ff4.ICEROD:        "[ROD]Ice",
  ff4.THUNDERROD:    "[ROD]Thunder",
  ff4.FLAMEROD:      "[ROD]Flame",
  ff4.CHANGEROD:     "[ROD]Polymrph",
  ff4.CHARMROD:      "[ROD]Fairy",
  ff4.CURESTAFF:     "[STF]Healing",
  ff4.SILVERSTAFF:   "[STF]Mythril",
  ff4.LUNARSTAFF:    "[STF]Aura",
  ff4.LIFESTAFF:     "[STF]Sage",
  ff4.BLACKSWORD:    "[FEL]Death",
  ff4.LIGHTSWORD:    "[KNS]Luminous",
  ff4.DEFENSE:       "[SWD]Defender",
  ff4.DRAINSWORD:    "[SWD]Blood",
  ff4.SLUMBERSWORD:  "[SWD]Sleep",
  ff4.MEDUSASWORD:   "[SWD]Break",
  ff4.DRAGOONSPEAR:  "[SPR]Wyvern",
  ff4.WHITESPEAR:    "[SPR]Holy",
  ff4.DRAINSPEAR:    "[SPR]Blood",
  ff4.SHORTBLADE:    "[KAT]Kunai",
  ff4.MIDDLEBLADE:   "[KAT]Ashura",
  ff4.LONGBLADE:     "[KAT]Kotetsu",
  ff4.NINJABLADE:    "[KAT]Kikuichi",
  ff4.MUTEKNIFE:     "[DAG]Mage",
  ff4.WHIP:          "[WHP]Leather",
  ff4.HANDAXE:       "[AXE]Hand",
  ff4.DWARFAXE:      "[AXE]Tomahawk",
  ff4.OGREAXE:       "[AXE]Ogrekilr",
  ff4.SILVERKNIFE:   "[DAG]Mythril",
  ff4.SILVERSWORD:   "[SWD]Mythril",
  ff4.NINJASTAR:     "[SHU]Fuma",
  ff4.CHARMHARP:     "[HRP]Lamia",
  ff4.POISONAXE:     "[AXE]Venom",
  ff4.RUNEAXE:       "[AXE]Rune",
  ff4.SILVERHAMMER:  "[HMR]Mythril",
  ff4.EARTHHAMMER:   "[HMR]Gaia",
  ff4.WOODENHAMMER:  "[HMR]Wooden",
  ff4.SHORTBOW:      "[BOW]Short",
  ff4.CROSSBOW:      "[BOW]Long",
  ff4.GREATBOW:      "[BOW]Great",
  ff4.ARCHERBOW:     "[BOW]Killer",
  ff4.ELVENBOW:      "[BOW]Rune",
  ff4.SAMURAIBOW:    "[BOW]Yoichi",
  ff4.WHITEARROW:    "[ARO]Holy",
  ff4.LITARROW:      "[ARO]Bolt",
  ff4.DARKNESSARROW: "[ARO]Blind",
  ff4.MUTEARROW:     "[ARO]Silence",
  ff4.CHARMARROW:    "[ARO]Angel",
  ff4.SAMURAIARROW:  "[ARO]Yoichi",
  ff4.SILVERSHIELD:  "[SHL]Mythril",
  ff4.SAMURAISHIELD: "[SHL]Genji",
  ff4.DRAGOONSHIELD: "[SHL]Dragon",
  ff4.SILVERHELM:    "[HAT]Mythril",
  ff4.SAMURAIHELM:   "[HAT]Genji",
  ff4.DRAGOONHELM:   "[HAT]Dragon",
  ff4.GAEAHAT:       "[HAT]Triangle",
  ff4.WIZARDHAT:     "[HAT]Mitre",
  ff4.TIARA:         "[HAT]Hairpin",
  ff4.NINJAHAT:      "[HAT]Blk.Cowl",
  ff4.SILVERMAIL:    "[ARM]Mythril",
  ff4.SAMURAIMAIL:   "[ARM]Genji",
  ff4.DRAGOONMAIL:   "[ARM]Dragon",
  ff4.GAEAROBE:      "[ROB]GaiaGear",
  ff4.SORCERERROBE:  "[ROB]Lords",
  ff4.HEROINEROBE:   "[ROB]Minerva",
  ff4.BARDROBE:      "[ROB]Poet",
  ff4.KARATEROBE:    "[ROB]KenpoGi",
  ff4.BLBELT:        "[ROB]JudoGi",
  ff4.SILVERGLOVE:   "[GLV]Mythril",
  ff4.SAMURAIGLOVE:  "[GLV]Genji",
  ff4.DRAGOONGLOVE:  "[GLV]Dragon",
  ff4.IRONRING:      "[RNG]Iron",
  ff4.RUBYRING:      "[RNG]Ruby",
  ff4.LILBOMB:       "#BombShrd",
  ff4.BIGBOMB:       "#BombArm",
  ff4.NOTUS:         "#Arctic",
  ff4.BOREAS:        "#Antartic",
  ff4.BLIZZARD:      "#Ice-Ball",
  ff4.KAMIKAZE:      "#Exploder",
  ff4.CURE1:         "[BTL]Potion",
  ff4.CURE2:         "[BTL]HiPotion",
  ff4.CURE3:         "[BTL]X-Potion",
  ff4.ETHER1:        "[BTL]Ether",
  ff4.ETHER2:        "[BTL]DryEther",
  ff4.LIFE:          "[BTL]Phoenix",
  ff4.SOFT:          "[BTL]Soft",     # Free Enterprise doesn't use the
  ff4.MAIDKISS:      "[BTL]MaidKiss", # bottle symbols for these.
  ff4.MALLET:        "[BTL]Mallet",   #
  ff4.DIETFOOD:      "[BTL]DietFood", #
  ff4.ECHONOTE:      "[BTL]EchoHerb",
  ff4.EYEDROPS:      "[BTL]Eyedrop",
  ff4.ANTIDOTE:      "[BTL]Pure",
  ff4.CROSS:         "[BTL]Cross",
  ff4.HEAL:          "[BTL]Remedy",
  ff4.GOLDAPPLE:     "#HP-Apple",
  ff4.SILVERAPPLE:   "#HP-Seed",
  ff4.SOMADROP:      "#MP-Seed",
  ff4.EAGLEEYE:      "#DwarfBun"
 }
 
 # Rename the items.
 for item, newname in renames.items():

  # Only the first line of the descrpition should reference the item
  # name.
  # We need to split it to keep the equipment stats right-aligned.
  tokens = item.description[0].split(" ")

  # We convert it to FF4Text in order to keep the correct length.
  rightpart = ff4.text.ff4text(tokens[len(tokens) - 1].strip())

  # If it's an armor, the right-aligned part is the last two tokens
  # instead of just the last one.
  index = ff4.items.index(item)
  armors = ff4.rom.ARMORS_START_INDEX
  if index in range(armors, armors + ff4.rom.TOTAL_ARMORS):
   addendum = ff4.text.ff4text(tokens[len(tokens) - 2].strip() + " ")
   rightpart = addendum + rightpart

  # Replace the name.
  leftpart = tokens[0].replace(item.name, newname)

  # For similar reasons as above, we convert it to FF4Text and pad it
  # to the full line length in case it came out shorter.
  leftpart = ff4.text.ff4text(leftpart).ljust(27, ff4.text.ff4text(" "))

  # Then we crop it to make room for the "right part".
  leftpart = leftpart[0:27 - len(rightpart) - 1]

  # Put the two back together.
  item.description[0] = leftpart + ff4.text.ff4text(" ") + rightpart

  # And finally, covert back to ASCII.
  item.description[0] = ff4.text.asciitext(item.description[0])

  # Now that we're done fixing the description, it's safe to rename the
  # actual item itself.
  item.name = newname

# Give DK Cecil some equipment.
def dk_equips_tank_gear(ff4):

 # He should be able to equip the things that in vanilla were
 # equippable by everyone except DK.
 ff4.equips[0x01].flags[0] = True

 # He should also be able to use the equipment that all the other
 # "tank" type characters can use.
 ff4.equips[0x03].flags[0] = True
 ff4.equips[0x04].flags[0] = True
 ff4.equips[0x05].flags[0] = True
 ff4.equips[0x06].flags[0] = True
 ff4.equips[0x07].flags[0] = True

# Allow Porom to use hammers.
def porom_uses_hammers(ff4):

 # Unlike the Dark Knight equips function, we won't modify the equip
 # table itself, but rather we will create a new one out of one of the
 # unused equip tables and assign all the hammers to that index.
 # Note that since this change is made AFTER the Free Enterprise
 # randomization, a Porom Hero seed will still never generate a hammer
 # as the forge item. However, if a Cid Hero seed generates a hammer,
 # Porom will still be able to use it.
 unused = 0x0D
 for index in range(16):
  ff4.equips[unused].flags[index] = False
 ff4.equips[unused].flags[8] = True
 ff4.equips[unused].flags[10] = True

 # Now that the equip table has been created, we assign the hammers to
 # use that table.
 ff4.WOODENHAMMER.equips = unused
 ff4.SILVERHAMMER.equips = unused
 ff4.EARTHHAMMER.equips = unused

 # I'm pretty sure the forge item replaces the Dummy Crystal Sword so
 # we'll check if it's a hammer. I think the best way to do that is to
 # check its item symbol.
 if ff4.DUMMYSWORD.name[0] == "[":
  if ff4.DUMMYSWORD.name[0:5] == "[WRN]":
   
   # If the item renaming function was used, it will replace the 
   # wrench symbol on the hammers with the hammer symbol. This makes
   # sure that if the forge item is a hammer, it will start with the
   # same symbol as the other hammers.
   if ff4.WOODENHAMMER.name[0] == "[":
    prefix = ff4.WOODENHAMMER.name[0:5]
    ff4.DUMMYSWORD.name = ff4.DUMMYSWORD.name.replace("[WRN]", prefix)
   
   # And since we've determined it's a hammer, update its equip index.
   ff4.DUMMYSWORD.equips = unused

# There's no reason Cid should be able to use bows IMO.
# Pure speculation, but I suspect it was only only that way in vanilla
# in order to give him more options in the magnetic cave besides the
# wooden hammer.
def cid_no_bows(ff4):
 ff4.equips[ff4.SHORTBOW.equips].flags[10] = False

def customize_equips(ff4):
 dk_equips_tank_gear(ff4)
 porom_uses_hammers(ff4)
 cid_no_bows(ff4)

# Creates a new harp for Edward.
def create_fairy_harp(ff4):

 # We need to replace something and I'm not a fan of the drain gear.
 ff4.FAIRYHARP = ff4.DRAINSWORD

 # Update its properties to match that of a harp.
 ff4.FAIRYHARP.equips = ff4.DREAMER.equips
 ff4.FAIRYHARP.ranged = True
 ff4.FAIRYHARP.magnetic = False
 ff4.FAIRYHARP.throwable = False
 ff4.FAIRYHARP.sprite = ff4.DREAMER.sprite
 ff4.FAIRYHARP.swing = ff4.DREAMER.swing
 ff4.FAIRYHARP.slash = ff4.DREAMER.slash
 ff4.FAIRYHARP.palette = ff4.DRAGONWHIP.palette

 # Let's make it add blind.
 ff4.FAIRYHARP.attributes = ff4.DARKNESSARROW.attributes

 # And it should hurt giants, like the Fairy/Charm Claw.
 for index in range(8):
  ff4.FAIRYHARP.races.flags[index] = False
 ff4.FAIRYHARP.races.flags[ff4.config.race_names.index("Giant")] = True

 # Give it some combat stats.
 ff4.FAIRYHARP.attack = 80
 ff4.FAIRYHARP.hit = 80

 # And stat buffs.
 ff4.FAIRYHARP.statbuff.stats = [True, True, True, False, False]
 ff4.FAIRYHARP.statbuff.amount = 1

 # It of course needs a new name and a new description to match.
 ff4.FAIRYHARP.name = "[HRP]Fairy"
 ff4.FAIRYHARP.description[0] = "[HRP]Fairy              [KAT]80/80%"
 ff4.FAIRYHARP.description[1] = "STR/AGI/VIT+5. Two-handed. "
 ff4.FAIRYHARP.description[2] = "Inflicts Blind. Strong     "
 ff4.FAIRYHARP.description[3] = "against giants.            "

 # Finally, it should be two-handed, which appears to still be handled
 # by item index. This means we have to swap it with a two-handed item 
 # of an appropriate tier which we don't mind being one-handed.
 # Poison/Venom axe seems like a decent candidate.
 # They have to be swapped by index like this because using the 
 # constants doesn't seem to work.
 ff4.items[0x47], ff4.items[0x1F] = ff4.items[0x1F], ff4.items[0x47]
 
 # But it's a lower tier now so we need to make sure it's weaker than
 # the Ogre axe, so we can just swap their attack powers I guess.
 ff4.POISONAXE.attack, ff4.OGREAXE.attack = ff4.OGREAXE.attack, ff4.POISONAXE.attack

 # This means we have to fix the axe's description too.
 ff4.OGREAXE.description[0] = ff4.OGREAXE.description[0].replace(str(ff4.POISONAXE.attack), str(ff4.OGREAXE.attack))
 ff4.POISONAXE.description[0] = ff4.POISONAXE.description[0].replace(str(ff4.OGREAXE.attack), str(ff4.POISONAXE.attack))
 line = ff4.POISONAXE.description[1].replace("Two-handed.", "")
 line = line.lstrip().ljust(27)
 ff4.POISONAXE.description[1] = line

def create_sledge_hammer():
 ff4.SLEDGEHAMMER = ff4.DRAINSPEAR
 ff4.SLEDGEHAMMER.equips = ff4.EARTHHAMMER.equips
 ff4.SLEDGEHAMMER.ranged = False
 ff4.SLEDGEHAMMER.magnetic = False
 ff4.SLEDGEHAMMER.throwable = False
 ff4.SLEDGEHAMMER.sprite = ff4.EARTHHAMMER.sprite
 ff4.SLEDGEHAMMER.swing = ff4.EARTHHAMMER.swing
 ff4.SLEDGEHAMMER.slash = ff4.EARTHHAMMER.slash
 ff4.SLEDGEHAMMER.palette = ff4.SILVERSWORD.palette
 ff4.SLEDGEHAMMER.attributes = ff4.WOODENHAMMER.attributes
 ff4.SLEDGEHAMMER.attack = 85
 ff4.SLEDGEHAMMER.hit = 75
 ff4.SLEDGEHAMMER.statbuff.stats = [False, False, True, False, True]
 ff4.SLEDGEHAMMER.statbuff.amount = 1
 for index in range(8):
  ff4.SLEDGEHAMMER.races.flags[index] = False
 ff4.SLEDGEHAMMER.races.flags[ff4.config.race_names.index("Machine")] = True
 ff4.SLEDGEHAMMER.name = "[HMR]Sledge"
 ff4.SLEDGEHAMMER.description[0] = "[HMR]Sledge             [KAT]85/75%"
 ff4.SLEDGEHAMMER.description[1] = "VIT+10, WIL+10. Two-handed."
 ff4.SLEDGEHAMMER.description[2] = "Strong against machines.   "
 ff4.SLEDGEHAMMER.description[3] = "                           "
 line = ff4.RUNEAXE.description[1].replace("Two-handed.", "")
 line = line.lstrip().ljust(27)
 ff4.RUNEAXE.description[1] = line
 ff4.items[0x29], ff4.items[0x48] = ff4.items[0x48], ff4.items[0x29]

# Normally the Mythril Staff casts Dispel, but if you use the Dispel
# spell customizatiotn, it is now un-reflectable and able to hit bosses
# (like the Wyvern), which makes it fairly high-level spell IMO, and so
# should not be castable for free off of a low-tier item.
def remove_dispel_from_staff(ff4):
 ff4.SILVERSTAFF.casts_spell = 0
 updated = ff4.SILVERSTAFF.description[1].replace("Casts [WHT]Dspel.", "")
 ff4.SILVERSTAFF.description[1] = updated

# Normally the Ogrekiller and Poison/Venom Axe both hurt giants.
# This seems a bit redundant to me, especially when combined with the
# edit that makes Venom Axe one-handed. This function makes it hurt
# slimes instead.
def customize_venom_axe(ff4):
 ff4.POISONAXE.races.flags[ff4.config.race_names.index("Giant")] = False
 ff4.POISONAXE.races.flags[ff4.config.race_names.index("Slime")] = True
 updated = ff4.POISONAXE.description[3].replace("giants", "slimes")
 ff4.POISONAXE.description[3] = updated
 
# I feel like the black shirt should give more WIS than the
# Sorcerer/Lords robe at the very least.
def customize_black_shirt(ff4):

 # Here I'm trying WIS +10
 ff4.BLACKROBE.statbuff.amount = 2
 ff4.BLACKROBE.description[2] = "WIS+10."

# The wizard robe seems like something that should boost both WIS and
# WIL, so let's replace WIL +5 with WIS/WIL +3.
def customize_wizard_robe(ff4):
 ff4.WIZARDROBE.statbuff.stats = [False, False, False, True, True]
 ff4.WIZARDROBE.statbuff.amount = 0
 ff4.WIZARDROBE.description[2] = "WIS+3, WIL+3."
 
# I feel like the crystal equipment should give a bigger WIL bonus than
# the paladin equipment.
def customize_crystal_gear(ff4):
 ff4.CRYSTALSHIELD.statbuff.amount = 1
 ff4.CRYSTALHELM.statbuff.amount = 1
 ff4.CRYSTALMAIL.statbuff.amount = 1
 ff4.CRYSTALGLOVE.statbuff.amount = 1
 ff4.CRYSTALSHIELD.description[1] = "WIL+5."
 ff4.CRYSTALHELM.description[1] = "WIL+5."
 updated = ff4.CRYSTALMAIL.description[1].replace("+3", "+5")
 ff4.CRYSTALMAIL.description[1] = updated
 ff4.CRYSTALGLOVE.description[1] = "WIL+5."

# Gaia Gear seems less like it should be a robe for wizards and more like a "vest" 
# type item.
def customize_gaia_gear(ff4):
 ff4.GAEAROBE.equips = ff4.KARATEROBE.equips

def customize_equipment(ff4):
 create_fairy_harp(ff4)
 remove_dispel_from_staff(ff4)
 customize_venom_axe(ff4)
 customize_black_shirt(ff4)
 customize_wizard_robe(ff4)
 customize_crystal_gear(ff4)
 customize_gaia_gear(ff4)

# This makes Rosa's Pray command proportional so that it stays about
# equally useful regardless of how far along in the game you are.
# It also makes it work more often.
def customize_pray(ff4):
 
 # Set Pray's spell to "Remedy" (the enemy skill that heals MHP/10 HP).
 ff4.rom.data[0x1EA64] = 0x84

 # Set Pray's success rate to 3/4 instead of 1/2.
 ff4.rom.data[0x1EA56] = 0xC0
 
# This makes Tellah's Recall command only cast spells he doesn't
# already have.
def customize_recall(ff4):
 
 # Recall consists of four "rare" slots followed by four common slots.
 newrares = [
  ff4.STONE_SPELL, 
  ff4.QUAKE_SPELL, 
  ff4.WEAK_SPELL, 
  ff4.FATAL_SPELL
 ]
 newcommons = [
  ff4.FIRE3_SPELL,
  ff4.ICE3_SPELL,
  ff4.LIT3_SPELL,
  ff4.VIRUS_SPELL
 ]
 newspells = newrares + newcommons
 for index, spell in enumerate(newspells):
  ff4.rom.data[0x1EC26 + index * 8] = ff4.spells.index(spell)

# This is a custom IPS patch that allows Edward's "Heal"/"Salve"
# command to select any healing item and apply its full effect to the
# entire party. I haven't tested it with J-items, but there is a known
# bug with Life potions / phoenix downs where ALL your other allies
# have to be KOed in order for it to revive ANY of them. I didn't
# create this patch and thus have no idea how to fix it. I still feel
# like it's a huge boost to Edward though, even with that bug.
def customize_heal(ff4, patchpath):
 ff4.rom.apply_patch(patchpath + "Custom Salve.ips", "unheadered")

# Change Bear into Rage (self-berserk) and give it to Cid.
# Only does this if J-commands are enabled.
def customize_bear(ff4):

 # Define some aliases so it's easier to work with.
 yang1 = ff4.YANG1
 yang2 = ff4.YANG2
 cid = ff4.CID1
 # yang1 = ff4.actors[7]
 # yang2 = ff4.actors[13]
 # cid = ff4.actors[14]
 bear = ff4.commands.index(ff4.BEAR_COMMAND)
 fight = ff4.commands.index(ff4.FIGHT_COMMAND)
 item = ff4.commands.index(ff4.ITEM_COMMAND)
 blank = 0xFF
 # bear = 0x0F
 # fight = 0x00
 # item = 0x01
 # blank = 0xFF
 
 # First determine if J-commands are enabled. We do this by checking
 # if Yang has the Bear command.
 if bear in yang1.commands:
  
  # Remove it from both Yangs.
  yang1.commands.remove(bear)
  yang1.commands.append(blank)
  # yang1.commands[3] = item
  # yang1.commands[4] = blank
  yang2.commands.remove(bear)
  yang2.commands.append(blank)
  # yang2.commands = yang1.commands
  
  # And give it to Cid
  cid.commands = [fight, bear, item, blank, blank]
  
  # Then make it cast Berserk instead of Protect.
  ff4.rom.data[0x1E897] = ff4.spells.index(ff4.BERSK_SPELL)
  
  # And rename it to "Rage"
  ff4.BEAR_COMMAND.name = "Rage"
  
  # Also give Berserk a 100% hit rate so that Cid never wastes a turn
  # doing nothing by selecting this command.
  ff4.BERSK_SPELL.hit = 100

# This is just a shortcut to apply all the command customizations in
# one function call.
def customize_commands(ff4, patchpath):
 customize_pray(ff4)
 customize_recall(ff4)
 customize_heal(ff4, patchpath)
 customize_bear(ff4)

# In vanilla, at sufficiently high levels, Yang suddenly stops gaining
# max HP. This fixes that.
def fix_yang_hp(ff4):
 for index in range(60, 70):
  ff4.YANG.levelups[index].hp = 152

# This will give Tellah some better levelup stats as well as some
# better HP and even some MP.
def improve_tellah_levels(ff4):
 for index, levelup in enumerate(ff4.TELLAH.levelups):
  if index >= ff4.TELLAH.level:

   # He just doesn't gain STR and that's fine.
   levelup.statbonus.stats[0] = False

   # He can get 1 AGI every second level.
   levelup.statbonus.stats[1] = (index % 2 == 0)

   # He can get 1 VIT every third level.
   levelup.statbonus.stats[2] = (index % 3 == 0)

   # He'll also get 1 WIS and 1 WIL every third level, but staggered.
   levelup.statbonus.stats[3] = (index % 3 == 1)
   levelup.statbonus.stats[3] = (index % 3 == 2)
   levelup.statbonus.amount = 1

   # His HP boosts start at 24 and go up by 12 every four levels.
   levelup.hp = int((index - ff4.TELLAH.level) / 4) * 12 + 24

   # His MP boosts start at 1 and double every ten levels.
   levelup.mp = 2 ** int((index - ff4.TELLAH.level) / 10)

 # Except after level 70 where his MP goes up by 30 every level :O
 ff4.TELLAH.levelups[69].mp = 30

# Give DK Cecil some better HP progression.
# It doesn't have to compete with the Paladin but it should at least
# be closer to tank HP than mage HP.
def improve_dk_levels(ff4):

 # Now his HP gains will start at 20 and go up by 10 every six levels.
 for index, levelup in enumerate(ff4.DKCECIL.levelups):
  if index >= ff4.DKCECIL.level:
   levelup.hp = int((index - ff4.DKCECIL.level) / 6) * 10 + 20

# This is simply a shortcut to apply all the levelup customizations in
# a single function call.
def customize_levelups(ff4):
 fix_yang_hp(ff4)
 improve_tellah_levels(ff4)
 improve_dk_levels(ff4)
 
# Makes the sealed cave exitable from everywhere but crystal room and
# evil wall room. You shouldn't be able to skip the boss fight just by
# casting Exit, but there's no need to prevent people from skipping a
# plot scene that no longer exists.
def exit_sealed_cave(ff4):
 sealed_cave_rooms = list(range(330, 343)) + [344, 324]
 for index in sealed_cave_rooms:
  ff4.maps[index].exitable = True
  ff4.maps[index].warpable = True

# Makes Mount Ordeals exitable. I don't think that leads to any abuses
# and I'm really not sure why it wasn't exitable to begin with. I get
# why you shouldn't be able to warp back into the mirror room but exit
# should be safe.
def exit_mount_ordeals(ff4):
 mount_ordeals_rooms = list(range(132, 136))
 for index in mount_ordeals_rooms:
  ff4.maps[index].exitable = True

# This applies an IPS patch that makes it so that the black chocobo no
# longer automatically goes home when you remount it.
def black_chocobo_fix(ff4, patchpath):
 ff4.rom.apply_patch(patchpath + "Black Chocobo Fix.ips", "headered")

# This allows you to land next to Kaipo instead of having to walk all
# that way across the desert.
def kaipo_landing_tile(ff4):

 # Put a grass tile next to Kaipo town.
 ff4.overworld.tiles[104][124] = 0x16

 # Cosmetic adjustments to make it look more natural.
 ff4.overworld.tiles[104][123] = 0x34
 ff4.overworld.tiles[105][123] = 0x11
 ff4.overworld.tiles[105][124] = 0x33
 
 # And as a QOL thing let's make all Kaipo's exits put us on that tile.
 for trigger in ff4.KAIPO_TOWN.triggers:
  if trigger.type == "teleport":
   if trigger.map == 0xFB:
    trigger.new_x = 124
    trigger.new_y = 104
    # print(ff4.display(trigger))

# This is simply a shortcut to apply all the map related customizations
# in a single function call.
def customize_maps(ff4, patchpath):
 exit_sealed_cave(ff4)
 exit_mount_ordeals(ff4)
 black_chocobo_fix(ff4, patchpath)
 kaipo_landing_tile(ff4)

# Pale Dim always seemed to me like a "Holy" element dragon,
# especially given its name and appearance, almost a parallel to the
# dark dragon the Dark Elf becomes. So I feel like it only makes sense
# that it should be weak to Shadow.
def pale_dim_weakness(ff4):
 ff4.PALE_DIM.add_weakness("Shadow")
 ff4.PALE_DIM.add_resistance("Holy")

# Despite its name, the Mist Dragon is not actually a Dragon. This
# wouldn't have mattered in the vanilla game but it does matter in
# Free Enterprise, so let's fix it.
def customize_mist_dragon(ff4):
 ff4.D_MIST.add_race("Dragon")

 # It also seems like a holy element dragon, so let's make it weak to
 # Shadow while we're at it.
 ff4.D_MIST.add_weakness("Shadow")

# Bahamut definitely should have the "Dragon" flag.
def bahamut_dragon(ff4):
 ff4.BAHAMUT.add_race("Dragon")

# This makes it so that the monsters that seem like golems or other
# normally inanimate objects that have been somehow animated or made
# alive should count as the same creature type as "machines". This
# makes the category a little more general so hence why I'm calling it
# "constructs". Examples would be the EvilWall, the trap doors, the
# Staleman and its palette swaps, etc.
def customize_constructs(ff4):

 # I figure the easiest and most maintainable thing would be to just
 # make a list of every monster I think should have these properties,
 # regardless of whether they already have them in vanilla or not.
 constructs = [
  ff4.PUPPET,
  ff4.BOMB,
  ff4.GRAYBOMB,
  ff4.STONEMAN,
  ff4.BEAMER,
  ff4.EVILDOLL,
  ff4.BALLOON,
  ff4.GRENADE,
  ff4.LAST_ARM,
  ff4.D_MACHIN,
  ff4.TRAPDOOR,
  ff4.IRONMAN,
  ff4.ALERT,
  ff4.MACHINE,
  ff4.MACGIANT,
  ff4.EVILMASK,
  ff4.REDGIANT,
  ff4.STALEMAN,
  ff4.SEARCHER,
  ff4.MOMBOMB,
  ff4.CAL,
  ff4.BRENA,
  ff4.CALBRENA,
  ff4.BALNAB,
  ff4.BALNAB_Z,
  ff4.EVILWALL,
  ff4.CPU,
  ff4.DEFENDER,
  ff4.ATTACKER
 ]
 
 # Then we just batch process the whole list.
 for monster in constructs:
  monster.add_race("Machine")
  # monster.has_races = True
  # construct_race = ff4.config.race_names.index("Machine")
  # monster.races.flags[construct_race] = True

# A number of monsters in vanilla seem like they should be floating,
# yet do not actually float. Even if they display the "bobbing up and
# down in the air" animation, Quake etc seems to still work on them.
# This makes it so the monsters that seem to me like they should be
# floating are actually floating. This may not work when they are
# spawned in or transformed from another monster, but I don't know what
# I can really do about that.
# Note that this does NOT take the floating away from monsters that do
# float even if it may seem like they shouldn't, like the fish.
def customize_floating(ff4):
 
 # As with the constructs, the easiest thing to do is simply create a
 # list of the monsters I think should float, regardless of whether
 # they already do or not, then process the whole list.
 floaters = [
  ff4.EAGLE,
  ff4.FLOATEYE,
  ff4.CAVE_BAT,
  ff4.SANDMOTH,
  ff4.WEEPER,
  ff4.SPIRIT,
  ff4.COCKTRIC,
  ff4.ROC_BABY,
  ff4.RAVEN,
  ff4.SOUL,
  ff4.VAMPGIRL,
  ff4.GRUDGER ,
  ff4.VAMPLADY,
  ff4.GLOMWING,
  ff4.SCREAMER,
  ff4.GHOST,
  ff4.BOMB,
  ff4.GRAYBOMB,
  ff4.ROC,
  ff4.GIANTBAT,
  ff4.BALLOON,
  ff4.GRENADE,
  ff4.PLAGUE,
  ff4.LAST_ARM,
  ff4.RED_EYE,
  ff4.ROCKMOTH,
  ff4.WERE_BAT,
  ff4.BREATH,
  ff4.MIND,
  ff4.ALERT,
  ff4.GING_RYU,
  ff4.FATALEYE,
  ff4.SEARCHER,
  ff4.BLUE_D,
  ff4.KING_RYU,
  ff4.CLAPPER,
  ff4.PALE_DIM,
  ff4.RED_D,
  ff4.D_MIST,
  ff4.MOMBOMB,
  ff4.VALVALIS,
  ff4.SHADOW,
  ff4.CPU,
  ff4.DEFENDER,
  ff4.ATTACKER
 ]
 
 # Then process the whole list.
 for monster in floaters:
  
  # Air weakness is what determines whether a monster is immune to
  # Quake and similar.
  monster.add_weakness("Air")
  # monster.has_weaknesses = True
  # air_element = ff4.config.element_names.index("Air")
  # monster.weaknesses.flags[air_element] = True


# Changing the monster data like this is what makes it so that this
# customizer has to be a Gamingway script and can't be a static IPS
# patch. The monster shuffling leaves the monsters' indexes alone, and
# presumably most of their properties, but it changes around their
# stats each time. Combined with the fact that the monster data records
# are variable length, this means that if you were to create an IPS for
# a particular seed, it won't work for other seeds because it will be
# changing monster stats to what they were for the seed you created the
# patch relative to.
def customize_monsters(ff4):
 pale_dim_weakness(ff4)
 bahamut_dragon(ff4)
 customize_mist_dragon(ff4)
 customize_constructs(ff4)
 customize_floating(ff4)

# I feel like there are no currently available flag settings in Free
# Enterprise that provide a good amount of standard supplies like tents
# and potions and stuff in the chests. Treasure shuffle can do that
# somewhat but it goes almost a bit too far and good equipment is a bit
# too rare. So my solution is to play with J items on but then convert
# all J items in chests to standard things like remedies or phoenix
# downs or whatever.
def convert_jitems(ff4):

 # Which items we convert to depends on the tier of the item being
 # converted. The summon orbs aren't coverted.
 tier2 = [
  ff4.THORRAGE,
  ff4.HERMES,
  ff4.STARVEIL,
  ff4.MUTEBELL,
  ff4.UNIHORN,
  ff4.LIFE,
  ff4.TENT,
  ff4.EXIT
 ]
 
 tier3 = [
  ff4.SUCCUBUS,
  ff4.SILKWEB,
  ff4.KAMIKAZE,
  ff4.CURE2,
  ff4.ETHER1,
  ff4.HEAL
 ]
 
 tier4 = [
  ff4.BIGBOMB,
  ff4.BOREAS,
  ff4.ZEUSRAGE,
  ff4.STARDUST,
  ff4.VAMPIRE,
  ff4.ILLUSION,
  ff4.FIREBOMB,
  ff4.BLIZZARD,
  ff4.LITBOLT,
  ff4.GAIADRUM,
  ff4.GRIMOIRE,
  ff4.CURE3,
  ff4.ETHER2,
  ff4.SOMADROP,
  ff4.CABIN
 ]
 
 tier5 = [
  ff4.BACCHUS,
  ff4.HRGLASS2,
  ff4.COFFIN,
  ff4.ELIXIR,
  ff4.SIREN
 ]
 
 tier6 = [
  ff4.AUAPPLE,
  ff4.AGAPPLE
 ]
 
 tier7 = [
  ff4.MOONVEIL
 ]
 
 # Now we loop through all the treasure triggers and convert all
 # items of each tier to their corresponding supplies. If there are
 # multiple possible items to covert to, we use the parity (odd/even)
 # of the item index to decide which one. I could randomize it, but
 # doing it this way ensures that the same seed will always produce
 # the same output rom, even when patched with this utility.
 for map in ff4.maps:
  for trigger in map.triggers:
   if trigger.type == "treasure":
    if not trigger.has_money:
     item = ff4.items[trigger.contents]
     even = trigger.contents % 2
     if item in tier2:
      if even:
       trigger.contents = ff4.items.index(ff4.LIFE)
      else:
       trigger.contents = ff4.items.index(ff4.LIFE)
     elif item in tier3:
      if even:
       trigger.contents = ff4.items.index(ff4.TENT)
      else:
       trigger.contents = ff4.items.index(ff4.ETHER1)
     elif item in tier4:
      if item != ff4.CABIN:
       if even:
        trigger.contents = ff4.items.index(ff4.CURE2)
       else:
        trigger.contents = ff4.items.index(ff4.CABIN)
     elif item in tier5:
      trigger.contents = ff4.items.index(ff4.CURE3)
     elif item in tier6:
      trigger.contents = ff4.items.index(ff4.ETHER2)
     elif item in tier7:
      trigger.contents = ff4.items.index(ff4.ELIXIR)
     
      