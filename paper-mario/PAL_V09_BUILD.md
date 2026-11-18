# Building Paper Mario PAL v0.9-alpha

The hardware-tested executable in the prepared release was built from commit
`5c61202a76d9138970442adb1e342db5d23474b2`, with stamp `7F13DC13` and SHA-256
`59ddb6c7bec337b0884a146a8aecf114448785d9164359c61983cdbc4773f9c3`.
Later documentation-only commits do not change that executable. See
`PAL_V09_CHANGELOG.md` for test scope and `miyoo/README-PAL-V09-ALPHA.txt`
for installation and save migration.

## Prerequisites and image provenance

- Git, Docker, and a compatible 64 MiB, big-endian European PAL ROM supplied by
  the builder. Its SHA-1 must be `2111d39265a317414d359e35a7d971c4dfa5f9e1`.
  Do not commit or distribute the ROM, extracted assets, or personal saves.
- The build and fresh-checkout reproduction used the existing local
  `pm64hh:decomp` image with ID
  `sha256:0c42a871ebcd90da2a7cde0ce981fd02dbd53683f9ff771c86af7b21ad1b0289`.
  It runs on linux/amd64 and contained Clang 14.0.6, Miyoo ARM hard-float GCC
  8.3.0, Ninja 1.11.1, Python 3.11.2 and splat64 0.31.0.

The repository includes `mario-kart-64/docker/Dockerfile`,
`paper-mario/docker/Dockerfile`, and `paper-mario/docker/Dockerfile.decomp` for
the image chain `mk64hh:build` -> `pm64hh:build` -> `pm64hh:decomp`. The first
Dockerfile fetches the Miyoo toolchain; later layers fetch system packages,
Python and Rust tools. The repository's Dockerfiles describe how to build these
images, but the base image and network dependencies are not all pinned by
digest. An independently rebuilt image has not been validated as identical to
the image ID above, and a public source for that exact image has not been
established. Record and verify your image and tool versions before comparing a
new build; do not assume the same output from a newly built image.

From the repository root, the documented Dockerfile chain can be built with
the following commands. These image-build commands were not rerun as part of
the fresh-checkout validation; network downloads and upstream availability
are required, and success or identity with the tested image is not established.

```sh
docker build --platform linux/amd64 -t mk64hh:build mario-kart-64/docker
docker build --platform linux/amd64 -t pm64hh:build paper-mario/docker
docker build --platform linux/amd64 -t pm64hh:decomp \
  -f paper-mario/docker/Dockerfile.decomp paper-mario/docker
docker image inspect pm64hh:decomp --format '{{.Id}}'
```

## Pinned decomp and PAL build

The following describes the commands used in the successful fresh-checkout
build. Set `ROM` to the absolute path of your own ROM and `PMROOT` to the
absolute path of the `paper-mario` directory in a fresh checkout of the source
commit above. The empty `baserom.z64` is a bind-mount target inside the checkout;
the real ROM is mounted read-only and is not copied into the tree.

```sh
cd "$PMROOT"
git clone https://github.com/pmret/papermario.git refs/papermario
git -C refs/papermario checkout --detach ee321921df2debdaae4c9c00426b6ea84f26adb5
git -C refs/papermario apply --check "$PMROOT/game/patches/decomp.patch"
git -C refs/papermario apply "$PMROOT/game/patches/decomp.patch"
touch refs/papermario/ver/pal/baserom.z64

docker run --rm --cpus 3 --entrypoint sh \
  --mount "type=bind,source=$PMROOT,target=/work" \
  --mount "type=bind,source=$ROM,target=/work/refs/papermario/ver/pal/baserom.z64,readonly" \
  --mount "type=bind,source=$ROM,target=/rom/PaperMarioPAL.z64,readonly" \
  -w /work pm64hh:decomp -c '
    set -eu
    python3 -B tools/port/prepare_splat_provider.py
    cd refs/papermario
    python3 tools/configure/src/configure/main.py pal
    ninja -j 2 generated_code_pal inc_img_bins_pal
    cd /work
    python3 -B tools/port/pal_build.py --rom /rom/PaperMarioPAL.z64
  '
```

The PAL build generates its region-specific graph, compiles the game and Miyoo
port, links the ARM executable and asset ELF, and derives a fresh matching
`recipes.bin`. Outputs are under `build/game/pal/miyoo/`. The program chooses a
new nonzero random stamp for each build and places the same stamp in the binary
and recipe file; consequently the SHA-256 is expected to differ. Keep each
binary with its own recipes. The asset data used during the build is not a
release file.

## Reproduction and validation

In the fresh checkout, the same image produced stamp `46909CB6` and binary
SHA-256 `9e1819e869a1692ad8145a1e4e63b579d3fd47a3b2c88931758ca887509f0a6c`.
Both binaries were 10,575,956 bytes and differed only at the four bytes of
`port_build_stamp` at file offset `0x3e6f80`; changing those four bytes in an
in-memory comparison to the reference stamp yielded the reference SHA-256.
The asset files matched exactly, and recipes differed only in their `STMP`
field. These offsets and hashes describe this observed build, not a guarantee
for a different toolchain. Investigate every difference in another build and
validate the binary/recipe pair before making any equivalence claim.

The tested binary, not the fresh rebuild, is used in this release. Run the
existing `tools/port/pal_release_gates.py` on a generated app-only package to
check source provenance, the binary/asset/recipe pair, relocations and ROM
leakage; the separate Ports shortcut and cover need additional package checks.
The script's `hardware_tested` value is an automated gate status, not the
user-reported hardware test record. Hardware validation is a separate step.
