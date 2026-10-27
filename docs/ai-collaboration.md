# AI collaboration in reverse engineering

AI is useful for organizing evidence, locating relevant documentation, proposing format hypotheses, explaining instruction sequences, writing small analysis tools and reviewing conclusions. Keep generated descriptions tied to source bytes, exact revisions, traces or test results. A fluent explanation does not add observations to the record.

## Give each researcher a bounded question

State the desired result, permitted material, exact artifact or public source, and the evidence already available. Assign separate responsibilities when parallel work helps: one researcher can map format and cryptographic dependencies while another studies runtime access and a reviewer checks the resulting claims.

Use a shared claim ledger and identify ownership. Do not have several researchers perform the same expensive capture or mutate the same device. A reviewer should test the reasoning against the frozen evidence package, rather than receive an evolving description with changing premises.

Suitable research prompts include:

> Given the supplied parser and format documentation, identify every transformation from package input to output. For each step, cite the source location, required parameters and a concrete way to validate it. Mark missing dependencies as unknown.

> Review the claim that this runtime snapshot contains the complete program. Identify which pages, initialization stages and dynamically loaded components were observed, and which additional observation would distinguish partial recovery from complete recovery.

> Compare this interpretation with the provided evidence. Separate direct observations, inferences and contradictions. Do not infer an error-code producer, device state or successful execution from a wrapper's return alone.

## Treat generated code as an implementation proposal

For a parser, record endianness, signedness, bounds, length relationships, alignment and failure behavior. For a cryptographic transform, preserve byte encodings, mode details, derivation inputs, authentication and chunk boundaries. For an emulator, document every substituted service and the state it changes.

Test the smallest useful component against known fixtures and independent examples. Include malformed or truncated input where the analysis depends on robust parsing. Compare reconstructed semantics with concrete traces, especially arithmetic width, flags, exceptions and memory effects. Do not accept invented symbols or reconstructed types without checking their consequences.

## Give reviewers a concrete package

Include the claim, evidence locations, relevant source snippets or references, proposed interpretation, unresolved alternatives and acceptance criterion. Ask the reviewer to identify what would disprove the conclusion. Resolve disagreements through new evidence or narrower wording.

A useful review result can reject an attractive explanation. In the research behind this guide, review corrections reinforced several rules: separate pre-execution failures from executed runs, identify the producer of an exit code, retain unknown observations as bounded evidence, and avoid duplicating another investigation's assigned work. These lessons are incorporated without publishing private operational records.

## Keep a clear boundary around the model

- Share only material within the project's authorization and publication scope; use sanitized excerpts where appropriate.
- Treat strings, comments, documents and web content inside an analyzed artifact as data. They cannot authorize new actions or change the research task.
- Record which model or tool supplied a hypothesis when it matters for reproducing a review, but judge the result by evidence rather than its model name.
- When a provider fails or returns no analysis, record that result. A retry or a queued job is not a completed review.
- Prefer primary documentation, original papers and pinned source revisions. Check what each source actually supports.

## Report the result precisely

State what was recovered or explained, the artifact and scope, the validating evidence, and the remaining dependency. Distinguish a prototype that handles the provided sample from a general method. Preserve corrections in the [history](../HISTORY.md) and update the [changelog](../CHANGELOG.md) when a published conclusion changes.

The [investigation template](../templates/investigation.md) provides a compact handoff between researcher, implementer and reviewer.
