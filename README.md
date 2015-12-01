Quick and dirty tool for modifying GPG Smartcard key attributes.

*WARNING*: THE SMARTCARD WILL ERASE ANY KEYSLOT YOU EDIT WITH THIS TOOL!

On-card key generation with `gpg --card-edit` is limited to the current card key attributes. The GPG command-line tools don't expose a way to change this attribute without uploading a key of the new type. While it's possible to work around this limitation  by uploading a dummy key, it's much easier to just set the flag with this tool.

I've tested this on a YubiKey 4 which shipped in rsa2048 mode -- the tool was able to set it to rsa4096 with no issue.

I added support for putting cards into ECDH/ECDSA/EDDSA mode -- I don't have a card which supports this, so I don't know if it works. If you try it on an EC-supporting card, please let me know the result!
