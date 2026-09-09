# Inputs

Declare a schema once.
`schemaToFlags` and `schemaToArgs` build the oclif surface.
`io.resolveInputs` resolves flags, env, positionals, then prompts.

```ts
import {
  InputFieldType,
  type InputSchema,
  schemaToArgs,
  schemaToFlags,
} from "@metamask/agent-wallet/plugin";

const inputs = {
  token: {
    type: InputFieldType.Text,
    flag: "token",
    message: "Token address",
    required: true,
    index: 0,
  },
  confirm: {
    type: InputFieldType.Boolean,
    flag: "confirm",
    default: false,
    prompt: false,
  },
} satisfies InputSchema;

static override flags = schemaToFlags(inputs);
static override args = schemaToArgs(inputs);
```

## Field types

Use `Text`, `Password`, `Select`, `Confirm`, or `Boolean`.

## Resolution order per field

1. CLI flag such as `--token`.
2. Environment variable if `env` is set.
3. Positional argument if `index` is set.
4. Stored fallback if configured.
5. Interactive `ask` when `prompt` is not `false` and a TTY is present.
6. Required validation, which throws `MISSING_FLAG` or another validation error.

Headless and `--json` sessions have no prompts.
Required fields must come from flags, env, or positionals.

Set `prompt: false` for agent-friendly commands.
The template `hello ping` command does this.

## Base flags

Do not add `--json`, `--format`, `--toon`, or `--verbose`.
They are inherited.

## Advanced helpers

`resolveInputs`, `mergeArgsIntoFlags`, `enumFlag`, and `trimKey` are also exported from
`@metamask/agent-wallet/plugin`.
Prefer `io.resolveInputs` inside `execute`.
