export type Tree = {
    [name: string]: Tree | string | Uint8Array
};

export type OutputStream =
    (bytes: Uint8Array | null) => void;

export type RunOptions = {
    stdout?: OutputStream | null,
    stderr?: OutputStream | null,
    decodeASCII?: boolean
};

export type Command =
    (args?: string[], files?: Tree, options?: RunOptions) => Tree | Promise<Tree> | undefined;

export class Exit extends Error {
    code: number;
    files: Tree;
}

export const runYosys: Command;

export const commands: {
    'yosys': Command,
};
