# Reverse Engineering with AI

A practical research guide to reverse engineering encrypted firmware and software, using AI to support analysis, experiments and review.

The central question is where protected material becomes usable and whether that point is observable. Recovering a key is one route. Others include finding an equivalent plaintext artifact, observing a transformation, executing an existing reader, or reconstructing behavior without recovering the key.

This repository contains a **31-method survey**, an evidence framework, public-source examples and reusable investigation templates. It covers file analysis, software instrumentation, rehosting, hardware acquisition, side channels and cryptographic limitations. Each method distinguishes prerequisites, possible results and the evidence needed to support a conclusion.

## Start here

1. Follow the [investigation workflow](docs/workflow.md) to identify the artifact, desired outcome and available access.
2. Use the [methods survey](docs/methods.md) to choose a suitable experiment.
3. Apply the [evidence framework](docs/evidence-framework.md) before claiming recovery or explaining a failure.
4. Use the [AI collaboration guide](docs/ai-collaboration.md) to divide research and review without turning model agreement into proof.
5. Record the experiment in the [investigation template](templates/investigation.md).

The [public-source case studies](docs/public-source-case-studies.md) illustrate encrypted image design, transparent flash decryption, Android settings persistence and boot milestones. The [source index](docs/sources.md) links the documentation, implementations and papers used throughout the guide.

## Choose the result before choosing the tool

| Desired result | What would establish it |
| --- | --- |
| One plaintext artifact | Correctly scoped authentication or independent reference agreement, with coherent structure |
| A reusable content key | Independently validated decryption on applicable samples, with key scope identified |
| A device or root key | Verified key identity and scope; a content key or key handle alone is insufficient |
| An explanation of behavior | Concrete traces, dataflow and tests covering the stated behavior |
| A reconstructed executable | Format correctness plus representative behavior in a documented environment |
| A vendor-accepted modified image | Separate evidence for the actual signature and boot acceptance path |

## Corrections that change the investigation

- High entropy is a clue about randomness. Compression and encryption can both produce it; record the tool, scale and window size. [Binwalk entropy documentation](https://github.com/ReFirmLabs/binwalk/wiki/Generating-Entropy-Graphs)
- Bootloader placement follows the platform and image format. The first 64 KB is not a general extraction rule, and an update package may omit the bootloader.
- Encryption and signatures solve different problems. Recovering plaintext does not provide the signing key or establish that a modified image will boot. [MCUboot encrypted images](https://docs.mcuboot.com/encrypted_images.html)
- A successful command, plausible string, loaded library or wrapper return needs validation at the layer relevant to the claim. See the [source-based examples](docs/public-source-case-studies.md).
- Strong cryptography is not made practically breakable by a decompiler or language model. Useful progress usually comes from the surrounding implementation, accessible representations or a specific demonstrated weakness. [Full AES biclique research](https://eprint.iacr.org/2011/449)

## Scope and provenance

The initial research was developed through AI-assisted specialist research and critical review, including Astra, Opus and Fable contributions. Reviews were integrated selectively: unsupported interpretations and overlapping work were rejected. The resulting guide makes methodological claims and cites public sources; it does not claim a new universal decryptor or a demonstrated compromise of a particular device.

The public repository contains research prose, public links, blank templates and a documentation validation tool. Firmware binaries, private captures, device identifiers, extracted keys, credentials and operational logs are outside its publication scope. Apply the methods to systems and artifacts you are authorized to examine.

## Validate the repository

Python 3.9 or later is sufficient; no third-party packages are required.

```sh
python3 tools/check_docs.py
python3 tools/check_docs.py --self-test
```

The local harness checks the file inventory, Markdown links, method numbering, source index, version records and several common accidental-publication patterns. It does not execute firmware, contact devices, fetch linked websites or prove that every technical statement is correct. Source verification remains part of research review.

Current documentation version: **1.0.0**. See the [changelog](CHANGELOG.md) and append-only [history](HISTORY.md).
