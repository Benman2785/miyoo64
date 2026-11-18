Paper Mario PAL v0.9-alpha

Onion OS installation
---------------------
Use a Miyoo Mini family device running Onion OS with the Ports Collection
installed. The tested device is a Miyoo Mini Plus. Back up your SD card and
existing saves before installation. With the device powered off, extract the
ZIP at the root of the Onion SD card, preserving the App/ and Roms/ folders.

Supply your own compatible European PAL ROM (big-endian .z64, 64 MiB) at:
  /mnt/SDCARD/Roms/N64/PaperMarioPAL.z64
The accepted SHA-1 is 2111d39265a317414d359e35a7d971c4dfa5f9e1.
No ROM or saves are included. Start Paper Mario PAL from Apps or Games > Ports.
Refresh Onion's game list or use its Ports import if the entry is not visible.

Existing installations and saves
--------------------------------
This release uses App/PaperMarioPALv09Alpha/ and its own data/ directory.
It can coexist with other app directories, although similarly named Apps
entries may be difficult to distinguish. The Ports shortcut and cover use the
same names as other Paper Mario PAL installations. Installing them replaces
those same-named files on the card: back them up first and switch deliberately.

Regular game saves are stored as data/pm64.sav; states are data/state_XX.sav
and data/state_quick.sav. To migrate voluntarily, power off the game, back up
both data directories, then copy the desired save to this release's data/.
Never move or overwrite the original without a backup. Normal saves and states
from other builds have not been generally validated for migration; save states
are tied to the exact executable build and may be rejected. Clean-RC1 test
states use this same binary, but a copied state must still be checked. Start a
new game if unsure. Keep a working backup until loading has been verified.
