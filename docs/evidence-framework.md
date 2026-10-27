# Evidence framework

Choose evidence for the exact claim being made. Acquiring bytes, recovering structure, decrypting content, extracting a reusable key and reproducing behavior are separate results. The six families below organize the [31 methods](methods.md); individual methods can span more than one family.

| Family | Required input or access | Possible result | Validation and limit |
| --- | --- | --- | --- |
| Acquisition and provenance | A documented source or readable interface | A reproducible artifact and coverage map | Establish identity, representation and omitted regions; a digest alone does not establish authenticity |
| Structure recovery | Bytes, format hypotheses or a known reader | Containers, offsets, streams and reconstructed objects | Check independent boundaries and references; parser self-consistency can preserve shared errors |
| Cryptographic recovery | A complete construction plus relevant key material, observations or a demonstrated weakness | Plaintext, a scoped key or a validated weakness | Validate original authentication or independent examples; plausible output does not prove the key |
| Dynamic recovery | An observable execution environment and named checkpoint | Transformed buffers, mapped code or runtime behavior | Record coverage and compare independently; one snapshot need not contain every path |
| Program analysis | Suitable code, runtime representation or traces | Dataflow, semantics and behavioral hypotheses | Check lower-level instructions and concrete outcomes; decompiler names and model agreement are hypotheses |
| Measurement and physical methods | A relevant interface, leakage channel or physical observation | Acquired state, constrained secrets or fault-dependent observations | Validate the channel and result independently; a statistical peak, readable bus or crash alone is insufficient |

## Match evidence to its scope

Authentication provides strong evidence only for the bytes, key relationship and interpretation it actually covers. A valid tag under an arbitrary untrusted key does not establish vendor provenance. A signature over an outer package does not automatically validate an analyst's later reconstruction.

An independently trusted reference digest can establish exact agreement with a named artifact. A digest calculated from the current sample provides an identity for repeatability, but no independent guarantee of authenticity. Repeated acquisitions help identify unstable reads; identical reads can still share a systematic acquisition error.

Coherent filesystems, valid executable metadata, successful decompression and representative execution corroborate a result within their tested coverage. Readable strings, low entropy, valid padding, successful loading and same-key round trips are preliminary checks.

## Use an explicit claim state

| State | Meaning |
| --- | --- |
| Observed | Directly recorded in a specified artifact, trace or source revision |
| Inferred | An explanation supported by observations, with assumptions stated |
| Independently validated | Checked against evidence that does not merely reproduce the same assumption |
| Contradicted | Conflicting evidence rejects the stated claim |
| Unknown | Available evidence does not discriminate among relevant explanations |
| Not attempted | The experiment or required stage was not run |

Do not collapse unknown into absent. A zero-byte capture, timed-out query or unrecognized header is an observation about the measurement, with a bounded effect on what can be concluded. A search with no matches establishes absence only within its stated files, representation and matching strategy.

## Trace effects across layers

For a persistent setting, the relevant chain may be:

```text
UI selection -> provider request -> storage change -> fresh readback
             -> downstream consumer -> visible or externally measured effect
```

Each arrow is a separate claim. A UI event or wrapper return can occur before persistence fails. A cached read may not establish fresh storage state. The public Android example demonstrates why the return contract must be read through the actual implementation. [Android settings case study](public-source-case-studies.md#android-settings-return-values)

For boot and graphics, describe a dependency graph instead of assuming a single total ordering. Process creation, library mapping, provider initialization, display configuration, frame production and visible output have different evidence. A boot property is useful for its defined milestone; it does not establish every downstream operation. [Boot milestone case study](public-source-case-studies.md#android-boot-milestones)

## Separate independent checks from correlated agreement

Two AI reviewers can repeat the same erroneous premise. Two parsers can share a library. A reference program and a rewrite can use the same incorrect fixture. Record what makes a check independent: separate acquisition, original authentication material, a separately derived implementation, held-out inputs, or an external observation.

For cryptographic recovery, use independent correct input/output examples. For behavioral reconstruction, reserve inputs and states that were not used to construct the model. For physical analysis, separate tuning observations from confirmation data.

Use the [investigation template](../templates/investigation.md) to state the falsifying observation before running the experiment.
