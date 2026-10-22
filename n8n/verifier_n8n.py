#!/usr/bin/env python3
"""Contrôle n8n en LECTURE SEULE (requêtes GET uniquement).

Variables lues : N8N_BASE_URL et N8N_API_KEY (environnement), ou un fichier
.env passé en argument (`python3 n8n/verifier_n8n.py ~/MB-Renovation/.env.n8n`).
Le script n'exécute, ne crée, ne modifie, n'active ni ne supprime rien, et
n'affiche jamais la clé. Les redirections ne sont pas suivies avec la clé.

Sortie : santé du serveur, liste des workflows (actif, date de modification,
versionId comparée au manifest), exécutions des 48 dernières heures (erreurs
et e-mails réellement envoyés par les nœuds d'envoi).
"""
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "..", "automation", "n8n", "manifest.json")
SEND_TYPES = ("n8n-nodes-base.emailSend",)


def load_env(path):
    if path and os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    base = os.environ.get("N8N_BASE_URL", "").rstrip("/")
    key = os.environ.get("N8N_API_KEY", "")
    if not base or not key:
        sys.exit("N8N_BASE_URL et N8N_API_KEY sont requis (la clé n'est jamais affichée).")
    return base, key


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def get(base, path, key=None, params=None):
    url = base + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, method="GET")
    if key:
        req.add_header("X-N8N-API-KEY", key)
    req.add_header("Accept", "application/json")
    try:
        with OPENER.open(req, timeout=40) as r:
            body = r.read()
            return r.status, (json.loads(body) if body[:1] in (b"{", b"[") else body.decode("utf-8", "replace")[:200])
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:  # réseau, TLS, proxy
        return 0, str(e)[:200]


def paged(base, path, key, params):
    params = dict(params)
    while True:
        code, data = get(base, path, key, params)
        if code != 200 or not isinstance(data, dict):
            yield ("ERROR", code, data)
            return
        for item in data.get("data", []):
            yield item
        cur = data.get("nextCursor")
        if not cur:
            return
        params["cursor"] = cur


def main():
    base, key = load_env(sys.argv[1] if len(sys.argv) > 1 else None)
    print("== Santé du serveur")
    for p in ("/healthz", "/healthz/readiness"):
        code, _ = get(base, p)
        print(f"  {p}: HTTP {code}")

    manifest = {}
    try:
        manifest = {w["id"]: w for w in json.load(open(MANIFEST, encoding="utf-8"))["workflows"].values()}
    except Exception:
        pass

    print("\n== Workflows")
    wfs = {}
    for w in paged(base, "/api/v1/workflows", key, {"limit": 100}):
        if isinstance(w, tuple):
            print(f"  Erreur API workflows : HTTP {w[1]} {w[2] or ''}")
            return
        wfs[w["id"]] = w
    names = {}
    for w in sorted(wfs.values(), key=lambda x: x.get("name", "")):
        names.setdefault(w.get("name"), []).append(w["id"])
        m = manifest.get(w["id"])
        ver = w.get("versionId")
        drift = "" if not m else (" = manifest" if m.get("version_id") == ver else " ≠ manifest (modifié depuis le 19/10)")
        print(f"  {w.get('name')} | actif={w.get('active')} | modifié={w.get('updatedAt')} | id={w['id']} | version{drift}")
    dups = {n: ids for n, ids in names.items() if len(ids) > 1}
    print("  Doublons de nom :", dups or "aucun")
    missing = [m["name"] for i, m in manifest.items() if i not in wfs]
    print("  Workflows du manifest absents :", missing or "aucun")

    print("\n== Exécutions des 48 dernières heures")
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=48)
    for wid, w in sorted(wfs.items(), key=lambda x: x[1].get("name", "")):
        ok = err = other = sent = 0
        errors = []
        for ex in paged(base, "/api/v1/executions", key, {"workflowId": wid, "limit": 50, "includeData": "true"}):
            if isinstance(ex, tuple):
                print(f"  {w.get('name')}: erreur API HTTP {ex[1]}")
                break
            started = ex.get("startedAt") or ""
            try:
                if dt.datetime.fromisoformat(started.replace("Z", "+00:00")) < since:
                    break
            except ValueError:
                pass
            st = ex.get("status")
            if st == "success":
                ok += 1
            elif st in ("error", "crashed"):
                err += 1
                errors.append(started[:16])
            else:
                other += 1
            run = (((ex.get("data") or {}).get("resultData") or {}).get("runData")) or {}
            send_nodes = {n["name"] for n in w.get("nodes", []) if n.get("type") in SEND_TYPES}
            for name in send_nodes:
                for r in run.get(name, []):
                    if not r.get("error"):
                        sent += sum(len(b or []) for b in ((r.get("data") or {}).get("main") or []))
        if ok or err or other:
            print(f"  {w.get('name')}: succès={ok} erreurs={err} autres={other} e-mails envoyés={sent}"
                  + (f" | erreurs à {', '.join(errors[:5])}" if errors else ""))
    print("\nLecture seule terminée. Aucune modification effectuée.")


if __name__ == "__main__":
    main()
