import { Application } from '@yowasp/runtime';
import * as resources from '../gen/yosys-resources.js';
import { instantiate } from '../gen/yosys.js';

export { Exit } from '@yowasp/runtime';

const yosys = new Application(resources, instantiate, 'yowasp-yosys');
const runYosys = yosys.run.bind(yosys);

export { runYosys };
export const commands = { 'yosys': runYosys };
export const version = VERSION;
