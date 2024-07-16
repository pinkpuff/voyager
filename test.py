import sys
sys.path.append("E:/Projects/Hacking/Gamingway/Source")
from gamingway import FF4Rom
from event import Instruction

patchpath = "../Resources/"

args = sys.argv
if len(args) < 2:
 # inputfile = "../Resources/ff4.smc"
 inputfile = "../Resources/fe.smc"
else:
 inputfile = args[1]
if len(args) < 3:
 outputfile = "../game.smc"
else:
 print(len(args))
 outputfile = args[2]

extended_instruction_names = {
 0x00: "End event",
 0x01: "Goto event",
 0x02: "If",
 0x03: "Age Rydia",
 0x04: "Placement set visible",
 0x05: "Placement set invisible",
 0x06: "Put Enterprise",
 0x07: "Party leader Cecil",
 0x08: "Activate NPC",
 0x09: "Deactivate NPC",
 0x0A: "Party leader character",
 0x0B: "Rememberize Tellah",
 0x0C: "Clear shadow party slot",
 0x0D: "Save vehicles from Mist",
 0x0E: "Load extra NPC palette",
 0x0F: "Reset NPC palette",
 0x10: "Debug buff",
 0x11: "Placement set visible by party leader",
 0x12: "Reload placement sprite",
 0x13: "Set placement speed",
 0x14: "Give float",
 0x15: "Clear party",
 0x16: "Debug fill shadow party",
 0x17: "Gosub event",
 0x18: "Return",
 0x19: "Load NPC palette",
 0x1A: "Test mode startup",
 0x1B: "Save music",
 0x1C: "Restore music",
 0x1D: "Take all",
 0x1E: "Tint off",
 0x1F: "Give starter kit",
 0x20: "Key item location hint",
 0x21: "Give character",
 0x22: "Paladinize Cecil",
 0x23: "Check character alt version",
 0x24: "Boss battle",
 0x25: "Check flag",
 0x26: "Give item side effects",
 0x27: "Init axtor name",
 0x28: "Deliver reward from slot",
 0x29: "Check flag equals",
 0x2A: "Post boss battle",
 0x2B: "Increase key item count",
 0x2C: "Retrieve character",
 0x2D: "Load wacky sprite",
 0x2E: "Load axtor fashion code",
 0x2F: "Give pink tail item",
 0x30: "Init vignette loop",
 0x31: "Check vignettes done",
 0x32: "Load vignette map",
 0x33: "Draw vignette window",
 0x34: "Next vignette",
 0x35: "Finalize stats",
 0x36: "Save endgame time",
 # 0x37 unused?
 0x38: "Set key item used",
 # 0x39 - 0x3F unused?
 0x40: "Load spell name",
 0x41: "Load reward name from slot",
 0x42: "Load objective name for index",
 # 0x43 - 0x4F unused?
 0x50: "Objectives impl. apply staged",
 0x51: "Objectives impl. show staged completion messages",
 0x52: "Objectives tick",
 0x53: "Objectives tick boss slot",
 0x54: "Objectives tick reward slot",
 0x55: "Objectives list in dialog"
}

extended_parameter_count = {
 # These are all guesses...
 0x00: 0,
 0x01: 1,
 0x02: 3,
 0x03: 0,
 0x04: 1,
 0x05: 1,
 0x06: 3,
 0x07: 0,
 0x08: 1,
 0x09: 1,
 0x0A: 1,
 0x0B: 0,
 0x0C: 1,
 0x0D: 0,
 0x0E: 0,
 0x0F: 0,
 0x10: 0,
 0x11: 1,
 0x12: 1,
 0x13: 2,
 0x14: 0,
 0x15: 0,
 0x16: 0,
 0x17: 1,
 0x18: 0,
 0x19: 0,
 0x1A: 0,
 0x1B: 0,
 0x1C: 0,
 0x1D: 0,
 0x1E: 0,
 0x1F: 0,
 0x20: 1,
 0x21: 1,
 0x22: 0,
 0x23: 1,
 0x24: 1,
 0x25: 1,
 0x26: 1,
 0x27: 1,
 0x28: 1,
 0x29: 2,
 0x2A: 0,
 0x2B: 0,
 0x2C: 1,
 0x2D: 1,
 0x2E: 2,
 0x2F: 0,
 0x30: 0,
 0x31: 0,
 0x32: 0,
 0x33: 0,
 0x34: 0,
 0x35: 0,
 0x36: 0,
 # 0x37 unused?
 0x38: 1,
 # 0x39 - 0x3F unused?
 0x40: 1,
 0x41: 2,
 0x42: 1,
 # 0x43 - 0x4F unused?
 0x50: 0,
 0x51: 0,
 0x52: 0,
 0x53: 1,
 0x54: 1,
 0x55: 0
}

def display_event(main, index):
 event = main.events[index]
 for instruction in event.script:
  if instruction.code == 0xE6:
   result = "*"
   result += extended_instruction_names[instruction.parameters[0]]
   if len(instruction.parameters) > 1:
    for parameter in instruction.parameters[1:]:
     result += " {:02X}".format(parameter)
  else:
   result = instruction.display(main)
  print(result)

ff4 = FF4Rom(inputfile)
ff4.config.parameter_count[0xE6] = 1
ff4.config.instruction_names[0xE6] = ""
ff4.read()

# Re-interpret E6 event instructions
for index in range(len(ff4.events)):
 event = ff4.events[index]
 event.script = []
 pointer = ff4.rom.EVENT_POINTERS_START + index * 2
 address = ff4.rom.read_wide(pointer) + ff4.rom.EVENT_POINTER_BONUS
 offset = address
 instruction = ff4.rom.data[offset]
 while instruction != 0xFF:
  parameters = []
  if instruction == 0xE6:
   offset += 1
   parameters.append(ff4.rom.data[offset])
   count = extended_parameter_count[parameters[0]]
  else:
   count = ff4.config.parameter_count[instruction]
  offset += 1
  if count > 0:
   for index in range(count):
    parameters.append(ff4.rom.data[offset + index])
   offset += count
  event.script.append(Instruction(instruction, parameters))
  instruction = ff4.rom.data[offset]  

display_event(ff4, 0x10)
# print(extended_instruction_names[0x02])
# print(extended_parameter_count[0x02])
# print(ff4.events[0x8].display(ff4))
# print(ff4.config.instruction_names[0xDA])

ff4.write()
ff4.save(outputfile)