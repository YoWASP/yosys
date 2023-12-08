import { Application } from '@yowasp/runtime';
import { instantiate } from '../gen/yosys.js';

export { Exit } from '@yowasp/runtime';

// Paths are relative to the bundle, which lives in gen/ together with the other build products.
const yosys = new Application(import.meta.url, {
    'share': './yosys-share.json',
}, {
    'yosys.core.wasm': './yosys.core.wasm',
    'yosys.core2.wasm': './yosys.core2.wasm',
    'yosys.core3.wasm': './yosys.core3.wasm',
    'yosys.core4.wasm': './yosys.core4.wasm',
}, instantiate, 'yowasp-yosys');

export const runYosys = yosys.run.bind(yosys);
export { runYosys as 'cmd:yosys' };
