# Investigation workflow

Begin with a precise question, such as recovering one image for static analysis, explaining a parser, or observing a setting's downstream effect. Use the [investigation template](../templates/investigation.md) to keep the answer tied to a named artifact and a reproducible experiment.

## Establish the representation

A downloaded update, extracted partition, raw flash dump and runtime snapshot can contain different bytes even when they belong to the same release. Record the acquisition source, model and hardware applicability, build or version, size, digest, acquisition time and tool versions. Retain the original separately from derivatives.

Map transformations explicitly. A possible sequence is:

```text
downloaded container
  -> authenticated package fields
  -> encrypted component
  -> compressed plaintext
  -> full or delta reconstruction
  -> filesystem or executable
  -> runtime mappings and generated code
```

This is an example, not a universal order. Mark the actual order, the signed or authenticated byte ranges, and the reference that establishes trust. Preserve unexplained gaps instead of silently filling them and calling them recovered data.

Look for full, recovery and development artifacts, source releases, SDKs, packaging tools and readable companion software. Match their applicability before using them as a reference. Android incremental updates illustrate why the exact source build matters. [Android OTA documentation](https://source.android.com/docs/core/ota/tools)

## Perform bounded file triage

The following commands inspect a local sample. Run extractors in a disposable analysis environment with appropriate resource limits: processing an unknown file can invoke complex parsers and unpack nested content. Keep resulting artifacts outside this public repository.

```sh
file firmware.bin
shasum -a 256 firmware.bin
binwalk firmware.bin
binwalk --entropy firmware.bin
unblob --report extraction-report.json firmware.bin
```

Verify syntax against the installed version. Binwalk's documented entropy graph uses a 0–8 scale; some other tools normalize values to 0–1. Record window size and normalization before comparing results. unblob reports extraction metadata and recursively handles recognized containers; review residual regions and errors. [Binwalk entropy graphs](https://github.com/ReFirmLabs/binwalk/wiki/Generating-Entropy-Graphs), [unblob guide](https://unblob.org/guide/)

Check compression wrappers, dictionaries, alignment, sparse layouts and deltas before assuming encryption. Raw DEFLATE can lack a wrapper header and checksum. Failed decompression can reflect the wrong starting point or missing dictionary. [zlib manual](https://zlib.net/manual.html)

## Identify the consumer and its dependencies

Trace the updater, installer, bootloader, application loader or configuration engine that reads the relevant bytes. Follow data from input through parsing, key setup, transformation, verification and output. Distinguish update cryptography from unrelated TLS, storage or password routines.

Record the complete cryptographic contract when applicable:

- Cipher and mode, including key size.
- Ciphertext boundaries, block or chunk layout, padding and byte order.
- Key source, key handle, wrapping scheme or derivation function.
- Salt, work factor and context strings for derivation.
- IV, nonce, counter initialization and any address-dependent tweak.
- Authentication tag, associated data and signature coverage.
- Decompression or reconstruction steps before and after decryption.

Recognizing AES constants is only a lead. Hardware instructions and bitsliced implementations can eliminate familiar lookup tables. A public verification key is not a private decryption key. [BearSSL implementation discussion](https://www.bearssl.org/constanttime.html)

## Select the shortest informative experiment

Choose according to available access and the result needed. A supported readback path on an authorized test unit may be simpler than full rehosting. A narrowly executed original reader may preserve undocumented behavior better than an immediate rewrite. An accessible process may expose plaintext while its key remains inside a separate service or hardware boundary.

| Available evidence or access | Useful next experiment |
| --- | --- |
| Files only | Recover structure, inspect alternative artifacts, compare versions and locate the consumer |
| Readable or executable updater | Trace transformations and reproduce a narrow component with controlled inputs |
| Accessible application process | Observe successful transformation boundaries and map runtime coverage |
| Partial platform model | Rehost the smallest relevant function and document every simulated dependency |
| Supported debug or recovery access | Establish readable ranges and whether the selected path exposes plaintext |
| Hardware access with a clear hypothesis | Choose an acquisition or measurement method whose observable boundary answers that hypothesis |

See the [full catalogue](methods.md) for prerequisites and limits. There is no universal ranking in which physical methods are always last or most expensive; repeatability, equipment, access and the particular channel matter.

## Reproduce and validate

Use a library or tool that implements the identified construction. `openssl enc` supports useful conventional cipher operations, but does not support authenticated modes such as GCM and CCM. Do not accept unauthenticated output from a substituted mode. [OpenSSL enc documentation](https://docs.openssl.org/3.2/man1/openssl-enc/)

For authenticated constructions, validate the original tag with the correct associated data before treating output as accepted plaintext. For signatures, identify the trusted key and exactly which representation is signed. For unsigned formats, seek an independent reference, consistent format structure and concrete behavioral checks; state the weaker assurance.

Re-run extraction on validated output when appropriate. Check sizes, offsets, stream consumption, metadata and residual bytes. A parser round trip can reveal internal consistency while preserving the same mistake in both directions. A guessed cipher key can also decrypt and re-encrypt back to the original ciphertext without being correct.

Use standard test vectors to validate an implementation, and independent target examples to validate the recovered contract. These answer different questions.

## Keep transport and payload protection separate

Observing an update download may recover the delivered package. It does not necessarily remove payload encryption. TLS analysis requires the applicable session secrets or another authorized observation point; possession of a server certificate or public key is insufficient. Wireshark documents the limited cases in which a server RSA private key can decrypt older TLS sessions, and why session key logs are more broadly applicable. [Wireshark TLS documentation](https://wiki.wireshark.org/TLS)

## Handle hardware and runtime limits explicitly

Distinguish a readable flash device from readable plaintext, a key handle from key bytes, and an emulated success response from real secret-dependent behavior. Protected hardware may perform a transformation without exporting its key. A CPU memory dump may not contain an FPGA's decrypted configuration. [Android Keystore](https://developer.android.com/privacy-and-security/keystore), [AMD encrypted bitstream architecture](https://docs.amd.com/r/en-US/xapp1267-encryp-efuse-program/Encrypted-Bitstream-Implementation-Overview)

When an experiment fails, name the stage reached and the component that emitted the error. Separate staging, process launch, transport, guest execution, initialization, observation and interpretation. Do not attribute an exit code to a particular shell or timeout utility unless the emitting path is known.

Stop repeating an experiment when no changed input, access or hypothesis can produce new information. Record the unresolved dependency and the evidence that would resolve it.
