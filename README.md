# BeastHHBB and iBeasts - Project ja-Kha'jay Patch

**Version 1.0**

An ESL-flagged (`.esp`) compatibility patch that fixes headless and wrong-faced Khajiit when **Project ja-Kha'jay** is installed together with **BeastHHBB** and **iBeasts - Interesting Npcs replacer**. The beast mods win the look of every NPC both sides edit; Project ja-Kha'jay keeps everything else.

Skyrim Special Edition and Anniversary Edition. Plugin only: no meshes, textures or other assets from any mod.

## Requirements

- [BeastHHBB](https://www.nexusmods.com/skyrimspecialedition/mods/38480) and its optional file **iBeasts - Interesting Npcs replacer**
- [Project ja-Kha'jay - Khajiit NPC Diversity Overhaul](https://www.nexusmods.com/skyrimspecialedition/mods/57610) with `JKJ - USSEP Patch.esp`, `JKJ - AI Overhaul Patch.esp`, or both
- [Project ja-Kha'jay - Interesting NPCs Khajiit Addon](https://www.nexusmods.com/skyrimspecialedition/mods/60447)
- [Interesting NPCs SE (3DNPC)](https://www.nexusmods.com/skyrimspecialedition/mods/29194)
- [Unofficial Skyrim Special Edition Patch](https://www.nexusmods.com/skyrimspecialedition/mods/266)

### Supported optional mods

Not required. The installer detects them and offers or selects the matching files:

| Mod | What the installer does |
|---|---|
| `JKJ - USSEP Patch.esp` / `JKJ - AI Overhaul Patch.esp` (Project ja-Kha'jay options) | installs the main plugin built for the one you have, or for both |
| `JKJ- Ohmes Risaad Restored.esp` (Project ja-Kha'jay option) | installs the main plugin built to load after it; Ri'saad still gets the BeastHHBB look |
| [Hand to Hand - Trainers and Skill Books Addon](https://www.nexusmods.com/skyrimspecialedition/mods/59790) (`H2HBooksandTrainers.esp`) | offers the add-on `BeastHHBB iBeasts - JKJ Patch - Hand to Hand.esp`, selected automatically |

**Why the Hand to Hand add-on.** Hand to Hand makes Ma'jhad a Hand to Hand trainer by editing his record (trainer class, faction, items). The Project ja-Kha'jay records, which this patch builds on, also edit Ma'jhad and would overwrite that. The add-on puts the three fields back on top of this patch and loads after both. Without Hand to Hand, the option is greyed out and nothing extra is installed.

### Target versions
Built and checked against BeastHHBB 3.8, iBeasts 1.2.0.0, Project ja-Kha'jay 4.08.1, Project ja-Kha'jay Interesting NPCs Addon 3.05, Hand to Hand Trainers and Skill Books Addon 1.0.5. Project ja-Kha'jay is no longer supported by its author. If one of these mods updates, rebuild (see [BUILDING.md](BUILDING.md)); the build stops if the overlap changed.

## The Problem

Each NPC's look comes from two places that are resolved separately: the NPC record (race, head parts, face shape, tints), won by **plugin load order**, and the FaceGen head mesh and tint texture, won by **mod manager priority** for loose files. When two mods edit the same NPC and each ships its own FaceGen, the two can be won by different mods. The record then describes one head and the mesh is another: dark face, neck seam or missing head.

1. **27 Interesting NPCs Khajiit:** `JKJ - 3DNPC.esp` wins the record (Cathay-Raht race, JKJ head parts) while iBeasts wins the FaceGen. Neither plugin masters the other, so LOOT does not fix their order either.
2. **11 caravan Khajiit** (Ri'saad, Ahkari, Ma'dran, Kharjo and the rest): the Project ja-Kha'jay plugins win the record while BeastHHBB wins the FaceGen.
3. **Mazaka and J'zargo:** same split once BeastHHBB wins the FaceGen (below), unless `BeastHHBB - Ai Overhaul Patch.esp` happens to win their records.

## What the Patch Does

### Replaced (beast mods win)
- **Look of 40 NPCs:** race, head parts, hair color, head texture, skin tone, face shape, face parts, tint layers, height, weight, skin (`WornArmor`) and default outfit come from iBeasts (27) or BeastHHBB (13).
- **Kharjo:** also takes BeastHHBB's 11 perks, level cap 160 (was 30) and the "doesn't affect stealth meter" flag.

### Kept (Project ja-Kha'jay)
- Everything else on those records: factions, AI packages, inventory, voice, class, skills, and the USSEP and AI Overhaul fixes the Project ja-Kha'jay plugins carry.

### Lost
- **Project ja-Kha'jay's look** for these 40 NPCs, including the Ohmes-raht Ri'saad from `JKJ- Ohmes Risaad Restored.esp`.
- **JKJ outfits** for 5 of the 27 Interesting NPCs (Akh'ir, Inari, Qa'Dojo, Serazi, S'vashni) and Zaynabi.
- **Edits of other mods to these NPCs that the Project ja-Kha'jay records do not carry**, for example Tamrielic Distribution's inventory item on the caravan Khajiit. They are already lost without this patch, because the Project ja-Kha'jay plugins load after those mods.

### Not touched
- 4 NPCs only `JKJ - 3DNPC.esp` edits (Darksteel3, FinalDarksteel5, JeerahCaptive3, Male4Darksteel) keep the JKJ look.
- Every other Khajiit and Argonian.

The full NPC list and field-level detail are in [NOTES.md](NOTES.md).

## Install

1. Enable the Project ja-Kha'jay plugins you want to use (and Hand to Hand, if you use it). The installer reads which plugins are enabled; a disabled plugin counts as not installed.
2. Install the archive with your mod manager. The installer shows one page:
   - **Your Project ja-Kha'jay plugins:** six options, the one matching your enabled plugins is preselected. It installs one plugin, `BeastHHBB iBeasts - JKJ Patch.esp`.
   - **Optional support for other mods:** Hand to Hand, selected when `H2HBooksandTrainers.esp` is enabled, greyed out otherwise.
3. Set the file priority (below), then sort plugins with LOOT. The masters make LOOT place the patch after every plugin it needs.

The installer stops with a missing-requirements message unless `3DNPC.esp`, `JKJ - 3DNPC.esp`, `IBeasts - 3dNpcs.esp`, `BeastHHBB.esp`, `Project ja-Kha'jay- Khajiit Diversity.esp`, USSEP and at least one of the two JKJ patches are enabled.

**Reinstall** after enabling or disabling `JKJ - USSEP Patch.esp`, `JKJ - AI Overhaul Patch.esp`, `JKJ- Ohmes Risaad Restored.esp` or `H2HBooksandTrainers.esp`. Otherwise the game may not start (missing master) or the headless NPCs come back.

### Required file priority

The patch ships no FaceGen; the faces come from iBeasts and BeastHHBB, so their files must win over Project ja-Kha'jay:

- **iBeasts - Interesting Npcs replacer** must overwrite **Project ja-Kha'jay - Interesting NPCs Khajiit Addon** (54 shared files, the 27 Interesting NPCs).
- **BeastHHBB** must overwrite **Project ja-Kha'jay - Khajiit NPC Diversity Overhaul** (26 shared files: the 11 caravan Khajiit, Mazaka, J'zargo).

Every file these mods share is FaceGen of the 40 patched NPCs (measured with the target versions above), so this order changes nothing else. It is the opposite of the Project ja-Kha'jay Addon FAQ (load iBeasts first so JKJ wins); that advice is for keeping JKJ's look, which this patch replaces.

**Mod Organizer 2**
1. Left pane: drag `iBeasts - Interesting Npcs replacer` and `BeastHHBB` **below** both Project ja-Kha'jay mods (lower = higher priority, wins the conflict).
2. Check: the conflict icon on iBeasts and BeastHHBB shows a plus (they overwrite), on the two Project ja-Kha'jay mods a minus.
3. Right pane: sort with LOOT. The patch itself can sit anywhere in the left pane.

**Vortex**
1. On `iBeasts - Interesting Npcs replacer`, click the lightning-bolt conflict icon and set **Load after** `Project ja-Kha'jay - Interesting NPCs Khajiit Addon`; on `BeastHHBB`, set **Load after** `Project ja-Kha'jay - Khajiit NPC Diversity Overhaul`. In this dialog "Load after" means "overwrites its files"; it is not plugin load order.
2. If you already set the opposite rule (the JKJ FAQ order), remove it first: Vortex reports a rule cycle otherwise.
3. Deploy, then sort plugins (Plugins page, Sort Now).

**Check in game:** with More Informative Console, click a patched NPC (Ri'saad, J'zargo, Inari): "Base last changed by" must be `BeastHHBB iBeasts - JKJ Patch.esp` (for Ma'jhad with Hand to Hand: the add-on). Another plugin there loads after the patch and edits that NPC: it needs its own patch or must load earlier.

**Saves:** the patch adds no new records, only overrides, so removing it leaves nothing orphaned. Mid-playthrough behavior for NPCs you have already met has not been tested.

**Upgrading from an earlier patch:** remove `JKJ - iBeasts 3DNPC Patch`, `JKJ - BeastHHBB Patch`, `JKJ - Beast Mods FaceGen Patch` and `BeastHHBB - JKJ FaceGen Patch` first.

## Build from Source

See [BUILDING.md](BUILDING.md).

## Verification Status

- All 6 main plugin variants and the Hand to Hand add-on round-trip through Spriggit line-for-line; an independent byte parse confirms the ESL flag, the expected masters per variant and unique `NPC_` records (40 per variant, 1 in the add-on).
- For the 38 NPCs of the earlier patch (`BeastHHBB - JKJ FaceGen Patch` 2.2, built from a load order with both JKJ patches, Ri'saad Restored and Hand to Hand), the matching variant plus the Hand to Hand add-on give byte-identical records.
- FOMOD validates against the ModConfig 5.0 XSD; an evaluator over every enabled/disabled/missing combination of the four detected plugins confirms the preselection. MO2: correct option preselected (tested).
- **Not tested in game in this form, not tested in Vortex.**

## Credits and Permissions

Sources: each mod's Nexus description via the Nexus API, and the "Permissions and credits" section of every page below, read on 2026-11-01.

### BeastHHBB, including iBeasts - Interesting Npcs replacer
- **Author:** Mharlek1. **Page:** [BeastHHBB](https://www.nexusmods.com/skyrimspecialedition/mods/38480). iBeasts is an optional file on this page; its standalone page (50355) is removed.
- **Used by this patch:** appearance fields from `BeastHHBB.esp` (13 NPCs) and `IBeasts - 3dNpcs.esp` (27 NPCs). Both are masters. No assets.
- **Permissions:** modification allowed with credit; upload elsewhere not allowed; some assets belong to other authors. Author notes: "You are free to upload patches using this esp and modifying it for the patches, but not the assets, thus still requiring this mod." Credit and a link required.
- **Consequence:** allowed with credit and a link, as long as no BeastHHBB / iBeasts assets (FaceGen included) are shipped. That is why the patch is plugin only and relies on the file priority above.

### Project ja-Kha'jay - Khajiit NPC Diversity Overhaul and Interesting NPCs Khajiit Addon
- **Author:** SassiestAssassin (formerly allosnywisegirl). **Pages:** [Diversity Overhaul](https://www.nexusmods.com/skyrimspecialedition/mods/57610); [Interesting NPCs Khajiit Addon](https://www.nexusmods.com/skyrimspecialedition/mods/60447).
- **Used by this patch:** the non-appearance part of the records in `Project ja-Kha'jay- Khajiit Diversity.esp`, `JKJ - USSEP Patch.esp`, `JKJ - AI Overhaul Patch.esp`, `JKJ- Ohmes Risaad Restored.esp` and `JKJ - 3DNPC.esp`. They are masters. No assets.
- **Permissions:** modification allowed with credit; asset use: 57610 "must get permission", 60447 "not allowed under any circumstances". Author notes: 57610 "If you want to make a patch with this mod as a master, go for it! Let me know, and I'll add it to the description."; 60447 "Patches that require this mod as a master are allowed."
- **Consequence:** allowed with credit. The Addon FAQ recommends the opposite file priority; this patch deliberately reverses it for these 40 NPCs.

### Interesting NPCs SE (3DNPC)
- **Author:** Kris Takahashi (SE port by KaptainCnucklz and co). **Page:** [Interesting NPCs SE](https://www.nexusmods.com/skyrimspecialedition/mods/29194).
- **Used by this patch:** `3DNPC.esp` as a master. No assets. **Permissions:** upload, modification and asset use allowed with credit.

### Unofficial Skyrim Special Edition Patch (USSEP)
- **Author:** Unofficial Patch Project Team. **Page:** [USSEP](https://www.nexusmods.com/skyrimspecialedition/mods/266).
- **Used by this patch:** master; its fixes on these records are carried through unaltered (only appearance fields change). **Author's instructions:** "You are permitted to use the unofficial patches as master files in your own work for the purpose of ensuring that fixes are not lost." "Altering fixes is specifically prohibited."

### Hand to Hand - An Adamant Addon (Trainers and Skill Books Addon)
- **Authors:** Simon Magus, Colinswrath and Jelidity. **Page:** [Hand to Hand](https://www.nexusmods.com/skyrimspecialedition/mods/59790).
- **Used by the optional add-on:** Ma'jhad's trainer class, faction and items from `H2HBooksandTrainers.esp`, which is a master of the add-on. No assets.
- **Permissions:** upload, modification and asset use allowed with credit. Author notes: credit all of the authors who contributed, not only Simon.

## License

The code and documentation in this repository (`build.py`, `fomod/`, `inputs.sha256`, the Markdown files) are under
the [MIT License](LICENSE). The built plugins in the FOMOD zip are derived from the mods above and stay under their
permissions, as described in Credits and Permissions.
