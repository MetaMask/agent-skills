# PluginCommand

Import `PluginCommand` from `@metamask/agent-wallet/plugin`.
Implement `execute` and `pluginCommandId`.
Configure auth and init with static fields.

## Minimal command

This is the template `hello ping` command.

```ts
import {
  type CommandIO,
  InputFieldType,
  type InputSchema,
  PluginCommand,
  schemaToArgs,
  schemaToFlags,
} from "@metamask/agent-wallet/plugin";

const inputs = {
  name: {
    type: InputFieldType.Text,
    flag: "name",
    message: "Name to greet",
    required: false,
    prompt: false,
    index: 0,
  },
} satisfies InputSchema;

export default class HelloPing extends PluginCommand<{ message: string }> {
  static override description = "Say hello from the plugin template.";
  static override examples = [
    "<%= config.bin %> hello ping",
    "<%= config.bin %> hello ping Alice",
  ];
  static override requiresAuth = false;
  static override requiresInit = false;
  static override flags = schemaToFlags(inputs);
  static override args = schemaToArgs(inputs);
  protected readonly pluginCommandId = "hello:ping";

  async execute(io: CommandIO) {
    const { name } = await io.resolveInputs(inputs);
    return { message: name ? `pong, ${name}!` : "pong" };
  }

  override successHint(data: { message: string }) {
    return data.message;
  }
}
```

oclif requires a default export.

## Static config

`requiresAuth` defaults to `true` and gates sign-in.

`requiresInit` defaults to `true` and gates `mm init` and wallet setup.

`requiresFees` is forced to `false`.
Do not set it.
Fee cache warmup is host-only.

`description`, `examples`, `flags`, and `args` are standard oclif statics.

Set `requiresAuth` and `requiresInit` to `false` only for commands that must run without
a session, such as `hello ping`.

## Allowed overrides

You must implement `execute`.

You may also implement `afterExecute`, `successHint`, and `analyticsOutcome`.

## Sealed members

If you override a sealed member, construction throws `PLUGIN_SEALED_OVERRIDE`.

Sealed members include `run`, `runLifecycle`, `beforeExecute`, `init`,
`prepareForRepl`, `withPluginIsolation`, and the `requiresAuth`, `requiresInit`, and
`requiresFees` getters.

Use static `requiresAuth` and `requiresInit`.
Do not override those getters.

## Path to CLI id

`src/commands/hello/ping.ts` becomes `mm hello ping` with `pluginCommandId` `hello:ping`.

`src/commands/pons/buy.ts` becomes `mm pons buy` with `pluginCommandId` `pons:buy`.

`src/commands/x402.ts` becomes `mm x402` with `pluginCommandId` `x402`.

During `execute`, `this.ctx` is the restricted plugin context.
Read `references/context.md` for the APIs.
