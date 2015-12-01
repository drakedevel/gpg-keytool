Quick and dirty tool for modifying GPG SmartCard key attributes.

**WARNING**: THE SMARTCARD WILL ERASE ANY KEYSLOT YOU EDIT WITH THIS TOOL!

This should work with any SmartCard supported by GnuPG, and with both Python 2 and 3. I've tested it on Fedora 23 with a YubiKey 4.

Why do I need this?
-------------------

On-card key generation with `gpg --card-edit` is limited to the current card key attributes. The GPG command-line tools don't expose a way to change this attribute without uploading a key of the new type. While it's possible to work around this limitation  by uploading a dummy key, it's much easier to just set the flag with this tool.

The main reason you might want this is if your card shipped in `rsa2048` mode but you want to generate a `rsa4096` key on-device.

There is support for putting cards into ECDH/ECDSA/EDDSA mode, but I don't have a card which supports EC so I don't know if it works. If you try it on an EC-supporting card, please let me know the result!

Troubleshooting
---------------

Make sure no scdaemon processes are running:

`$ pkill -9f scdaemon`
