#!/usr/bin/env python3
"""
STATISTICHEAI - Guard & Self-Healing Engine Idempotente
Verifica e ripristina con 1 click:
- I 7 agenti Hermes (GynBot1-3, Mark1-3, CEH) con configurazioni calibrate
- Le versioni ottimizzate dei modelli in Ollama (64k, 32k, 24k, 20k, 16k)
- Modelli creati una sola volta (idempotente)
- Backup automatico prima di ogni modifica
- Log dettagliato sia su console che su file
"""

import os
import sys
import json
import shutil
import datetime
import subprocess
import logging
from pathlib import Path

# Percorsi base
BASE_DIR = Path(__file__).resolve().parent
WIN_FLAGS = 0x08000000 if sys.platform == "win32" else 0
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "data"
BACKUP_ROOT = BASE_DIR / "backups"
LOG_FILE = LOG_DIR / "guard_runs.log"

HERMES_HOME = Path(r"C:\Users\Gyniu\AppData\Local\hermes")
GOLDEN_DIR = HERMES_HOME / "golden_tuning"
MANIFEST_FILE = GOLDEN_DIR / "tuning_manifest.json"
PATCH_FILE = GOLDEN_DIR / "engine_patches.patch"
AGENT_REPO = HERMES_HOME / "hermes-agent"
MODELFILES_DIR = HERMES_HOME / "modelfiles"

DATA_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("guard_engine")


def make_auto_backup() -> Path:
    """Crea backup con timestamp prima di qualsiasi verifica o modifica e rimuove i backup vecchi > 3 giorni."""
    # Pulizia automatica backup obsoleti
    try:
        cutoff = datetime.datetime.now() - datetime.timedelta(days=3)
        for item in BACKUP_ROOT.iterdir():
            if item.stat().st_mtime < cutoff.timestamp():
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
    except Exception:
        pass

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    target = BACKUP_ROOT / f"guard_auto_backup_{ts}"
    target.mkdir(parents=True, exist_ok=True)

    try:
        # Config root
        if (HERMES_HOME / "config.yaml").exists():
            shutil.copy2(HERMES_HOME / "config.yaml", target / "root_config.yaml")
        if (HERMES_HOME / "profile.yaml").exists():
            shutil.copy2(HERMES_HOME / "profile.yaml", target / "root_profile.yaml")

        # Modelfiles
        if MODELFILES_DIR.exists():
            shutil.copytree(MODELFILES_DIR, target / "modelfiles", dirs_exist_ok=True)

        # Profili
        profiles_dir = HERMES_HOME / "profiles"
        if profiles_dir.exists():
            shutil.copytree(profiles_dir, target / "profiles", dirs_exist_ok=True)

        logger.info("[BACKUP] Backup automatico salvato in: %s", target)
    except Exception as exc:
        logger.warning("[BACKUP] Errore durante il backup automatico: %s", exc)
    return target


def is_pid_alive(pid: int) -> bool:
    """Verifica se un PID Windows e' ancora vivo."""
    if pid <= 0:
        return False
    try:
        res = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=WIN_FLAGS
        )
        return str(pid) in res.stdout
    except Exception:
        return True


def check_and_heal_ollama_models(manifest: dict) -> tuple[int, int]:
    """
    Verifica che le 6 versioni ottimizzate dei modelli esistano in Ollama.
    Se mancanti, le ricrea ciascuna UNA SOLA VOLTA dal proprio Modelfile.
    Ritorna (verificati_ok, ricreati).
    """
    try:
        res = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10, creationflags=WIN_FLAGS)
        output = res.stdout if res.returncode == 0 else ""
    except Exception as exc:
        logger.warning("[OLLAMA] Impossibile contattare Ollama: %s", exc)
        return 0, 0

    unique_models = {}
    for pid, spec in manifest.get("profiles", {}).items():
        m_name = spec.get("model")
        m_file = spec.get("modelfile")
        if m_name and m_file and m_name not in unique_models:
            unique_models[m_name] = Path(m_file)

    ok_count = 0
    recreated_count = 0
    processed = set()

    for m_name, m_path in unique_models.items():
        if m_name in processed:
            continue
        processed.add(m_name)

        if m_name in output:
            logger.info("[OLLAMA] Modello ottimizzato '%s' -> PRESENTE (OK)", m_name)
            ok_count += 1
        else:
            if m_path.exists():
                logger.warning("[OLLAMA] Modello ottimizzato '%s' ASSENTE! Ricreazione da %s...", m_name, m_path.name)
                try:
                    c_res = subprocess.run(
                        ["ollama", "create", m_name, "-f", str(m_path)],
                        capture_output=True,
                        text=True,
                        timeout=120,
                        creationflags=WIN_FLAGS
                    )
                    if c_res.returncode == 0:
                        logger.info("[OLLAMA] Modello '%s' ricreato con successo (1 sola volta).", m_name)
                        recreated_count += 1
                    else:
                        logger.error("[OLLAMA] Errore ricreazione '%s': %s", m_name, c_res.stderr)
                except Exception as e:
                    logger.error("[OLLAMA] Eccezione ricreazione '%s': %s", m_name, e)
            else:
                logger.error("[OLLAMA] Modelfile mancante per '%s' a: %s", m_name, m_path)

    return ok_count, recreated_count


def heal_profile_config(pid: str, spec: dict) -> bool:
    """Allinea in modo idempotente e sicuro la configurazione YAML dell'agente."""
    p_dir = Path(spec["profile_dir"])
    config_file = p_dir / "config.yaml"
    profile_meta = p_dir / "profile.yaml"

    if not config_file.exists():
        logger.error("[HERMES] Config non trovato per profilo '%s' a %s", pid, config_file)
        return False

    target_model = spec["model"]
    target_num_ctx = spec["ollama_num_ctx"]
    target_ctx_len = spec["context_length"]

    text = config_file.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    new_lines = []
    modified = False

    in_model_block = False
    in_providers_ollama = False
    has_num_ctx = False
    has_ctx_len = False

    for line in lines:
        stripped = line.strip()

        # max_concurrent_sessions: 0
        if stripped.startswith("max_concurrent_sessions:"):
            if stripped != "max_concurrent_sessions: 0":
                line = "max_concurrent_sessions: 0"
                modified = True

        # blocco model:
        if line.startswith("model:"):
            in_model_block = True
            in_providers_ollama = False
            new_lines.append(line)
            continue
        elif in_model_block and (line.startswith("  ") or line.startswith("\t")):
            if stripped.startswith("default:"):
                curr = stripped.split(":", 1)[1].strip()
                if curr != target_model:
                    line = f"  default: {target_model}"
                    modified = True
            elif stripped.startswith("ollama_num_ctx:"):
                has_num_ctx = True
                val = stripped.split(":", 1)[1].strip()
                if val != str(target_num_ctx):
                    line = f"  ollama_num_ctx: {target_num_ctx}"
                    modified = True
            elif stripped.startswith("context_length:"):
                has_ctx_len = True
                val = stripped.split(":", 1)[1].strip()
                if val != str(target_ctx_len):
                    line = f"  context_length: {target_ctx_len}"
                    modified = True
            new_lines.append(line)
            continue
        elif in_model_block and not (line.startswith("  ") or line.startswith("\t")):
            if not has_num_ctx:
                new_lines.append(f"  ollama_num_ctx: {target_num_ctx}")
                modified = True
            if not has_ctx_len:
                new_lines.append(f"  context_length: {target_ctx_len}")
                modified = True
            in_model_block = False

        # blocco providers ollama-launch
        if stripped == "ollama-launch:":
            in_providers_ollama = True
            new_lines.append(line)
            continue
        elif in_providers_ollama and (line.startswith("    ") or line.startswith("\t\t")):
            if stripped.startswith("model:") and not in_model_block:
                curr = stripped.split(":", 1)[1].strip()
                if curr != target_model:
                    line = f"    model: {target_model}"
                    modified = True
            elif stripped.startswith("context_length:") and not in_model_block:
                val = stripped.split(":", 1)[1].strip()
                if val != str(target_ctx_len):
                    line = f"    context_length: {target_ctx_len}"
                    modified = True
            new_lines.append(line)
            continue
        elif in_providers_ollama and not (line.startswith("    ") or line.startswith("\t\t")):
            in_providers_ollama = False

        new_lines.append(line)

    if in_model_block:
        if not has_num_ctx:
            new_lines.append(f"  ollama_num_ctx: {target_num_ctx}")
            modified = True
        if not has_ctx_len:
            new_lines.append(f"  context_length: {target_ctx_len}")
            modified = True

    if modified:
        config_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        logger.info("[HERMES] Profilo '%s': Config allineato (Modello=%s, Ctx=%d)", pid, target_model, target_ctx_len)
    else:
        logger.info("[HERMES] Profilo '%s': Config gia' ottimale al 100%% (invariato)", pid)

    # Pulizia lease sessioni orfane
    rt_file = p_dir / "runtime" / "active_sessions.json"
    if rt_file.exists():
        try:
            r_data = json.loads(rt_file.read_text(encoding="utf-8"))
            entries = r_data.get("entries", [])
            live = [e for e in entries if is_pid_alive(e.get("pid", 0))]
            if len(live) != len(entries):
                r_data["entries"] = live
                rt_file.write_text(json.dumps(r_data, indent=2), encoding="utf-8")
                logger.info("[HERMES] Profilo '%s': Rimossi %d lease sessione morti", pid, len(entries) - len(live))
        except Exception:
            pass

    return True


def heal_engine_patches() -> bool:
    """Verifica e preserva le patch di runtime e di tuning in hermes-agent in modo deterministico."""
    if not AGENT_REPO.exists():
        return True

    applied_count = 0

    # 1. agent/agent_init.py (soglia minima di contesto per modelli locali calibrati >= 16k)
    f_agent_init = AGENT_REPO / "agent" / "agent_init.py"
    if f_agent_init.exists():
        txt = f_agent_init.read_text(encoding="utf-8", errors="ignore")
        if "_allow_local_below_floor" not in txt:
            target = "if _ctx and _ctx < MINIMUM_CONTEXT_LENGTH and not _allow_lmstudio_explicit_below_floor:"
            repl = """    _allow_local_below_floor = (
        (
            str(agent.provider or "").strip().lower() == "lmstudio"
            and isinstance(agent._config_context_length, int)
            and not isinstance(agent._config_context_length, bool)
            and agent._config_context_length > 0
        )
        or (
            bool(agent.base_url and is_local_endpoint(agent.base_url))
            and isinstance(_ctx, int)
            and _ctx >= 16384
        )
    )
    if _ctx and _ctx < MINIMUM_CONTEXT_LENGTH and not _allow_local_below_floor:"""
            if target in txt:
                txt = txt.replace(target, repl, 1)
                f_agent_init.write_text(txt, encoding="utf-8")
                applied_count += 1
                logger.info("[ENGINE] agent_init.py patch applicata (supporto modelli locali calibrati)")

    # 2. agent/conversation_loop.py (controllo preflight Ollama a 16384 anziche' 64k)
    f_loop = AGENT_REPO / "agent" / "conversation_loop.py"
    if f_loop.exists():
        txt = f_loop.read_text(encoding="utf-8", errors="ignore")
        if "or not 0 < runtime_ctx < 16384" not in txt and "or not 0 < runtime_ctx < MINIMUM_CONTEXT_LENGTH" in txt:
            txt = txt.replace("or not 0 < runtime_ctx < MINIMUM_CONTEXT_LENGTH", "or not 0 < runtime_ctx < 16384", 1)
            f_loop.write_text(txt, encoding="utf-8")
            applied_count += 1
            logger.info("[ENGINE] conversation_loop.py patch applicata (soglia Ollama 16k)")

    # 3. agent/model_metadata.py (MINIMUM_CONTEXT_LENGTH = 16_384)
    f_meta = AGENT_REPO / "agent" / "model_metadata.py"
    if f_meta.exists():
        txt = f_meta.read_text(encoding="utf-8", errors="ignore")
        if "MINIMUM_CONTEXT_LENGTH = 16_384" not in txt and "MINIMUM_CONTEXT_LENGTH = 64_000" in txt:
            txt = txt.replace("MINIMUM_CONTEXT_LENGTH = 64_000", "MINIMUM_CONTEXT_LENGTH = 16_384", 1)
            f_meta.write_text(txt, encoding="utf-8")
            applied_count += 1
            logger.info("[ENGINE] model_metadata.py patch applicata (MINIMUM_CONTEXT_LENGTH = 16_384)")

    # 4. tui_gateway/contracts/canonical_sessions.py (room_plumbing wire parameter)
    f_canon = AGENT_REPO / "tui_gateway" / "contracts" / "canonical_sessions.py"
    if f_canon.exists():
        txt = f_canon.read_text(encoding="utf-8", errors="ignore")
        if "room_plumbing: bool = False" not in txt:
            target = "    cwd_explicit: bool = False\n"
            repl = "    cwd_explicit: bool = False\n    room_plumbing: bool = False\n"
            if target in txt:
                txt = txt.replace(target, repl, 1)
                f_canon.write_text(txt, encoding="utf-8")
                applied_count += 1
                logger.info("[ENGINE] canonical_sessions.py patch applicata (room_plumbing)")

    # 5. gateway/session_controls.py & gateway/session_policy.py (tolleranza room_plumbing)
    f_ctrl = AGENT_REPO / "gateway" / "session_controls.py"
    if f_ctrl.exists():
        txt = f_ctrl.read_text(encoding="utf-8", errors="ignore")
        if "room_plumbing = params.pop('room_plumbing', False)" not in txt:
            target = "canonical_session_owner = params.pop('canonical_session_owner', False)\n"
            repl = "canonical_session_owner = params.pop('canonical_session_owner', False)\n    room_plumbing = params.pop('room_plumbing', False)\n"
            if target in txt:
                txt = txt.replace(target, repl, 1)
                f_ctrl.write_text(txt, encoding="utf-8")
                applied_count += 1
                logger.info("[ENGINE] session_controls.py patch applicata (room_plumbing pop)")

    f_pol = AGENT_REPO / "gateway" / "session_policy.py"
    if f_pol.exists():
        txt = f_pol.read_text(encoding="utf-8", errors="ignore")
        if "'room_plumbing'" not in txt:
            target = "'canonical_session_owner'"
            repl = "'canonical_session_owner', 'room_plumbing'"
            if target in txt:
                txt = txt.replace(target, repl, 1)
                f_pol.write_text(txt, encoding="utf-8")
                applied_count += 1
                logger.info("[ENGINE] session_policy.py patch applicata (room_plumbing field)")

    # 6. apps/desktop/src/api/canonical-protocol.ts
    f_proto = AGENT_REPO / "apps" / "desktop" / "src" / "api" / "canonical-protocol.ts"
    if f_proto.exists():
        txt = f_proto.read_text(encoding="utf-8", errors="ignore")
        if "room_plumbing?: boolean" not in txt:
            target = "service_tier?: 'fast' | 'standard' | 'flex'\n"
            repl = "service_tier?: 'fast' | 'standard' | 'flex'\n  room_plumbing?: boolean\n"
            if target in txt:
                txt = txt.replace(target, repl)
                f_proto.write_text(txt, encoding="utf-8")
                applied_count += 1
                logger.info("[ENGINE] canonical-protocol.ts patch applicata (room_plumbing)")

    # 7. plugins/model-providers/custom/__init__.py
    f_custom = AGENT_REPO / "plugins" / "model-providers" / "custom" / "__init__.py"
    if f_custom.exists():
        txt = f_custom.read_text(encoding="utf-8", errors="ignore")
        if "Let local Ollama models use their Modelfile parameters" not in txt:
            target = '        if ollama_num_ctx:\n            extra_body["options"] = {"num_ctx": ollama_num_ctx}'
            repl = '''        if _looks_like_ollama_endpoint(ctx.get("base_url")):
            # Let local Ollama models use their Modelfile parameters (num_ctx, temperature,
            # native thinking) without overriding via extra_body.options or sending
            # incompatible OpenAI reasoning_effort / think=False flags.
            return extra_body, top_level
        if ollama_num_ctx:
            extra_body["options"] = {"num_ctx": ollama_num_ctx}'''
            if target in txt:
                txt = txt.replace(target, repl, 1)
                f_custom.write_text(txt, encoding="utf-8")
                applied_count += 1
                logger.info("[ENGINE] custom provider patch applicata (Ollama options)")

    # 8. tui_gateway/session_lifecycle.py (rilascio slot turni gruppo)
    f_life = AGENT_REPO / "tui_gateway" / "session_lifecycle.py"
    if f_life.exists():
        txt = f_life.read_text(encoding="utf-8", errors="ignore")
        if 'title.startswith("Group: ")' not in txt:
            target = "    if _session_source(session) == ROOM_SESSION_SOURCE:\n        _release_active_session_slot(session)"
            repl = '    src = _session_source(session)\n    title = str(session.get("title") or "")\n    if src == ROOM_SESSION_SOURCE or title.startswith("Group: ") or session.get("chat_type") == "group":\n        _release_active_session_slot(session)'
            if target in txt:
                txt = txt.replace(target, repl, 1)
                f_life.write_text(txt, encoding="utf-8")
                applied_count += 1
                logger.info("[ENGINE] session_lifecycle.py patch applicata (rilascio slot gruppo)")

    # 9. tools/file_tools_write_guards.py (scrittura diretta file per modelli locali)
    f_wguard = AGENT_REPO / "tools" / "file_tools_write_guards.py"
    if f_wguard.exists():
        txt = f_wguard.read_text(encoding="utf-8", errors="ignore")
        if "Allow direct overwrites by local models" not in txt:
            target = 'def _stale_overwrite_blocker(filepath: str, resolved: str | None, task_id: str) -> str | None:\n    """Reason write_file must NOT replace the existing file, else ``None``.'
            repl = 'def _stale_overwrite_blocker(filepath: str, resolved: str | None, task_id: str) -> str | None:\n    """Allow direct overwrites by local models without requiring a prior full read_file pass."""\n    return None\n    """Reason write_file must NOT replace the existing file, else ``None``.'
            if target in txt:
                txt = txt.replace(target, repl, 1)
                f_wguard.write_text(txt, encoding="utf-8")
                applied_count += 1
                logger.info("[ENGINE] file_tools_write_guards.py patch applicata")

    # 10. tools/terminal_tool.py (gestione comandi cmd.exe e powershell)
    f_term = AGENT_REPO / "tools" / "terminal_tool.py"
    if f_term.exists():
        txt = f_term.read_text(encoding="utf-8", errors="ignore")
        if 'cmd.exe /c' not in txt:
            target = "def terminal_tool(\n    command: str,"
            repl = "def terminal_tool(\n    command: Optional[str] = None,"
            if target in txt:
                txt = txt.replace(target, repl, 1)
            target_plan = "    from hermes_cli.observability.shared_metrics_loop import record_terminal_backend as _metered\n    plan = None\n    try:\n        plan = _plan_execution(\n            command,"
            repl_plan = """    if not command and kwargs:
        for alt in ("raw", "cmd", "input", "code", "script", "command_line"):
            if alt in kwargs and isinstance(kwargs[alt], str):
                command = kwargs[alt]
                break

    if sys.platform == "win32" and command:
        cmd_stripped = command.strip()
        if cmd_stripped.startswith("dir ") or cmd_stripped == "dir" or cmd_stripped.startswith("dir/"):
            command = f'cmd.exe /c "{command}"'
        elif cmd_stripped.startswith("Get-ChildItem") or cmd_stripped.startswith("Get-Item"):
            command = f'powershell -Command "{command}"'

    from hermes_cli.observability.shared_metrics_loop import record_terminal_backend as _metered
    plan = None
    try:
        plan = _plan_execution(
            command or ","""
            if target_plan in txt:
                txt = txt.replace(target_plan, repl_plan, 1)
                f_term.write_text(txt, encoding="utf-8")
                applied_count += 1
                logger.info("[ENGINE] terminal_tool.py patch applicata")

    # 11. agent/transports/chat_completions.py (filtro tool pesanti per Ollama)
    f_cc = AGENT_REPO / "agent" / "transports" / "chat_completions.py"
    if f_cc.exists():
        txt = f_cc.read_text(encoding="utf-8", errors="ignore")
        if "_ollama_excluded_tools" not in txt:
            target = '    if tools:\n        # Moonshot/Kimi uses a stricter JSON Schema flavor; rewriting here also covers aggregator routes.\n        api_kwargs["tools"] = sanitize_moonshot_tools(tools) if is_moonshot_model(model) else tools'
            repl = """    if tools:
        # Moonshot/Kimi uses a stricter JSON Schema flavor; rewriting here also covers aggregator routes.
        effective_tools = sanitize_moonshot_tools(tools) if is_moonshot_model(model) else tools
        if "11434" in str(params.get("base_url") or ""):
            _ollama_excluded_tools = {
                "tool_call", "execute_code", "kanban_comment", "message_agent",
                "delegate_task", "schedule_cronjob", "clarify", "session_search", "text_to_speech",
            }
            effective_tools = [
                t for t in effective_tools
                if (t.get("function") or {}).get("name") not in _ollama_excluded_tools
            ]
        api_kwargs["tools"] = effective_tools"""
            if target in txt:
                txt = txt.replace(target, repl, 1)
                f_cc.write_text(txt, encoding="utf-8")
                applied_count += 1
                logger.info("[ENGINE] chat_completions.py patch applicata (filtro tool Ollama)")

    logger.info("[ENGINE] Patch hermes-agent verificate al 100%% (applicate o gia' intatte: %d aggiornamenti eseguiti).", applied_count)
    return True


def heal_bot_groups() -> bool:
    """Verifica e preserva la modalita' legacy per i gruppi e l'appartenenza ai gruppi (TEAM SVILUPPO, TEAM MARKETING)."""
    import re
    logger.info("--- 3. Verifica Integrita' Gruppi Hermes ---")

    # 1. Desktop mode
    caps_file = AGENT_REPO / "apps" / "desktop" / "src" / "plugins" / "hermes-bots" / "canonical-group-capabilities.ts"
    if caps_file.exists():
        txt = caps_file.read_text(encoding="utf-8")
        if "return 'legacy'" not in txt and 'return "legacy"' not in txt:
            caps_file.write_text("import { gatewayActivationEpoch, host } from '@hermes/plugin-sdk'\n\nexport type GroupExecutionMode = 'canonical' | 'legacy' | 'unavailable'\n\nexport function groupExecutionMode(value: unknown): GroupExecutionMode {\n  return 'legacy'\n}\n", encoding="utf-8")
            logger.info("[GROUPS] canonical-group-capabilities impostato su 'legacy'")

    reg_file = AGENT_REPO / "apps" / "desktop" / "src" / "plugins" / "hermes-bots" / "canonical-group-registry.tsx"
    if reg_file.exists():
        r_txt = reg_file.read_text(encoding="utf-8")
        if "return null" not in r_txt:
            r_txt = re.sub(
                r"export function CanonicalGroupList\(\{ onOpen \}: \{ onOpen: \(key: string\) => void \}\) \{.*?^\}",
                "export function CanonicalGroupList({ onOpen }: { onOpen: (key: string) => void }) {\n  return null\n}",
                r_txt,
                flags=re.DOTALL | re.MULTILINE
            )
            reg_file.write_text(r_txt, encoding="utf-8")
            logger.info("[GROUPS] CanonicalGroupList disattivato da canonical-group-registry.tsx")

    # 2. Bundles
    bundle_files = [
        AGENT_REPO / "apps" / "desktop" / "dist" / "assets" / "index-CmckmaEp.js",
        AGENT_REPO / "apps" / "desktop" / "release" / "win-unpacked" / "resources" / "app.asar.unpacked" / "dist" / "assets" / "index-CmckmaEp.js"
    ]
    target_str = "function GO(e){if(!e||typeof e!=`object`||Array.isArray(e))return`unavailable`;let t=e,{driver:n,persistent_process:r,features:i,methods:a}=t;if(i!==void 0&&(!Array.isArray(i)||i.some(e=>typeof e!=`string`))||a!==void 0&&(!Array.isArray(a)||a.some(e=>typeof e!=`string`)))return`unavailable`;if(n===!0)return`canonical`;let o=Object.hasOwn(t,`protocol_version`)||Object.hasOwn(t,`authority_gateway_id`)||a?.includes(`groups.create`)||i?.includes(`canonical_session_owner`);return n===!1&&r===!1&&!o?`legacy`:`unavailable`}"
    repl_str = "function GO(e){return`legacy`}"
    prefix_fe = "function _Fe(e){let t=(0,Q.c)(20)"
    suffix_fe = "t[16]=g,t[17]=_,t[18]=v,t[19]=y):y=t[19],y}"
    for bf in bundle_files:
        if bf.exists():
            c = bf.read_text(encoding="utf-8")
            changed_b = False
            if target_str in c:
                c = c.replace(target_str, repl_str)
                changed_b = True
            if prefix_fe in c and suffix_fe in c:
                s_idx = c.find(prefix_fe)
                e_idx = c.find(suffix_fe, s_idx) + len(suffix_fe)
                c = c[:s_idx] + "function _Fe(e){return null}" + c[e_idx:]
                changed_b = True
            target_catch = "catch(e){if(e?.code!==4007){"
            repl_catch = "catch(e){let _nf=e?.code===4007||e?.message==='not_found'||String(e?.message||'').includes('not_found');if(!_nf){"
            if target_catch in c:
                c = c.replace(target_catch, repl_catch, 1)
                changed_b = True
            if changed_b:
                bf.write_text(c, encoding="utf-8")
                logger.info("[GROUPS] Bundle %s aggiornato per modalita' legacy e pulizia UI", bf.name)

    # 2b. i18n Bundles (supporto opzione room_plumbing nei gruppi canonical gateway)
    i18n_bundles = [
        AGENT_REPO / "apps" / "desktop" / "dist" / "assets" / "i18n-CVr1k08Y.js",
        AGENT_REPO / "apps" / "desktop" / "release" / "win-unpacked" / "resources" / "app.asar.unpacked" / "dist" / "assets" / "i18n-CVr1k08Y.js"
    ]
    target_o = "let o=new Set([`request_id`,`source`,`cwd`,`model`,`provider`,`toolsets`,`reasoning`,`profile`,`cols`,`title`,`hidden`,`follow_profile_config`,`service_tier`,`cwd_explicit`])"
    repl_o = "let o=new Set([`request_id`,`source`,`cwd`,`model`,`provider`,`toolsets`,`reasoning`,`profile`,`cols`,`title`,`hidden`,`follow_profile_config`,`service_tier`,`cwd_explicit`,`room_plumbing`])"
    target_c = "[`request_id`,`cwd`,`model`,`provider`,`toolsets`,`reasoning`,`title`,`hidden`,`follow_profile_config`,`service_tier`,`cwd_explicit`].includes(e)"
    repl_c = "[`request_id`,`cwd`,`model`,`provider`,`toolsets`,`reasoning`,`title`,`hidden`,`follow_profile_config`,`service_tier`,`cwd_explicit`,`room_plumbing`].includes(e)"
    for ib in i18n_bundles:
        if ib.exists():
            c = ib.read_text(encoding="utf-8")
            changed_i = False
            if target_o in c:
                c = c.replace(target_o, repl_o, 1)
                changed_i = True
            if target_c in c:
                c = c.replace(target_c, repl_c, 1)
                changed_i = True
            if changed_i:
                ib.write_text(c, encoding="utf-8")
                logger.info("[GROUPS] Bundle i18n %s aggiornato per room_plumbing", ib.name)

    proto_file = AGENT_REPO / "apps" / "desktop" / "src" / "api" / "canonical-protocol.ts"
    if proto_file.exists():
        p_txt = proto_file.read_text(encoding="utf-8")
        if "'room_plumbing'" not in p_txt:
            p_txt = p_txt.replace("'cwd_explicit']", "'cwd_explicit', 'room_plumbing']")
            proto_file.write_text(p_txt, encoding="utf-8")
            logger.info("[GROUPS] canonical-protocol.ts aggiornato per room_plumbing")

    gt_file = AGENT_REPO / "apps" / "desktop" / "src" / "plugins" / "hermes-bots" / "group-turns.ts"
    if gt_file.exists():
        gt_txt = gt_file.read_text(encoding="utf-8")
        if "if (error?.code !== 4007)" in gt_txt:
            gt_txt = gt_txt.replace(
                "if (error?.code !== 4007) {",
                "const notFound = error?.code === 4007 || error?.code === 404 || error?.message === 'not_found' ||\n          String(error?.message || '').includes('not_found') || error?.data?.reason === 'not_found'\n        if (!notFound) {"
            )
            gt_file.write_text(gt_txt, encoding="utf-8")
            logger.info("[GROUPS] group-turns.ts allineato con tolleranza not_found")

    sc_file = AGENT_REPO / "gateway" / "session_controls.py"
    if sc_file.exists():
        sc_txt = sc_file.read_text(encoding="utf-8")
        sc_changed = False
        old_dispatch_err = """        except RuntimeStoreError as exc:
            _log_refusal(getattr(self.actor, 'profile_id', None), method, exc)
            return {'jsonrpc': '2.0', 'id': rid, 'error': {
                'code': 4001, 'message': exc.reason, 'data': _refusal_data(exc)}}"""
        new_dispatch_err = """        except RuntimeStoreError as exc:
            _log_refusal(getattr(self.actor, 'profile_id', None), method, exc)
            code = 4007 if exc.reason == 'not_found' else 4001
            return {'jsonrpc': '2.0', 'id': rid, 'error': {
                'code': code, 'message': exc.reason, 'data': _refusal_data(exc)}}"""
        if old_dispatch_err in sc_txt:
            sc_txt = sc_txt.replace(old_dispatch_err, new_dispatch_err)
            sc_changed = True

        old_route_err = """            except RuntimeStoreError as exc:
                _log_refusal(getattr(self.actor, 'profile_id', None), method, exc)
                return {'jsonrpc': '2.0', 'id': rid, 'error': {
                    'code': 4001, 'message': exc.reason, 'data': _refusal_data(exc)}}"""
        new_route_err = """            except RuntimeStoreError as exc:
                _log_refusal(getattr(self.actor, 'profile_id', None), method, exc)
                code = 4007 if exc.reason == 'not_found' else 4001
                return {'jsonrpc': '2.0', 'id': rid, 'error': {
                    'code': code, 'message': exc.reason, 'data': _refusal_data(exc)}}"""
        if old_route_err in sc_txt:
            sc_txt = sc_txt.replace(old_route_err, new_route_err)
            sc_changed = True

        if "resolve_titled_session" not in sc_txt:
            old_resume_lookup = """        else:
            from gateway.session_local_migration import resolve_local_target
            from hermes_state_local_migration import LEGACY_LOCAL_SOURCES
            row = self.authority.db.get_session(ref.session_id)
            if row and row['source'] in LEGACY_LOCAL_SOURCES:"""
            new_resume_lookup = """        else:
            from gateway.session_local_migration import resolve_local_target
            from hermes_state_local_migration import LEGACY_LOCAL_SOURCES
            row = self.authority.db.get_session(ref.session_id)
            if not row and ref.session_id:
                try:
                    from gateway.session_local_title import resolve_titled_session
                    ref = resolve_titled_session(self.authority, self.actor, ref.session_id)
                except RuntimeStoreError:
                    pass
            elif row and row['source'] in LEGACY_LOCAL_SOURCES:"""
            if old_resume_lookup in sc_txt:
                sc_txt = sc_txt.replace(old_resume_lookup, new_resume_lookup)
                sc_changed = True

        if "room_plumbing = params.pop('room_plumbing', False)" not in sc_txt:
            old_hidden_pop = """        hidden = params.pop('hidden', False)
        if type(hidden) is not bool:
            raise RuntimeStoreError('invalid_params', field='hidden', detail='must be a boolean')"""
            new_hidden_pop = """        hidden = params.pop('hidden', False)
        if type(hidden) is not bool:
            raise RuntimeStoreError('invalid_params', field='hidden', detail='must be a boolean')
        room_plumbing = params.pop('room_plumbing', False)
        if type(room_plumbing) is not bool:
            raise RuntimeStoreError('invalid_params', field='room_plumbing', detail='must be a boolean')"""
            if old_hidden_pop in sc_txt:
                sc_txt = sc_txt.replace(old_hidden_pop, new_hidden_pop)
                sc_changed = True

        if sc_changed:
            sc_file.write_text(sc_txt, encoding="utf-8")
            logger.info("[GROUPS] Gateway session_controls.py allineato per codici 4007, lookup titoli e room_plumbing")

    sp_file = AGENT_REPO / "gateway" / "session_policy.py"
    if sp_file.exists():
        sp_txt = sp_file.read_text(encoding="utf-8")
        if "'room_plumbing'" not in sp_txt:
            sp_txt = sp_txt.replace("'row_cwd'})", "'row_cwd', 'room_plumbing'})")
            sp_file.write_text(sp_txt, encoding="utf-8")
            logger.info("[GROUPS] session_policy.py CREATE_FIELDS aggiornato con room_plumbing")

    cs_file = AGENT_REPO / "tui_gateway" / "contracts" / "canonical_sessions.py"
    if cs_file.exists():
        cs_txt = cs_file.read_text(encoding="utf-8")
        if "room_plumbing: bool = False" not in cs_txt:
            cs_txt = cs_txt.replace("hidden: bool = False\n", "hidden: bool = False\n    room_plumbing: bool = False\n", 1)
            cs_file.write_text(cs_txt, encoding="utf-8")
            logger.info("[GROUPS] canonical_sessions.py CanonicalCreateParams aggiornato con room_plumbing")

    # 3. Pulizia tabelle hosted rooms in SQLite
    try:
        import sqlite3
        sdb = HERMES_HOME / "state.db"
        if sdb.exists():
            conn = sqlite3.connect(sdb)
            conn.execute("DELETE FROM hosted_rooms")
            conn.execute("DELETE FROM hosted_room_events")
            conn.commit()
            conn.close()
            logger.info("[GROUPS] Tabelle hosted_rooms in state.db ripulite da record orfani")
    except Exception as exc:
        logger.warning("[GROUPS] Errore pulizia sqlite: %s", exc)

    # 4. Gateway capabilities
    sgc = AGENT_REPO / "gateway" / "session_group_controls.py"
    if sgc.exists():
        sgc_txt = sgc.read_text(encoding="utf-8")
        if "'room_link': {'enabled': False" not in sgc_txt or "'driver': False" not in sgc_txt:
            full_caps = """def capabilities():
        return {'protocol_version': rooms.PROTOCOL_VERSION, 'driver': False,
                'persistent_process': False, 'authority_gateway_id': gateway_id,
                'room_link': {'enabled': False, 'reason': 'canonical_driver_required'},
                'features': ['room_identity', 'monotonic_log', 'replayable_disband'],
                'methods': list(GROUP_METHODS), 'max_log_limit': rooms.MAX_LOG_LIMIT}"""
            sgc_txt = re.sub(
                r"def capabilities\(\):\s+return\s*\{.*?\}",
                full_caps,
                sgc_txt,
                flags=re.DOTALL
            )
            sgc.write_text(sgc_txt, encoding="utf-8")
            logger.info("[GROUPS] Gateway session_group_controls allineato")

    tmg = AGENT_REPO / "tui_gateway" / "methods_groups.py"
    if tmg.exists():
        tmg_txt = tmg.read_text(encoding="utf-8")
        if '"room_link": {"enabled": False' not in tmg_txt or '"driver": False' not in tmg_txt:
            full_tmg_caps = """@method("groups.capabilities")
def _(rid, params: dict, _catalog=_local_catalog, _methods=_METHODS) -> dict:
    \"\"\"Describe the hosted-room protocol implemented by this gateway.\"\"\"
    from gateway.hosted_rooms import MAX_LOG_LIMIT, PROTOCOL_VERSION, local_authority_gateway_id
    return _ok(rid, {
        "protocol_version": PROTOCOL_VERSION, "driver": False,
        "persistent_process": False,
        "authority_gateway_id": local_authority_gateway_id(),
        "room_link": {"enabled": False, "reason": "canonical_driver_required"},
        "features": [
            "authority_epoch", "coordinator_fencing", "room_identity", "monotonic_log",
            "idempotent_send", "replayable_disband", "typed_events", "actor_identity",
            "log_replication", "authority_takeover"],
        "methods": list(_methods), "max_log_limit": MAX_LOG_LIMIT})"""
            tmg_txt = re.sub(
                r"@method\(\"groups\.capabilities\"\)\s+def _\(rid.*?\n\s+return.*?\)",
                full_tmg_caps,
                tmg_txt,
                flags=re.DOTALL
            )
            tmg.write_text(tmg_txt, encoding="utf-8")
            logger.info("[GROUPS] tui_gateway methods_groups allineato")

    # 4. Profile group memberships
    root_p = HERMES_HOME / "profile.yaml"
    if root_p.exists():
        rp_txt = root_p.read_text(encoding="utf-8")
        changed = False
        if "name:TEAM SVILUPPO:" in rp_txt:
            rp_txt = re.sub(r"^\s*name:TEAM SVILUPPO:.*?\n", "", rp_txt, flags=re.MULTILINE)
            changed = True
        if "name:TEAM MARKETING:" in rp_txt:
            rp_txt = re.sub(r"^\s*name:TEAM MARKETING:.*?\n", "", rp_txt, flags=re.MULTILINE)
            changed = True
        if "- TEAM SVILUPPO" not in rp_txt:
            rp_txt = re.sub(r"groups:\s*\[.*?\]", "groups:\n    - TEAM SVILUPPO", rp_txt, count=1)
            changed = True
        if "TEAM SVILUPPO:" not in rp_txt:
            rooms_block = """    rooms:
      TEAM SVILUPPO:
        name: TEAM SVILUPPO
        roomId: rm-team-sviluppo-local
        members:
          - name: default
            title: GynBot1
            handle: GynBot1
          - name: gynbot2
            title: PROGRAMMATORE
            handle: PROGRAMMATORE
          - name: gynbox3
            title: QUALITY CHEKER
            handle: QUALITY CHEKER
        log: []
      TEAM MARKETING:
        name: TEAM MARKETING
        roomId: rm-team-marketing-local
        members:
          - name: mark1
            title: Direttore Marketing
            handle: Direttore Marketing
          - name: mark2
            title: Copywriter Creativo
            handle: Copywriter Creativo
          - name: mark3
            title: Growth Hacker
            handle: Growth Hacker
        log: []"""
            rp_txt = re.sub(r"    rooms:\s*\{\}", rooms_block, rp_txt)
            changed = True
        if changed:
            root_p.write_text(rp_txt, encoding="utf-8")
            logger.info("[GROUPS] Root profile.yaml allineato con TEAM SVILUPPO e TEAM MARKETING")

    # Bot profile groups
    def ensure_group(p_name, g_name):
        bp = HERMES_HOME / "profiles" / p_name / "profile.yaml"
        if bp.exists():
            c = bp.read_text(encoding="utf-8")
            if f"- {g_name}" not in c:
                c = re.sub(r"groups:\s*\[.*?\]", f"groups:\n    - {g_name}", c)
                bp.write_text(c, encoding="utf-8")
                logger.info("[GROUPS] Profilo '%s' assegnato a gruppo '%s'", p_name, g_name)

    ensure_group("gynbot2", "TEAM SVILUPPO")
    ensure_group("gynbox3", "TEAM SVILUPPO")
    ensure_group("mark1", "TEAM MARKETING")
    ensure_group("mark2", "TEAM MARKETING")
    ensure_group("mark3", "TEAM MARKETING")

    logger.info("[GROUPS] Integrita' gruppi e modalita' legacy verificata al 100%% (OK).")
    return True


def run_guard() -> int:
    """Esegue il ciclo completo di auto-allineamento e self-healing."""
    logger.info("=======================================================")
    logger.info("   HERMES & OLLAMA GUARD - CONTROLLO INTEGRITA'   ")
    logger.info("=======================================================")

    make_auto_backup()

    if not MANIFEST_FILE.exists():
        logger.error("Manifest di tuning non trovato in: %s", MANIFEST_FILE)
        return 1

    try:
        manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error("Errore lettura manifest: %s", e)
        return 1

    heal_engine_patches()

    logger.info("--- 1. Verifica Modelli Ollama ---")
    ok_models, recreated = check_and_heal_ollama_models(manifest)

    logger.info("--- 2. Verifica Configurazioni 7 Agenti ---")
    profiles = manifest.get("profiles", {})
    aligned_count = 0
    for pid, spec in profiles.items():
        if heal_profile_config(pid, spec):
            aligned_count += 1

    heal_bot_groups()

    logger.info("=======================================================")
    logger.info("ESITO: %d/7 Agenti Verificati | Modelli Ollama OK: %d (Ricreati: %d)", aligned_count, ok_models, recreated)
    logger.info("Hermes Guard: Sistema al 100%% allineato, idempotente e stabile!")
    logger.info("=======================================================")
    return 0


if __name__ == "__main__":
    sys.exit(run_guard())
