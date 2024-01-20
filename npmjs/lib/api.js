import { Application } from '@yowasp/runtime';
import { instantiate } from '../gen/yosys.js';

export { Exit } from '@yowasp/runtime';

const yosys = new Application(() => import('./resources-yosys.js'), instantiate, 'yowasp-yosys');
const runYosys = yosys.run.bind(yosys);

export { runYosys };
export const commands = { 'yosys': runYosys };
