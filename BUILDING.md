# Building from source

Back to [README.md](README.md). The technical notes are in [NOTES.md](NOTES.md).

This repository contains no plugin data from other mods. It holds only the build script, the FOMOD and the
decisions in `build.py`. You supply the original plugins; Spriggit extracts them on your machine and the build
applies the BeastHHBB / iBeasts look to the Project ja-Kha'jay records and writes the new plugins.

## Platforms

Tested: macOS (arm64) only. Expected to work, but not run:

- **Linux:** needs `python3` and the .NET 10 SDK.
- **Windows:** run `python build.py` from `cmd`, PowerShell or Git Bash (no `bash` needed). Set `SPRIGGIT_DLL` if the
  automatic DLL lookup (below) does not find it.

## What you need

Download these yourself and put the eight plugin files in `inputs/` (create the folder):

| File in `inputs/` | Where it comes from |
|---|---|
| `BeastHHBB.esp` | [BeastHHBB](https://www.nexusmods.com/skyrimspecialedition/mods/38480?tab=files&file_id=467776) 3.8, main file "BeastHHBB" (file ID 467776), `data/` in the archive |
| `IBeasts - 3dNpcs.esp` | the same page, main file "iBeasts - Interesting Npcs replacer" 1.2 ([file ID 536994](https://www.nexusmods.com/skyrimspecialedition/mods/38480?tab=files&file_id=536994)), `data/` |
| `Project ja-Kha'jay- Khajiit Diversity.esp` | [Project ja-Kha'jay](https://www.nexusmods.com/skyrimspecialedition/mods/57610?tab=files&file_id=520523) 4.08.1 (file ID 520523), `Project ja-Kha'jay/00 Data/00DATA CORE/` |
| `JKJ - USSEP Patch.esp` | the same archive, `00 Data/Patches/USSEP Patch/` |
| `JKJ - AI Overhaul Patch.esp` | the same archive, `00 Data/Patches/AI Overhaul Patch/` |
| `JKJ- Ohmes Risaad Restored.esp` | the same archive, `00 Data/Optional Patches/0NPC Replacers/Ohmes Ri'saad/` |
| `JKJ - 3DNPC.esp` | [Project ja-Kha'jay - Interesting NPCs Addon](https://www.nexusmods.com/skyrimspecialedition/mods/60447?tab=files&file_id=455820) 3.05 (file ID 455820), `JKJ - 3DNPC/` |
| `H2HBooksandTrainers.esp` | [Hand to Hand](https://www.nexusmods.com/skyrimspecialedition/mods/59790?tab=files&file_id=312593), optional file "Hand to Hand - Trainers and Skill Books Addon" 1.0.5 (file ID 312593), archive root |

The BeastHHBB and iBeasts plugins give the look of every patched NPC; the Project ja-Kha'jay plugins give
everything else on those records, one set per installer variant; `H2HBooksandTrainers.esp` gives Ma'jhad's trainer
fields for the optional add-on. Nothing from them is stored in this repository. `inputs.sha256` lists the file
hashes this patch was written against. A different hash only prints a warning; different content stops the build
(see below). Set `INPUTS` to use another folder.

Tools: the .NET 10 SDK, Python 3, and Spriggit 0.41.0 (see below, most Skyrim users do not have it).

## Spriggit

[Spriggit](https://github.com/Mutagen-Modding/Spriggit) is a command line tool from the Mutagen project
that converts a Skyrim plugin (`.esp`, `.esm`, `.esl`) into a folder of readable YAML files and back. It is
a modding developer tool, not part of a normal Skyrim install, and **you only need it to rebuild the patch**.
To just use the patch, install the FOMOD zip and skip this section.

The build calls the Skyrim serializer package `Spriggit.Yaml.Skyrim` 0.41.0 directly, not the CLI. It looks for
`Spriggit.Yaml.Skyrim.dll` in this order:

1. `SPRIGGIT_DLL`, if set;
2. `<temp>/Spriggit/Translations/Spriggit.Yaml.Skyrim/0.41.0/`, where the Spriggit CLI downloads it;
3. `~/.nuget/packages/spriggit.yaml.skyrim/0.41.0/`.

**With the CLI** (needs the .NET 10 SDK, `dotnet --version` must print 10 or higher):

```
dotnet tool install --global Spriggit.CLI --version 0.41.0
spriggit serialize --InputPath "inputs/BeastHHBB.esp" --OutputPath some-empty-folder --GameRelease SkyrimSE --PackageName Spriggit.Yaml.Skyrim --PackageVersion 0.41.0
```

The first conversion downloads the package into the temp folder above. The CLI prints its version with a nonzero
exit status; that is normal. On macOS the CLI itself crashes during a conversion (`kernel32.dll` cannot be loaded
by a dependency's process tracker), so there use the package download instead.

**Without the CLI:** `dotnet restore` rejects `Spriggit.Yaml.Skyrim` (it is a tool-type package). Download
`https://api.nuget.org/v3-flatcontainer/spriggit.yaml.skyrim/0.41.0/spriggit.yaml.skyrim.0.41.0.nupkg`, unzip it
(a `.nupkg` is a zip) and set `SPRIGGIT_DLL` to `tools/net10.0/any/Spriggit.Yaml.Skyrim.dll` inside it, or unzip it
to `~/.nuget/packages/spriggit.yaml.skyrim/0.41.0/`. With that DLL the build ran to the end on macOS (arm64, .NET 10).

These steps are untested on a machine that has never run Spriggit.

## Run

```
python3 build.py           # check run: extracts the inputs, prints masters and records, writes no plugin
python3 build.py --write   # builds, checks and packages
```

Output: `dist/BeastHHBB and iBeasts - Project ja-Kha'jay Patch.zip`. Intermediate files are in `build/`.

What the script does:

1. Checks that all eight inputs exist, compares them with `inputs.sha256` and serializes them to YAML with Spriggit.
2. Builds the main plugin `BeastHHBB iBeasts - JKJ Patch.esp` once per installer variant (`ussep|aio|both` x
   `ohmes|default`, one per combination of optional Project ja-Kha'jay plugins):
   - picks the 40 NPCs: the 27 both iBeasts and `JKJ - 3DNPC.esp` edit, plus the 11 caravan Khajiit, Mazaka and J'zargo;
   - takes each NPC's record from the last Project ja-Kha'jay plugin of the variant that edits it;
   - replaces every appearance field (race, head parts, face, tints, height, weight, skin, outfit) with the
     BeastHHBB or iBeasts value, and Kharjo's perks and level settings with BeastHHBB's;
   - masters every plugin the records belong to or reference, plus the variant's Project ja-Kha'jay plugins, so
     the patch always loads after them.
3. Builds the Hand to Hand add-on: the main patch's Ma'jhad with the trainer class, faction and items from
   `H2HBooksandTrainers.esp`, mastering both.
4. Deserializes each plugin, re-serializes it and compares every record, the ESL flag and the master list with the
   source, then checks the FOMOD XML is well-formed and zips the package.

The build refuses to continue if:
- the record count is not 40 (an input changed which NPCs it edits);
- a FormID is missing from or found twice in an input;
- a master is not in `ORDER` in `build.py`;
- the add-on's NPC differs between variants (one add-on must fit every variant);
- a round trip differs.

That is the guard against building from different versions of the input mods.

The result is deterministic: the same inputs give byte-identical plugins.

## Changing the patch

All decisions are at the top of `build.py`:

- Which fields come from BeastHHBB / iBeasts: `APPEARANCE`, plus per-NPC `EXTRA` (Kharjo).
- Which Project ja-Kha'jay plugin a record comes from: `BASE_ORDER`; the variants: `CARAVAN_P` x `RISAAD_P`.
- Master order: `ORDER` (a valid load order of every plugin the patch can master).
- Optional support for another mod: add an entry to `ADDONS` (plugin, fields, NPCs, name), add its plugin to
  `ORDER` and `INPUT_PLUGINS`, and add an option to the "Optional support for other mods" group in
  `fomod/ModuleConfig.xml` (`defaultType NotUsable`, one pattern `Recommended` when its plugin is `Active`).
- The installer: `fomod/ModuleConfig.xml`, edited by hand. Validate it against the ModConfig 5.0 XSD after a change
  (the published `gemm` schema has a `type=" xs:string"` typo that libxml2 rejects: strip the space in a local copy).
  `package()` checks that its `source=` folders equal the built folders.
- After a build, `build/roundtrip/` holds each built plugin re-serialized. Spriggit drops unknown YAML fields
  silently, and item order inside a record can differ, so compare with lines sorted.

## Repository layout

```
build.py              Decisions, build, checks and packaging
inputs.sha256         Hashes of the input plugins this was written against
fomod/                FOMOD info.xml and ModuleConfig.xml shipped in the zip
README.md             What the patch does, install, credits
BUILDING.md           How to build from source
NOTES.md              Technical notes and the full record list
LICENSE               MIT, for the code and documentation (README, License)
inputs/               Your copies of the original plugins (not tracked)
build/, dist/         Generated (not tracked)
backups/              Local snapshots (not tracked)
```
