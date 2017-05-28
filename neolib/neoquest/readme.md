# Neoquest Automation notes

I'm going to run thru creating a game in normal mode and writing the query
params as I go.

root url for now: http://www.neopets.com/games/neoquest/neoquest.phtml


# Create game

created normal game, params are: ?create=1&game_diff=0
(create true, game_diff == normal == 0 - implying evil! is 1? and insane is
 2?)

after that create call, it simply calls back to the root without params to
start skill selection.


## Character Creation

### Skill Select

skill selection seems complicated, but i'm sure it's easy if you figure it
out.

You start with 7 points available.
There are js prompts on qmarks which popup info. Bots don't need to know that.
Fire weapons 1 = ?skill_choice=1001&
Ice " = ?skill_choice=2001&
Shock " 3001
Spectral " 4001
Life " 5001

They increase naturally, ie. Fire weapons = 1001, Firepower = 1002, fire ball
= 1003, wall of flame = 1004

Max skill points in ANY skill = 10 (To improve the next skill in a tree, the
level below must be equal to the next increment you want. ie. fire weapons
= 3, firepower = 2. You can upgrade firepower to 3, but not past it.
So each tree can have total spend = 40

At any point, you can restart by sending along param cc_restart=1
You confirm creation is complete with: cc_accept=1
(( can you complete creation without allocating all starting points??? ))


### Starting Weapon

pass along ?weapon_choice={type number}
where type number is the prefix x001 from element selection.
fire is 1, ice is 2, shock is 3, spectral is 4, and life is 5

Use cc_accept to continue on, or select a different weapon by just making
another weapon_choice request.


### Confirmation

A final chance to review your character, and use
cc_accept=1 to move on, or
cc_restart=1 to restart character creation entirely.

Continuing with a cc_accept here leads you to a final page without any params.
Get the root url again to begin playing. :)


## In-Game menu access

- Options: access options by passing along action=options
- Talk: action=talk&target={npc_id} (eleus batrin is 90010004, yeesh)
- Move: action=move&movedir={1-8}
  (1 is northwest, follow right across each row to southeast at 8)
- Change movement type: movetype={1-3} (normal, hunting, sneaking)
- Inventory: action=items
- Skills: action=skill


### Options

You can turn on music in this game?!? WTF?
action=options&{envon,fighton,bosson,allon}=1

You can start a new game from here:
action=options&startnew=1&diff={0:normal, 1:evil, 2:insane}

Return to map with a root call. (Probably not necessary at all for a bot)


### Talk

This seems... complicated.
idea from https://github.com/JDongian/Neoquest/blob/master/grind.py
-> don't need to know NPC ids, because you can just navigate to them and know
that they're there... So the servers will treat it as a no-op if you're not
with the target.
Boris = 90010001 and he just heals you I guess
lummock = 90010002
morax dorangis = 90010003
choras tillie = 90010005


### Move

In general it's
action=move&movedir={1-8}
Could be also:
action=move&movelink={portal_id}

### Inventory

### Skills

Looks like an ideal build for me is something like:
fortitude, evasion, reflex, absorption, shockwave, lifesteal

Ice seems to have nice offensive. glacier strike (highest level, gross)
Never invest points into resurrection, you won't die :)

## Fighting
Seems... mostly done! yowza!!! There is probably a lot of complicated stuff
I can add, but... yay!


# ETC Dev notes
- current goal:
    make it print nice 'current state' output / return this as a thing.
- next goal:
    make it able to navigate & build a map file && REMEMBER LAST LOCATION.
    - graphml format?
    - python libraries for this?
    - we have diagonal movement ...
    - how do we know we've reached the ends of the maps, as opposed to not knowing
        that there may be an edge somewhere?


#### Current Todos:
- also, some kind of "Strategy" module
    (ie. a sequence of skill points to allocate)
    (and also possibly some kind of indication of where to grind, which order to complete milestones)
- make state print nicer (as above)
- make a "portal" move command - TODO: check if local action
- inventory (action = items) + meaningful state
- battle; using potions/etc (no local actions)
- decide on how to know the value of a pot [ based on val = ogval * (1 + 0.1 x lifewep) ]? or parse?
- make state/player parsing both: better AND smarter (fewer updates to independent objects, etc)
- add testing?? does that even make sense?


#### Done
- make something that can tell you which movement mode you're in
- make player better: split on pipes, and then like split on spaces/colons... well, i made it better...
- create function that can perform a level up sequence
- parse skills so you can know which level your skills are at
- actually make level up work! (it does! yay!)
