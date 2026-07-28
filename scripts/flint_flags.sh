#!/usr/bin/env bash
# Shared, eval-free compiler and FLINT flag resolver.
#
# After flint_resolve_flags, callers use these arrays:
#   "${FLINT_CC[@]}" ... "${FLINT_CPPFLAGS[@]}" source.c \
#     "${FLINT_LDFLAGS[@]}" -o program "${FLINT_LIBS[@]}"

flint_die() {
  echo "FLINT configuration error: $*" >&2
  return 1
}

flint_split_words() {
  local value=$1
  local target=$2
  if [[ $value == *$'\n'* || $value == *$'\r'* ]]; then
    flint_die "$target must be a single line"
    return 1
  fi
  case "$target" in
    FLINT_CC)
      read -r -a FLINT_CC <<< "$value"
      ;;
    FLINT_CPPFLAGS)
      read -r -a FLINT_CPPFLAGS <<< "$value"
      ;;
    FLINT_LDFLAGS)
      read -r -a FLINT_LDFLAGS <<< "$value"
      ;;
    *)
      flint_die "internal array name error"
      return 1
      ;;
  esac
}

flint_add_prefix() {
  local prefix=$1
  local include_dir="$prefix/include"
  local lib_dir=
  [[ -d $include_dir ]] ||
    { flint_die "missing include directory below FLINT_ROOT: $include_dir"; return 1; }
  FLINT_CPPFLAGS+=("-I$include_dir" "-I$include_dir/flint")
  if [[ -d "$prefix/lib" ]]; then
    lib_dir="$prefix/lib"
  elif [[ -d "$prefix/lib64" ]]; then
    lib_dir="$prefix/lib64"
  else
    flint_die "missing lib or lib64 directory below FLINT_ROOT: $prefix"
    return 1
  fi
  FLINT_LDFLAGS+=("-L$lib_dir" "-Wl,-rpath,$lib_dir")
}

flint_resolve_flags() {
  FLINT_CC=()
  FLINT_CPPFLAGS=()
  FLINT_LDFLAGS=()
  FLINT_LIBS=(-lflint -lgmp -lmpfr -lm)

  flint_split_words "${CC:-cc}" FLINT_CC || return 1
  ((${#FLINT_CC[@]} > 0)) ||
    { flint_die "CC resolved to an empty command"; return 1; }
  if [[ -n ${CPPFLAGS:-} ]]; then
    flint_split_words "$CPPFLAGS" FLINT_CPPFLAGS || return 1
  fi
  if [[ -n ${LDFLAGS:-} ]]; then
    flint_split_words "$LDFLAGS" FLINT_LDFLAGS || return 1
  fi

  if [[ -n ${FLINT_ROOT:-} ]]; then
    [[ $FLINT_ROOT != *$'\n'* && $FLINT_ROOT != *$'\r'* ]] ||
      { flint_die "FLINT_ROOT must be a single line"; return 1; }
    [[ -d $FLINT_ROOT ]] ||
      { flint_die "FLINT_ROOT is not a directory: $FLINT_ROOT"; return 1; }
    flint_add_prefix "$FLINT_ROOT" || return 1
  else
    local include_dir=${FLINT_INCLUDE_DIR:-}
    local lib_dir=${FLINT_LIB_DIR:-}
    if [[ -z $include_dir ]]; then
      if [[ -f /opt/homebrew/include/flint/arb.h ]]; then
        include_dir=/opt/homebrew/include
        [[ -n $lib_dir ]] || lib_dir=/opt/homebrew/lib
      elif [[ -f /usr/local/include/flint/arb.h ]]; then
        include_dir=/usr/local/include
        [[ -n $lib_dir ]] || lib_dir=/usr/local/lib
      elif [[ -f /usr/include/flint/arb.h ]]; then
        include_dir=/usr/include
      fi
    fi
    if [[ -n $include_dir ]]; then
      [[ -d $include_dir ]] ||
        { flint_die "FLINT_INCLUDE_DIR is not a directory: $include_dir"; return 1; }
      FLINT_CPPFLAGS+=("-I$include_dir")
      if [[ ${include_dir##*/} == flint ]]; then
        FLINT_CPPFLAGS+=("-I${include_dir%/*}")
      else
        FLINT_CPPFLAGS+=("-I$include_dir/flint")
      fi
    fi
    if [[ -n $lib_dir ]]; then
      [[ -d $lib_dir ]] ||
        { flint_die "FLINT_LIB_DIR is not a directory: $lib_dir"; return 1; }
      FLINT_LDFLAGS+=("-L$lib_dir" "-Wl,-rpath,$lib_dir")
    fi
  fi
}
