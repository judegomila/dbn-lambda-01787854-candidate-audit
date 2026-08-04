#!/usr/bin/env bash
set -euo pipefail

root_dir=$(cd "$(dirname "$0")/.." && pwd)
precision=${1:-256}

case "$precision" in
  ''|*[!0-9]*)
    echo "precision must be a positive integer" >&2
    exit 2
    ;;
esac
if ((precision < 64)); then
  echo "precision must be at least 64 bits" >&2
  exit 2
fi

compiler=${TRIANGLE_DINI_CC:-cc}
if ! command -v "$compiler" >/dev/null 2>&1; then
  echo "compiler not found: $compiler" >&2
  exit 2
fi

flint_prefix=${TRIANGLE_DINI_FLINT_PREFIX:-}
if [[ -z "$flint_prefix" && -f /opt/homebrew/include/flint/arb.h ]]; then
  flint_prefix=/opt/homebrew
fi

compile_flags=(-O2 -Wall -Wextra -Wpedantic -Werror "-DPREC=$precision")
link_flags=(-lflint -lm)
if [[ -n "$flint_prefix" ]]; then
  compile_flags+=("-I$flint_prefix/include")
  link_flags=("-L$flint_prefix/lib" -lflint -lm)
fi

scratch_dir=$(mktemp -d)
trap 'rm -rf "$scratch_dir"' EXIT
binary="$scratch_dir/verify_triangle_y_dini_p13_arb"
source_file="$root_dir/verifiers/verify_triangle_y_dini_p13_arb.c"

"$compiler" "${compile_flags[@]}" "$source_file" \
  "${link_flags[@]}" -o "$binary"

exact_row=(
  --t-num 16070 --t-den 100000
  --y2-num 87677 --y2-den 2500000
)

run_leg() {
  local label=$1
  local k=$2
  local nlo=$3
  local nhi=$4
  echo "LEG $label N=$nlo..$nhi"
  "$binary" "${exact_row[@]}" --nlo "$nlo" --nhi "$nhi" --k "$k"
}

run_leg P13 6 690988 728999
run_leg P11 5 729000 774999
run_leg P7 4 775000 849999
run_leg P5 3 850000 1074999
run_leg P23 2 1075000 4050000

echo "RESULT PASS: exact lower-time five-leg Triangle y-Dini schedule"
