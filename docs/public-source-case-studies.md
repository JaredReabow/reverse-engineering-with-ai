# Public source case studies

These examples show how to reason from an implementation to a bounded conclusion. Each applies to the named reference and revision. A vendor fork or a different hardware generation requires its own applicability check.

## MCUboot encrypted images

MCUboot documents plaintext headers and TLVs around an encrypted payload. Its design uses AES-CTR content encryption with a randomized content key, distributed through supported wrapping schemes including RSA-OAEP, AES-KW and ECIES. Hashing and signature validation operate on decrypted image data. Identifying the cipher therefore leaves wrapping, counters, metadata and verification to resolve. [MCUboot encrypted-image design](https://docs.mcuboot.com/encrypted_images.html)

The analytical lesson is to map both the secret dependency chain and authentication coverage. Recovering one content key need not recover the device secret used to unwrap other keys.

## ESP32 flash encryption

Espressif's original ESP32 documentation distinguishes physical off-chip flash contents from transparently decrypted mapped reads. The key can reside in read-protected eFuse storage, and encryption depends on flash address. Secure boot is a separate feature. A valid raw flash acquisition can therefore preserve ciphertext without yielding a reusable key or freely relocatable plaintext. [ESP32 flash-encryption documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/security/flash-encryption.html)

Record the chip generation, configuration and read path. Do not transfer the original ESP32's construction to every ESP-family device.

## Android settings return values

The following observations are scoped to AOSP `frameworks/base` commit `763ef60466ac752a3031719fb86b08486c9946b1`, associated with Android 4.2.2.

The source permits a settings write wrapper to report success without proving the database insertion succeeded:

| Layer | Behavior in the pinned source |
| --- | --- |
| `Settings.System.putInt` | Converts the integer to a string and calls the settings write path |
| `NameValueCache.putStringForUser` | Calls the provider and returns true if the shown call completes without its caught `RemoteException`; it does not inspect a returned persistence result |
| `SettingsProvider.call` for a system-setting write | Calls `insertForUser`, discards its URI result and returns null |
| `insertForUser` | Can return null on a failed database insertion before updating the cache or notifying |
| `SQLiteDatabase.insert` | Catches an SQL exception and returns a failure value |

See the exact implementations: [Settings.java](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/core/java/android/provider/Settings.java#770), [SettingsProvider.java](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/packages/SettingsProvider/src/com/android/providers/settings/SettingsProvider.java#594), [SQLiteDatabase.java](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/core/java/android/database/sqlite/SQLiteDatabase.java#1337).

This establishes a source-level failure path, not a demonstrated failure on a particular device. Other exception types may propagate. Fresh readback also needs the correct user and retrieval path: the client has cache behavior and the normal provider path participates in invalidation. Avoid both assuming every read is fresh and assuming every cached read is stale. [Settings cache implementation](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/core/java/android/provider/Settings.java#785), [Provider notification implementation](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/packages/SettingsProvider/src/com/android/providers/settings/SettingsProvider.java#218)

The useful acceptance chain is request, persisted value, fresh readback, downstream consumer and observed effect. Validation should reach the layer named in the claim.

## Android boot milestones

At the same pinned commit, `ActivityManagerService.finishBooting()` sets `sys.boot_completed` and `dev.bootcomplete` before scheduling boot-completed broadcasts in the shown non-low-level-factory-test path. The property is therefore evidence of that framework checkpoint. It does not establish broadcast handling, application readiness, frame presentation or an external device effect. [Pinned finishBooting implementation](https://android.googlesource.com/platform/frameworks/base/+/763ef60466ac752a3031719fb86b08486c9946b1/services/java/com/android/server/am/ActivityManagerService.java#4371)

Represent checkpoints as a partial dependency map, with unproven edges explicit. Match each reported result to the source contract and actual observation available.

## What these examples establish

The examples illustrate three recurring distinctions: representation versus plaintext, an API result versus persistence, and a framework milestone versus a downstream effect. They provide concrete questions for an investigation; they do not substitute for matching the target artifact and collecting the required evidence.
