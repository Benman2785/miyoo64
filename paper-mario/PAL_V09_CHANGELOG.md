# Paper Mario PAL v0.9-alpha

This release uses the Clean-RC1 executable built from commit
`5c61202a76d9138970442adb1e342db5d23474b2`, build stamp `7F13DC13`.
It contains the PAL gameplay port and retains the Alpha 0.4.5 RC's fixes for
PAL content and menus, TEXEL1 and sampler handling, texture cache dimensions,
Quizmo matrices, and the save path across save-state operations.

Changes after Alpha 0.4.5 RC include:

- Spiny Tromp's Vulkan interpolation duration remains intact.
- Lava Piranha vine animation DMA is handled in battle and in the overworld.
- Merlee's ritual-card image effect data is initialized.
- The triangle depth comparison respects both the geometry Z-buffer and RDP
  Z-compare settings.
- A restricted full-coverage approximation adjusts the texture-edge alpha
  threshold for one specific render mode; it is not general N64 coverage emulation.
- The HeartBlock content's relevant yaw history is reset after healing.

The user reported successful Clean-RC1 smoke and focused regression tests on
Miyoo Mini Plus, including startup, input, audio, saves and states, and the
affected scenes. The earlier M3.1 version was played through in full; that is
not a claim that Clean-RC1 received a full playthrough. A fresh Clean-RC1
rebuild using the same local image matched the tested executable byte for byte
except for its deliberately random build stamp; that rebuilt binary was not
hardware-tested.

## Credits

Thanks to Mr-Finster and the miyoo64 contributors for the original port,
renderer and handheld infrastructure, to the pmret/papermario contributors for
the decompilation, and to the other upstream projects and contributors named
in the repository. Preserve their existing notices. The player supplies their
own compatible PAL ROM; this release does not include one.
