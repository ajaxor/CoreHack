-- NetHack gehennom orcus.lua modified for main dungeon
-- Repurposed from the original Orcus level
-- Now a ghost town level for the main dungeon

des.level_init({ style = "solidfill", fg = " ", lit = 0 });

-- Remove the shortsighted flag to make it less difficult
--des.level_flags("mazelevel")

local tmpbounds = selection.match("-");
local bnds = tmpbounds:bounds();
local bounds2 = selection.fillrect(bnds.lx, bnds.ly + 1, bnds.hx - 2, bnds.hy - 1);

-- A ghost town
local orcus1 = des.map({ halign = "center", valign = "center", map = [[
----------------------------------------------
||....|....|....|..............|....|........|
||....|....|....|..............|....|........|
||....|....|....|--...-+-------|.............|
||....|....|....|..............+.............|
||.........|....|..............|....|........|
|--+-...-+----+--....-------...--------.-+---|
|....................|.....|.................|
|....................|.....|.................|
|--+----....-+---....|.....|...----------+---|
||....|....|....|....---+---...|......|......|
||.........|....|..............|......|......|
|----...---------.....-----....+......|......|
||........................|....|......|......|
|----------+-...--+--|....|....----------+---|
||....|..............|....+....|.............|
||....+.......|......|....|....|.............|
||....|.......|......|....|....|.............|
----------------------------------------------
]], contents = function(rm)
   --des.mazewalk(00,06,"west")
   -- Entire main area
   --des.region({region={29,7,50,6},type="ordinary",lit=0, irregular=true, filled=1, joined=true})

   des.stair("down", 33, 16)
   des.stair("up", 4, 8)
   
   -- Wall "ruins"
   des.object("boulder",19,03)
   des.object("boulder",20,03)
   des.object("boulder",21,03)
   des.object("boulder",36,03)
   des.object("boulder",36,04)
   des.object("boulder",06,05)
   des.object("boulder",05,06)
   des.object("boulder",06,06)
   des.object("boulder",07,06)
   des.object("boulder",39,06)
   des.object("boulder",08,09)
   des.object("boulder",09,09)
   des.object("boulder",10,09)
   des.object("boulder",11,09)
   des.object("boulder",06,11)
   des.object("boulder",05,12)
   des.object("boulder",06,12)
   des.object("boulder",07,12)
   des.object("boulder",21,12)
   des.object("boulder",21,13)
   des.object("boulder",13,14)
   des.object("boulder",14,14)
   des.object("boulder",15,14)
   des.object("boulder",14,15)
   -- Doors
   des.door("closed",23,03)
   des.door("open",31,04)
   des.door("nodoor",03,06)
   des.door("closed",09,06)
   des.door("closed",14,06)
   des.door("closed",41,06)
   des.door("open",03,09)
   des.door("nodoor",13,09)
   des.door("open",41,09)
   des.door("closed",24,10)
   des.door("closed",31,12)
   des.door("open",11,14)
   des.door("closed",18,14)
   des.door("closed",41,14)
   des.door("open",26,15)
   des.door("closed",06,16)
   -- Special rooms
   des.altar({ x=24,y=08,align="noalign",type="altar" }) -- Changed from sanctum to regular altar
   des.region({ region={22,13,25,17},lit=0,type="morgue",filled=1 })
   des.region({ region={32,10,37,13},lit=1,type="shop",filled=1 })
   des.region({ region={12,01,15,05},lit=1,type="shop",filled=1 })
   -- Some traps.
   des.trap("spiked pit")
   des.trap("sleep gas")
   des.trap("anti magic")
   des.trap("fire")
   des.trap("fire")
   des.trap("fire")
   des.trap("magic")
   des.trap("magic")
   -- Some random objects
   des.object()
   des.object()
   des.object()
   des.object()
   des.object()
   des.object()
   des.object()
   des.object()
   des.object()
   des.object()
   des.object()
   des.object()
   -- Replace Orcus with some challenging but not overwhelming monsters
   des.monster("vampire lord",33,16)
   -- Reduced number of companions and made them less dangerous
   des.monster("human zombie",32,16)
   des.monster("wraith",32,15)
   des.monster("wraith",32,17)
   des.monster("vampire",35,17)
   des.monster("vampire",35,15)
   -- Randomly placed monsters (reduced number and difficulty)
   des.monster("skeleton")
   des.monster("skeleton")
   des.monster("skeleton")
   des.monster("skeleton")
   des.monster("skeleton")
   des.monster("shade")

   des.monster("giant zombie")
   des.monster("giant zombie")
   des.monster("giant zombie")
   des.monster("ettin zombie")
   des.monster("ettin zombie")
   des.monster("ettin zombie")
   des.monster("human zombie")
   des.monster("human zombie")
   des.monster("human zombie")
   des.monster("vampire")
   des.monster("vampire")
   -- A few more random monsters
   des.monster()
   des.monster()
   des.monster()
   des.monster()
   des.monster()
end });

-- Remove teleport restrictions

-- No need for hell_tweaks since this is no longer in Gehennom
