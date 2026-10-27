# Sources

Primary documentation, original research papers and public implementation references used in this guide. Each link is cited beside the relevant claim; this index also shows where it is used.

The initial research and review took place in October 2026. Pinned AOSP links identify a specific historical implementation. Links to stable documentation, default branches or project wikis can change; record an exact version when applying their behavior to a target. Availability of a link is separate from validation of a technical claim.

| Reference | Used in |
| --- | --- |
| [AMD bitstream encryption architecture](https://docs.amd.com/r/en-US/xapp1267-encryp-efuse-program/Encrypted-Bitstream-Implementation-Overview) | [methods](methods.md), [workflow](workflow.md) |
| [AMD key storage](https://docs.amd.com/r/en-US/xapp1267-encryp-efuse-program/AES-Key-Storage) | [methods](methods.md) |
| [Android Keystore](https://developer.android.com/privacy-and-security/keystore) | [workflow](workflow.md) |
| [Android OTA documentation](https://source.android.com/docs/core/ota/tools) | [workflow](workflow.md) |
| [Android update metadata](https://android.googlesource.com/platform/system/update_engine/+/refs/heads/main/update_metadata.proto) | [methods](methods.md) |
| [BearSSL implementation discussion](https://www.bearssl.org/constanttime.html) | [methods](methods.md), [workflow](workflow.md) |
| [Binwalk entropy documentation](https://github.com/ReFirmLabs/binwalk/wiki/Generating-Entropy-Graphs) | [README](../README.md), [workflow](workflow.md) |
| [DCA](https://eprint.iacr.org/2015/753) | [methods](methods.md) |
| [ESP32 flash-encryption documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/security/flash-encryption.html) | [public-source-case-studies](public-source-case-studies.md) |
| [Frida API documentation](https://frida.re/docs/javascript-api/) | [methods](methods.md) |
| [Full AES biclique research](https://eprint.iacr.org/2011/449) | [README](../README.md), [methods](methods.md) |
| [Ghidra emulation caveats](https://ghidra.re/ghidra_docs/GhidraClass/Debugger/B2-Emulation.html) | [methods](methods.md) |
| [HALucinator research](https://www.usenix.org/conference/usenixsecurity20/presentation/clements) | [methods](methods.md) |
| [Joux’s GCM analysis](https://csrc.nist.gov/csrc/media/projects/block-cipher-techniques/documents/bcm/joux_comments.pdf) | [methods](methods.md) |
| [Linux NAND documentation](https://www.kernel.org/doc/html/v4.19/driver-api/mtdnand.html) | [methods](methods.md) |
| [MCUboot encrypted images](https://docs.mcuboot.com/encrypted_images.html) | [README](../README.md), [methods](methods.md), [public-source-case-studies](public-source-case-studies.md) |
| [Microsoft PE specification](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format) | [methods](methods.md) |
| [NIST mode review](https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8459.pdf) | [methods](methods.md) |
| [OP-TEE secure storage](https://github.com/OP-TEE/optee_docs/blob/master/architecture/secure_storage.rst) | [methods](methods.md) |
| [OpenSSL enc documentation](https://docs.openssl.org/3.2/man1/openssl-enc/) | [workflow](workflow.md) |
| [Original cold-boot research](https://www.usenix.org/legacy/event/sec08/tech/full_papers/halderman/halderman_html/) | [methods](methods.md) |
| [Pinned finishBooting implementation](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/services/java/com/android/server/am/ActivityManagerService.java#4371) | [public-source-case-studies](public-source-case-studies.md) |
| [Provider notification implementation](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/packages/SettingsProvider/src/com/android/providers/settings/SettingsProvider.java#218) | [public-source-case-studies](public-source-case-studies.md) |
| [Renode state saving](https://renode.readthedocs.io/en/latest/basic/saving.html) | [methods](methods.md) |
| [Settings cache implementation](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/core/java/android/provider/Settings.java#785) | [public-source-case-studies](public-source-case-studies.md) |
| [Settings.java](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/core/java/android/provider/Settings.java#770) | [public-source-case-studies](public-source-case-studies.md) |
| [SettingsProvider.java](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/packages/SettingsProvider/src/com/android/providers/settings/SettingsProvider.java#594) | [public-source-case-studies](public-source-case-studies.md) |
| [SQLiteDatabase.java](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/core/java/android/database/sqlite/SQLiteDatabase.java#1337) | [public-source-case-studies](public-source-case-studies.md) |
| [Syntia](https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/blazytko) | [methods](methods.md) |
| [UEFI firmware-management implementation](https://github.com/tianocore/edk2/blob/master/FmpDevicePkg/Readme.md) | [methods](methods.md) |
| [unblob guide](https://unblob.org/guide/) | [methods](methods.md), [workflow](workflow.md) |
| [Wireshark TLS documentation](https://wiki.wireshark.org/TLS) | [workflow](workflow.md) |
| [Zimerman and colleagues, 2021](https://proceedings.mlr.press/v139/zimerman21a.html) | [methods](methods.md) |
| [zlib manual](https://zlib.net/manual.html) | [methods](methods.md), [workflow](workflow.md) |
