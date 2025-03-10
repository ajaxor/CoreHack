-- NetHack 3.6	dungeon dungeon.lua	$NHDT-Date: 1652196135 2022/05/10 15:22:15 $  $NHDT-Branch: NetHack-3.7 $:$NHDT-Revision: 1.4 $
-- Copyright (c) 1990-95 by M. Stephenson
-- NetHack may be freely redistributed.  See license for details.
--
-- The dungeon description file.
dungeon = {
   {
      name = "The Dungeons of Doom",
      bonetag = "D",
      base = 30,
      range = 0,
      alignment = "unaligned",
      themerooms = "themerms.lua",
      branches = {
         {
            name = "The Quest",
            base = 20,
            range = 0,
            branchtype = "portal"
         },
         {
            name = "The Elemental Planes",
            base = 1,
            branchtype = "no_down",
            direction = "up"
         }
      },
      levels = {
         {
            name = "oracle",
            bonetag = "O",
            base = 4,
            range = 0,
            alignment = "neutral"
         },
         {
            name = "minetn",
            bonetag = "T",
            base = 8,
            range = 0,
            nlevels = 7,
            flags = "town"
         },
         {
           name = "minefill",
           base = 9,
           range = 0,
         },
         {
           name = "minefill",
           base = 10,
           range = 0
         },
         {
           name = "minefill",
           base = 11,
           range = 0
         },
         {
            name = "orcus",
            bonetag = "G",
            base = 24,
            range = 0
         },
         {
            name = "juiblex",
            bonetag = "J",
            base = 28,
            range = 0
         },
         {
            name = "castle",
            base = -1
         }
      }
   },
    {
        name = "The Quest",
        bonetag = "Q",
        base = 5,
        range = 2,
        levels = {
            {
            name = "x-strt",
            base = 1,
            range = 1
            },
            {
            name = "x-loca",
            bonetag = "L",
            base = 3,
            range = 1
            },
            {
            name = "x-goal",
            base = -1
            },
        }
    },    
    {
        name = "The Elemental Planes",
        bonetag = "E",
        base = 6,
        alignment = "unaligned",
        flags = { "mazelike" },
        entry = -2,
        levels = {
            {
            name = "astral",
            base = 1
            },
            {
            name = "water",
            base = 2
            },
            {
            name = "fire",
            base = 3
            },
            {
            name = "air",
            base = 4
            },
            {
            name = "earth",
            base = 5
            },
            {
            name = "dummy",
            base = 6
            },
        }
    },
    {
        name = "The Tutorial",
        base = 2,
        flags = { "mazelike", "unconnected" },
        levels = {
            {
            name = "tut-1",
            base = 1,
            },
            {
            name = "tut-2",
            base = 2,
            },
        }
    }
}