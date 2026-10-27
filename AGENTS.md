# Repository guidance

This repository publishes general research about reverse engineering firmware and software with AI assistance. Keep public documentation separate from device-specific working material.

- Preserve the difference between observations, hypotheses and validated results.
- Support implementation-specific claims with primary documentation or pinned source revisions.
- Do not add firmware binaries, raw memory, captures, keys, credentials, personal device identifiers or private operational logs.
- Keep third-party material linked and attributed; do not import entire source trees or articles.
- Preserve the existing method numbering and update internal links when reorganizing material.
- Update CHANGELOG.md and append to HISTORY.md for substantive changes.
- Run `python3 tools/check_docs.py` and `python3 tools/check_docs.py --self-test` before committing or pushing.
- Keep validation local unless CI is explicitly requested. Do not add paid services or device operations as documentation checks.
- Keep small tools within their owning module, with clear docstrings and input validation.
