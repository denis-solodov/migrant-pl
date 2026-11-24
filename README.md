# Migrant PL — Polish migration law skill for AI agents

An experimental, open-source Agent Skill for multilingual information on Polish migration law, residence, citizenship, international protection and administrative procedures. It guides an AI agent to verify official sources, compare lawful routes, select evidence, calculate with verified inputs and prepare drafts in Polish.

[Project website](https://denis-solodov.github.io/migrant-pl/) · [Download v1.0.1](https://github.com/denis-solodov/migrant-pl/releases/download/v1.0.1/migrant-pl-1.0.1.zip) · [Try 14 multilingual prompts](examples/try-migrant-pl.md) · [Report an issue](https://github.com/denis-solodov/migrant-pl/issues)

**Version:** 1.0.1 · **Status:** experimental public beta · **License:** MIT.

## Installation

Review `SKILL.md` and `scripts/` before installation. Skills can affect an agent's actions, and community publication is not a security certification. Install only a version and maintainer you trust. This package has no runtime installer or automatic updater.

Install the reviewed release with the version-pinned Skills CLI (Node.js 22.20+ and npm):

```bash
npx skills@1.9.0 add https://github.com/denis-solodov/migrant-pl/tree/v1.0.1 --skill migrant-pl --agent codex --copy
```

For ZIP installation, download `migrant-pl-1.0.1.zip` and `SHA256SUMS.txt` from the same versioned release. Check the expected checksum against the published release record, then verify the ZIP before extracting it:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath .\migrant-pl-1.0.1.zip
```

A matching checksum detects changed bytes relative to that record; it does not independently establish the maintainer's identity or the safety of the contents. If the source, version or checksum is unexpected, stop and review it. Do not run downloaded shell installers. Release ZIPs contain one skill folder and no install hooks.

Download the release ZIP and extract its `migrant-pl` folder into a skills directory supported by your AI agent. For a Codex project, place it at `.agents/skills/migrant-pl/` and invoke `$migrant-pl`. The folder must retain `SKILL.md`, `references/`, `assets/`, `agents/` and `scripts/`.

If your agent offers a skill-upload interface, use the release ZIP according to that product's instructions. Availability depends on the product and account. Live legal verification needs web access in the host. Arithmetic needs Python 3 and no third-party packages; the skill does not grant tool access.

For the trust boundary, source-domain checks and distribution details, see [SECURITY.md](SECURITY.md).

## What it covers

- Residence routes, employment, family, studies, EU free movement and citizenship.
- International protection, refusals, return decisions and procedural safeguards.
- Official Polish and EU legislation and national, CJEU and ECtHR case law.
- Evidence selection, income, deadlines, residence periods and Schengen arithmetic.
- Explanations in the user's language; document drafts in Polish.

The instructions require official primary sources and separate statutory requirements, office practice and uncertain interpretations. Current thresholds, laws and case law are **not** automatically updated or certified by this package.

## Try it

Ask in your preferred language. Examples include English, Ukrainian, Russian, Spanish, French, German and Polish. These are prompt examples, not evidence of equal performance across languages.

> Use $migrant-pl. I have received a request for additional documents in my temporary residence case. Explain the letter, verify the applicable deadline and help draft a response in Polish.

See [all 14 test prompts](examples/try-migrant-pl.md) and the [manual evaluation plan](tests/scenarios.md). Manual scenarios have not been executed as part of this release.

## Verification and tests

```bash
python -m unittest discover -s tests -v
python scripts/calculators.py --help
```

The 17 supplied unit tests passed during release preparation. They test arithmetic, not legal correctness or model behaviour. An automated GitHub workflow reruns them on changes.

## Feedback

Migrants, lawyers, researchers, NGOs and public administration professionals are invited to test the skill. Report problems through [GitHub Issues](https://github.com/denis-solodov/migrant-pl/issues), including the prompt, model, skill version, date, relevant answer, issue description and an official source supporting a correction where available. Use fictional or anonymised information. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Skill catalogues

- [skills.sh](https://skills.sh/denis-solodov/migrant-pl/migrant-pl)
- [agentskill.sh](https://agentskill.sh/@denis-solodov/migrant-pl)

Catalogue listings are discovery aids, not certifications of legal accuracy or security. Curated catalogue submissions are tracked separately in [Awesome Claude Skills PR #1531](https://github.com/BehiSecc/awesome-claude-skills/pull/1531) and [Awesome Legaltech PL issue #5](https://github.com/apiotrowski-afk/awesome-legaltech-pl/issues/5); neither is an accepted listing until its maintainer approves it.

## Related project

[Prawnik PL](https://github.com/denis-solodov/prawnik-pl) covers Polish law and administration more broadly. Migrant PL is published separately to maintain its migration-specific references, downloads and issue tracker.

## Disclaimer and license

Migrant PL is an experimental legal information and document-drafting tool, not a substitute for professional legal advice. Responses may contain errors and should be independently verified before use in administrative or judicial proceedings. It is not an official government service.

Released under the [MIT License](LICENSE). Copyright notices in the supplied package are retained.
