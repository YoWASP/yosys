import { Application } from '@yowasp/runtime';
import { instantiate } from '../gen/yosys.js';

export { Exit } from '@yowasp/runtime';

const resourceFileURL = new URL('./resources-yosys.js', import.meta.url);

const yosys = new Application(resourceFileURL, instantiate, 'yowasp-yosys');
const runYosys = yosys.run.bind(yosys);

export { runYosys };
export const commands = { 'yosys': runYosys };
