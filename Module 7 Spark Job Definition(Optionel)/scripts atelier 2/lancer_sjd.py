"""Lance une Spark Job Definition Fabric et attend son état terminal."""

from __future__ import annotations

import argparse
import json
import logging
import time
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

LOGGER = logging.getLogger("lancer_sjd")
FABRIC_SCOPE = "https://api.fabric.microsoft.com/.default"
FABRIC_API = "https://api.fabric.microsoft.com/v1"
TERMINAUX = {"Completed", "Failed", "Cancelled", "Deduped"}


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-id", required=True)
    parser.add_argument("--sjd-id", required=True)
    parser.add_argument("--command-line-arguments", default=None)
    parser.add_argument("--credential", choices=("cli", "default"), default="cli")
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    args = parser.parse_args()
    if args.poll_seconds < 1 or args.timeout_seconds < 1:
        parser.error("Les délais doivent être strictement positifs")
    return args


def _requete(url: str, token: str, method: str = "GET", corps: dict[str, Any] | None = None):
    donnees = None if corps is None else json.dumps(corps).encode("utf-8")
    requete = Request(url, data=donnees, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "x-ms-fabric-skill": "spark-cli",
    })
    try:
        return urlopen(requete, timeout=60)
    except HTTPError as exc:
        message = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Fabric HTTP {exc.code}: {message}") from exc


def lancer(args: argparse.Namespace) -> dict[str, Any]:
    from azure.identity import AzureCliCredential, DefaultAzureCredential

    credential = AzureCliCredential() if args.credential == "cli" else DefaultAzureCredential()
    token = credential.get_token(FABRIC_SCOPE).token
    url = (f"{FABRIC_API}/workspaces/{args.workspace_id}/sparkJobDefinitions/"
           f"{args.sjd_id}/jobs/sparkjob/instances")
    corps = None
    if args.command_line_arguments:
        corps = {"executionData": {"commandLineArguments": args.command_line_arguments}}

    with _requete(url, token, method="POST", corps=corps) as reponse:
        location = reponse.headers.get("Location")
        attente = int(reponse.headers.get("Retry-After", args.poll_seconds))
        request_id = reponse.headers.get("x-ms-request-id")
    if not location:
        raise RuntimeError("La réponse 202 ne contient pas d'en-tête Location")
    LOGGER.info("Job accepté request_id=%s", request_id or "non fourni")

    echeance = time.monotonic() + args.timeout_seconds
    time.sleep(max(attente, 1))
    while time.monotonic() < echeance:
        token = credential.get_token(FABRIC_SCOPE).token
        with _requete(location, token) as reponse:
            statut = json.loads(reponse.read().decode("utf-8"))
            attente = int(reponse.headers.get("Retry-After", args.poll_seconds))
        etat = statut.get("status")
        LOGGER.info("job_instance=%s status=%s", statut.get("id"), etat)
        if etat in TERMINAUX:
            return statut
        time.sleep(max(attente, args.poll_seconds))
    raise TimeoutError(f"Le job n'a pas atteint un état terminal en {args.timeout_seconds} secondes")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    statut = lancer(arguments())
    print(json.dumps(statut, ensure_ascii=False, indent=2))
    if statut.get("status") != "Completed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

