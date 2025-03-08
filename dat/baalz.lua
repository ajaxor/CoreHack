-- NetHack gehennom baalz.lua	$NHDT-Date: 1652196020 2022/05/10 15:20:20 $  $NHDT-Branch: NetHack-3.7 $:$NHDT-Revision: 1.4 $
--	Copyright (c) 1989 by Jean-Christophe Collet
--	Copyright (c) 1992 by M. Stephenson and Izchak Miller
-- NetHack may be freely redistributed.  See license for details.
--
des.level_init({ style = "solidfill", fg = " ", lit = 0 });

-- TODO FIXME: see baalz_fixup - the legs get removed currently.

-- des.level_flags("mazelevel", "corrmaze")
-- the two pools are fakes used to mark spots which need special wall fixups
-- the two iron bars are eyes and spots to their left will be made diggable
des.map({ halign = "right", valign = "center", map = [[
                                                 
                                                 
                                                 
                    ----          ---------      
           ----     |.|   ---------....|         
  ------    |.|  ----.----|.........|--P         
  F....|  ---.---|...........--------------      
---....|--|..................S............|----  
|...--....S..----------------|............S...|  
---....|--|..................|............|----  
  F....|  ---.---|...........-----S--------      
  ------    |.|  ----.----|.........|--P         
           ----     |.|   ---------....|         
                    ----          ---------      
                                                 
                                                 
                                                 
                                                 
]] });

-- Define this as a proper room that needs joining
--des.region({ region={29,9,3,3}, type="ordinary", lit=0, irregular=false, filled=0, joined=true })

-- des.levregion({ region = {01,00,28,20}, region_islev=1, exclude={15,1,70,16}, exclude_islev=1, type="stair-up" })
-- des.levregion({ region = {01,00,15,20}, region_islev=1, exclude={15,1,70,16}, exclude_islev=1, type="branch" })
--des.teleport_region({region = {01,00,15,20}, region_islev=1, exclude = {15,1,70,16}, exclude_islev=1 })
-- this actually leaves the farthest right column diggable
-- des.non_diggable(selection.area(00,00,47,12))
-- des.mazewalk(00,06,"west")
des.stair("up", 3,08)    
des.stair("down", 44,08)    
--des.door("locked",00,08)
-- The fellow in residence
des.monster("fire giant",35,08)
-- Some random weapons and armor.
des.object("[")
des.object("[")
des.object(")")
des.object(")")
des.object("*")
des.object("!")
des.object("!")
des.object("?")
des.object("?")
des.object("?")
des.object();
des.object();
-- Some traps.
des.trap("spiked pit")
des.trap("fire")
des.trap("sleep gas")
des.trap("anti magic")
des.trap("fire")
des.trap("magic")
des.trap("fire")
des.trap("fire")
-- Random monsters.
des.monster("ghost",37,09)
des.monster("&",32,07)
des.monster("&",38,09)
des.monster("L")
-- Some Vampires for good measure
des.monster("V")
des.monster("V")
des.monster("V")
des.monster("V")