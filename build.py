#!/usr/bin/env python3
"""Build the BeastHHBB and iBeasts - Project ja-Kha'jay Patch (see README.md, BUILDING.md, NOTES.md).

For NPCs that Project ja-Kha'jay (JKJ) and a beast mod (iBeasts, BeastHHBB) both edit, each patch record is the JKJ
record with its appearance fields replaced by the beast mod's. One ESL-flagged plugin per JKJ setup (6 variants, same
file name, picked by the FOMOD), plus optional add-ons for supported mods. No assets are shipped: the FaceGen comes
from the installed beast mods, which must win file conflicts over JKJ.
Usage: python3 build.py            (serializes inputs/, prints masters and records, writes no plugin)
       python3 build.py --write    (also writes the plugins to dist/ and packages the FOMOD zip)
Needs: dotnet, python3, the Spriggit.Yaml.Skyrim 0.41.0 DLL (SPRIGGIT_DLL or auto-detected), inputs/ (BUILDING.md).
"""
import hashlib, os, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
INPUTS = pathlib.Path(os.environ.get("INPUTS", HERE / "inputs"))
Y = HERE / "build"
INPUT_PLUGINS = ["IBeasts - 3dNpcs.esp", "BeastHHBB.esp", "JKJ - 3DNPC.esp", "Project ja-Kha'jay- Khajiit Diversity.esp",
                 "JKJ - USSEP Patch.esp", "JKJ - AI Overhaul Patch.esp", "JKJ- Ohmes Risaad Restored.esp",
                 "H2HBooksandTrainers.esp"]


def find_dll():  # SPRIGGIT_DLL, else Spriggit's own download folder, else the NuGet cache
    if os.environ.get("SPRIGGIT_DLL"):
        return pathlib.Path(os.environ["SPRIGGIT_DLL"])
    for base in [pathlib.Path(d) / "Spriggit/Translations/Spriggit.Yaml.Skyrim/0.41.0"
                 for d in {os.environ.get("TMPDIR", ""), tempfile.gettempdir(), "/tmp"} if d] + [
            pathlib.Path.home() / ".nuget/packages/spriggit.yaml.skyrim/0.41.0"]:
        hits = sorted(base.rglob("Spriggit.Yaml.Skyrim.dll")) if base.is_dir() else []
        if hits:
            return hits[0]
    sys.exit("Spriggit.Yaml.Skyrim.dll 0.41.0 not found. See BUILDING.md ('Spriggit'), or set SPRIGGIT_DLL.")


def serialize_inputs(dll):  # fresh YAML of every input; warns if an input differs from the hashed version
    missing = [f for f in INPUT_PLUGINS if not (INPUTS / f).is_file()]
    if missing:
        sys.exit("missing input(s) in " + str(INPUTS) + ": " + ", ".join(missing) + " (see BUILDING.md)")
    for line in (HERE / "inputs.sha256").read_text().splitlines():
        want, name = line.split(None, 1)
        if hashlib.sha256((INPUTS / name.strip()).read_bytes()).hexdigest() != want:
            print(f"warning: {name.strip()} differs from the version this patch was written for", file=sys.stderr)
    shutil.rmtree(Y, ignore_errors=True)
    for f in INPUT_PLUGINS:
        run(["dotnet", str(dll), "serialize", "-i", str(INPUTS / f), "-o", str(Y / f"yaml-{f[:-4]}"),
             "-g", "SkyrimSE", "-p", "Spriggit.Yaml.Skyrim", "-v", "0.41.0"])
    print(f"serialized {len(INPUT_PLUGINS)} input plugins")
NAME = "BeastHHBB iBeasts - JKJ Patch"
TITLE = "BeastHHBB and iBeasts - Project ja-Kha'jay Patch"
CARAVAN = ["01B1CF", "01B1D0", "01B1D1", "01B1D2", "01B1D3", "01B1D5", "01B1D6", "01B1D7", "01B1D9", "01B1DA"]
MAJHAD = "01B1D5"

# Master order in the plugin headers: a valid load order of every plugin the patch can master (each after its own
# masters). A master not listed here stops the build.
ORDER = ["Skyrim.esm", "Update.esm", "Dawnguard.esm", "HearthFires.esm", "Dragonborn.esm",
         "Unofficial Skyrim Special Edition Patch.esp", "3DNPC.esp", "AI Overhaul.esp", "BeastHHBB.esp",
         "H2HBooksandTrainers.esp", "Project ja-Kha'jay- Khajiit Diversity.esp", "JKJ - USSEP Patch.esp",
         "JKJ - AI Overhaul Patch.esp", "IBeasts - 3dNpcs.esp", "JKJ - 3DNPC.esp", "JKJ- Ohmes Risaad Restored.esp",
         f"{NAME}.esp"]

# Variants: which optional JKJ plugins the user has. Each variant masters its own, so it always loads after them.
CARAVAN_P = {"ussep": {"JKJ - USSEP Patch.esp"}, "aio": {"JKJ - AI Overhaul Patch.esp"},
             "both": {"JKJ - USSEP Patch.esp", "JKJ - AI Overhaul Patch.esp"}}
RISAAD_P = {"ohmes": {"JKJ- Ohmes Risaad Restored.esp"}, "default": set()}
VARIANTS = {f"{c}-{r}": cm | rm for c, cm in CARAVAN_P.items() for r, rm in RISAAD_P.items()}
CORE = {"Skyrim.esm", "Unofficial Skyrim Special Edition Patch.esp", "3DNPC.esp", "BeastHHBB.esp",
        "Project ja-Kha'jay- Khajiit Diversity.esp", "IBeasts - 3dNpcs.esp", "JKJ - 3DNPC.esp"}
# Record base: the last of these, among the variant's plugins, that edits the NPC. AI Overhaul after USSEP so "both"
# keeps AI Overhaul's packages (its records are the USSEP patch's plus packages).
BASE_ORDER = ["Project ja-Kha'jay- Khajiit Diversity", "JKJ - USSEP Patch", "JKJ - AI Overhaul Patch",
              "JKJ- Ohmes Risaad Restored", "JKJ - 3DNPC"]

# taken from the beast mod; everything else (factions, AI, perks, USSEP/AI Overhaul fixes) stays as in the JKJ record
APPEARANCE = {"Race", "HeadParts", "HairColor", "HeadTexture", "TextureLighting", "FaceMorph", "FaceParts",
              "TintLayers", "Height", "Weight", "WornArmor", "DefaultOutfit"}
# extra fields taken from the beast mod for single NPCs
EXTRA = {"01B1D2": {"Perks", "Configuration"}}  # Kharjo: BeastHHBB's 11 perks, CalcMaxLevel 160, DoesntAffectStealthMeter
# Optional add-ons for supported mods: one small plugin each, mastering the main patch and the supported mod, that
# copies the supported mod's fields onto NPCs the main patch overrides. Installed by the FOMOD only if that mod is active.
ADDONS = {"hand-to-hand": dict(plugin="H2HBooksandTrainers", fields={"Class", "Factions", "Items"}, npcs=[MAJHAD],
                               name=f"{NAME} - Hand to Hand",
                               desc="Hand to Hand trainer class, faction and items for Ma'jhad on top of the main patch.")}


def ibeasts_records():  # iBeasts donor records for the NPCs both JKJ - 3DNPC and iBeasts override
    jkj = {p.name for p in (Y / "yaml-JKJ - 3DNPC/Npcs").glob("*.yaml")}
    ib = {p.name: p for p in (Y / "yaml-IBeasts - 3dNpcs/Npcs").glob("*.yaml")}
    return [ib[n] for n in sorted(ib.keys() & jkj)]


def blocks(text):  # top-level YAML keys -> their lines; Spriggit writes list items of a top-level key at column 0
    out, key = {}, None
    for l in text.splitlines():
        if l and not l[0].isspace() and not l.startswith("- "):
            key = l.split(":")[0]
            out[key] = []
        out[key].append(l)
    return out


def unblock(b):
    return "".join(l + "\n" for v in b.values() for l in v)


def overlay(base, src, take):  # base blocks with the `take` fields replaced by src's (added/dropped as src has them)
    keys = list(base)
    for i, k in enumerate(src):  # src-only keys go after their src-order predecessor
        if k in take and k not in base:
            prev = [x for x in list(src)[:i] if x in keys]
            keys.insert(keys.index(prev[-1]) + 1 if prev else len(keys), k)
    return {k: (src[k] if k in take else base[k]) for k in keys if not (k in take and k not in src)}


def merge(base, donor):
    w, d = blocks(base.read_text()), blocks(donor.read_text())
    assert w["FormKey"] == d["FormKey"], f"FormKey mismatch: {base.name} / {donor.name}"
    return unblock(overlay(w, d, APPEARANCE | EXTRA.get(w["FormKey"][0][9:15], set())))


def pick(plugin, ids):  # records by FormID from a serialized plugin; must find each exactly once
    out = []
    for i in ids:
        hits = list((Y / f"yaml-{plugin}/Npcs").glob(f"* - {i}_*.yaml"))
        assert len(hits) == 1, f"{plugin}: {i} found {len(hits)} times"
        out.append(hits[0])
    return out


def base_for(fk, plugins):
    have = [p for p in BASE_ORDER if f"{p}.esp" in plugins and list((Y / f"yaml-{p}/Npcs").glob(f"* - {fk[:6]}_*.yaml"))]
    assert have, f"{fk}: no JKJ plugin of the variant edits it"
    return have[-1]


def masters_for(recs, extra):  # every plugin a record belongs to or references, plus `extra`, in ORDER
    text = "".join(recs.values())
    found = set(re.findall(r"^FormKey: [0-9A-F]{6}:(.+)$", text, re.M)) | set(re.findall(r"[0-9A-F]{6}:(.+?\.es[pml])\b", text))
    canon = {m.lower(): m for m in ORDER}
    unknown = sorted(m for m in found | extra if m.lower() not in canon)
    assert not unknown, f"masters not in ORDER: {unknown}"
    return sorted({canon[m.lower()] for m in found | extra}, key=ORDER.index)


def write_plugin(name, recs, masters, desc, out_y, esp, rt):
    """Deserialize `recs` (YAML file name -> text) into an ESL-flagged plugin, then round-trip check it."""
    shutil.rmtree(out_y, ignore_errors=True)
    (out_y / "Npcs").mkdir(parents=True)
    for f, m in recs.items():
        (out_y / "Npcs" / f).write_text(m)
    mrefs = "".join(f"  - Master: {m}\n    FileSize: 0\n" for m in masters)
    (out_y / "RecordData.yaml").write_text(
        "SpriggitSource:\n  PackageName: Spriggit.Yaml.Skyrim\n  Version: 0.41.0\n"
        f"ModKey: {name}.esp\nGameRelease: SkyrimSE\nModHeader:\n  Flags:\n  - Small\n"
        "  Stats:\n    Version: 1.7\n    NextFormID: 2048\n  Author: skyrim-workspace\n"
        f"  Description: {desc}\n  MasterReferences:\n{mrefs}  INTV: 1\n")
    esp.parent.mkdir(parents=True, exist_ok=True)
    run(["dotnet", str(DLL_PATH), "deserialize", "-i", str(out_y), "-o", str(esp)])
    shutil.rmtree(rt, ignore_errors=True)
    run(["dotnet", str(DLL_PATH), "serialize", "-i", str(esp), "-o", str(rt),
         "-g", "SkyrimSE", "-p", "Spriggit.Yaml.Skyrim", "-v", "0.41.0"])
    got = {p.name: p for p in (rt / "Npcs").glob("*.yaml")}
    assert sorted(got) == sorted(recs), f"{esp.name}: record set changed in round trip"
    for f, m in recs.items():
        assert sorted(m.splitlines()) == sorted(got[f].read_text().splitlines()), f"{esp.name}: round trip differs: {f}"
    hdr = (rt / "RecordData.yaml").read_text()
    assert "- Small" in hdr and re.findall(r"Master: (.+)", hdr) == masters, f"{esp.name}: header round trip failed"


def build(write):
    donors = ibeasts_records() + pick("BeastHHBB", CARAVAN + ["01B1DB", "013298", "01C195"])
    fk = {d: re.search(r"^FormKey: (.+)$", d.read_text(), re.M).group(1) for d in donors}
    dist = HERE / "dist" / TITLE
    if write:
        shutil.rmtree(dist, ignore_errors=True)
    desc = ("iBeasts (27 Interesting NPCs Khajiit) and BeastHHBB (13 Khajiit) win appearance over Project ja-Kha'jay. "
            "Requires iBeasts and BeastHHBB to win loose file conflicts over Project ja-Kha'jay.")
    print(f"== {NAME}.esp (ESL flag, 0 new records)")
    built = {}
    for v, extra in VARIANTS.items():
        recs = {}
        for d in donors:
            base = pick(base_for(fk[d], CORE | extra), [fk[d][:6]])[0]
            recs[base.name] = merge(base, d)
        assert len(recs) == 40, f"expected 40 records, got {len(recs)}: inputs changed"
        masters = masters_for(recs, CORE | extra)
        built[v] = recs
        print(f"masters [{v}]: " + ", ".join(masters))
        if write:
            write_plugin(NAME, recs, masters, desc, Y / "out" / v, dist / v / f"{NAME}.esp", Y / "roundtrip" / v)
            print(f"OK [{v}]: round-trips to the same {len(recs)} records, {len(masters)} masters")
    print("records: 40 (27 iBeasts + 13 BeastHHBB): JKJ record of the variant + beast mod appearance fields")

    for folder, a in ADDONS.items():
        recs = {}
        for fid in a["npcs"]:
            main = {v: [(f, t) for f, t in r.items() if f" - {fid}_" in f][0] for v, r in built.items()}
            assert len(set(main.values())) == 1, f"{fid}: main patch record differs between variants; add-on needs variants"
            f, t = main["ussep-default"]
            recs[f] = unblock(overlay(blocks(t), blocks(pick(a["plugin"], [fid])[0].read_text()), a["fields"]))
        masters = masters_for(recs, {f"{NAME}.esp", f"{a['plugin']}.esp"})
        print(f"\n== {a['name']}.esp (optional, folder {folder}): {len(recs)} record(s), masters: " + ", ".join(masters))
        if write:
            write_plugin(a["name"], recs, masters, a["desc"], Y / "out" / folder, dist / folder / f"{a['name']}.esp",
                         Y / "roundtrip" / folder)
            print(f"OK [{folder}]: round-trips to the same {len(recs)} record(s), {len(masters)} masters")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or "ERR" in r.stdout:
        sys.exit(f"failed: {' '.join(cmd)}\n{r.stdout}\n{r.stderr}")


def package():  # FOMOD zip: fomod/ + one folder per variant and per add-on
    from xml.dom import minidom
    import zipfile
    src, built = HERE / "fomod", HERE / "dist" / TITLE
    for x in ("info.xml", "ModuleConfig.xml"):
        minidom.parse(str(src / x))
    sources = set(re.findall(r'source="([^"]+)"', (src / "ModuleConfig.xml").read_text()))
    assert sources == set(VARIANTS) | set(ADDONS), f"ModuleConfig sources {sorted(sources)} != built folders"
    out = HERE / "dist" / f"{TITLE}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for x in ("info.xml", "ModuleConfig.xml"):
            z.write(src / x, f"fomod/{x}")
        for f in sorted(p for p in built.rglob("*") if p.is_file() and p.name != ".DS_Store"):
            z.write(f, f.relative_to(built).as_posix())
        n = len(z.infolist())
    print(f"OK: {out.name} ({n} files)")


if __name__ == "__main__":
    DLL_PATH = find_dll()
    serialize_inputs(DLL_PATH)
    build("--write" in sys.argv)
    if "--write" in sys.argv:
        package()
    else:
        print("\nDRY RUN: no plugin written. Re-run with --write.")
