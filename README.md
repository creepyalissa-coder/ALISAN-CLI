# ALISAN-CLI
### Cyber Infrastructure & Intelligence Toolkit

**Version:** 1.2.0
**Publisher:** Alisan Tech
**Copyright notice:** © 2026 Alisan Tech. All rights reserved.

ALISAN-CLI is an early-stage Python command-line toolkit for Termux and compatible Linux systems.

## Implemented modules

| Module | Current function | Limitation |
|---|---|---|
| Host Manager | Validates and resolves a hostname/IP | Does not manage or inventory hosts |
| Domain Checker | Validates a domain, queries DNS A/AAAA/MX/NS/TXT, performs a bounded HTTPS status check without following redirects, and saves a text report | Basic DNS/HTTPS lookup only; DNS rebinding is not fully prevented |
| Network Tools | Validates input and attempts one TCP connection to a supplied host and port | Single-port connectivity test, not a port scanner |
| Security Scanner | Checks presence of HSTS, CSP, X-Content-Type-Options, X-Frame-Options headers on a validated HTTPS URL; redirects are not followed | Header-presence check only; no vulnerability detection or exploitation |
| Report Engine | Creates a summary listing `.txt` report files | Simple report index, not a findings-analysis engine |

## Requirements
- Python 3.9 or later recommended
- Termux or compatible Linux
- Internet access for DNS/HTTPS functions

## Install

```bash
pkg update
pkg install python git
git clone https://github.com/creepyalissa-coder/ALISAN-CLI.git
cd ALISAN-CLI
python -m pip install -r requirements.txt
python main.py
```

## Authorized use
Use only on systems, domains, and networks you own or are explicitly authorized to assess. You are responsible for obtaining permission and complying with applicable laws and service terms. Do not use this toolkit to disrupt services, access data without authorization, or interfere with third-party systems.

## Privacy
The Domain Checker and Security Scanner make outbound DNS/HTTPS requests to the target supplied by the operator. Review the code before use and inspect reports before sharing them. Generated reports are ignored by Git by default to reduce accidental disclosure of target information.

## License and commercial permissions
See `LICENSE`. Public visibility does not place this project in the public domain or grant unrestricted redistribution or commercial rights. Commercial use, resale, and redistribution require separate written permission from the lawful rights holder. Third-party dependencies remain subject to their own licenses; see `THIRD_PARTY_NOTICES.md`.

## Project
- Project: ALISAN-CLI
- Publisher: Alisan Tech
- Repository: https://github.com/creepyalissa-coder/ALISAN-CLI
- Release: 1.2.0

Add an official licensing and security contact before announcing commercial support.

## Disclaimer
The software is provided "AS IS", without warranties or guarantees of any kind, to the maximum extent permitted by law.

## Version 1.2.0 security notes

- Validates hostnames, HTTPS URLs, and TCP ports.
- Rejects non-global destinations for HTTPS checks and does not follow redirects.
- Uses bounded connection/read timeouts.
- DNS validation followed by a separate HTTP client lookup does **not** fully eliminate DNS rebinding or time-of-check/time-of-use risks. Do not expose this CLI as a public scanning service; use network egress controls and pinned-IP transport for that deployment model.
- Run unit tests with `python -m unittest discover -s tests -v`.
