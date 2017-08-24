# Copyright 2012-2013, Andrey Kislyuk and argcomplete contributors.
# Licensed under the Apache License. See https://github.com/kislyuk/argcomplete for more info.

# Run something, muting output or redirecting it to the debug stream
# depending on the value of _ARC_DEBUG.
__python_argcomplete_run() {
    if [[ -z "$_ARC_DEBUG" ]]; then
        "$@" 8>&1 9>&2 1>/dev/null 2>&1
    else
        "$@" 8>&1 9>&2 1>&9 2>&1
    fi
}

_python_argcomplete_global() {
    local executable=$1
    local ARGCOMPLETE=1
    local IFS=$(echo -e '\v')
    COMPREPLY=( $(_ARGCOMPLETE_IFS="$IFS" \
        COMP_LINE="$COMP_LINE" \
        COMP_POINT="$COMP_POINT" \
        COMP_TYPE="$COMP_TYPE" \
        _ARGCOMPLETE_COMP_WORDBREAKS="$COMP_WORDBREAKS" \
        _ARGCOMPLETE=$ARGCOMPLETE \
        _ARGCOMPLETE_SUPPRESS_SPACE=1 \
        __python_argcomplete_run "$executable" "${COMP_WORDS[@]:1:ARGCOMPLETE-1}") )
    if [[ $? != 0 ]]; then
        unset COMPREPLY
    elif [[ "$COMPREPLY" =~ [=/:]$ ]]; then
        compopt -o nospace
    fi
}
complete -F _python_argcomplete_global git_cloc

