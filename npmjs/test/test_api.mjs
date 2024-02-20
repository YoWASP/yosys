import { runYosys } from '@yowasp/yosys';

runYosys(["--version"]);

const files = await runYosys(
  ["inv.v", "-p", "hierarchy -auto-top", "-o", "top.json"],
  {"inv.v": "module inv(input a, output o); assign o = ~a; endmodule"});
const actual = JSON.parse(files["top.json"]);
const expected = {
  "creator": actual["creator"],
  "modules": {
    "inv": {
      "attributes": {
        "hdlname": "inv",
        "top": "00000000000000000000000000000001",
        "src": "inv.v:1.1-1.56"
      },
      "ports": {
        "a": {
          "direction": "input",
          "bits": [ 2 ]
        },
        "o": {
          "direction": "output",
          "bits": [ 3 ]
        }
      },
      "cells": {
        "$not$inv.v:1$1": {
          "hide_name": 1,
          "type": "$not",
          "parameters": {
            "A_SIGNED": "00000000000000000000000000000000",
            "A_WIDTH": "00000000000000000000000000000001",
            "Y_WIDTH": "00000000000000000000000000000001"
          },
          "attributes": {
            "src": "inv.v:1.43-1.45"
          },
          "port_directions": {
            "A": "input",
            "Y": "output"
          },
          "connections": {
            "A": [ 2 ],
            "Y": [ 3 ]
          }
        }
      },
      "netnames": {
        "$not$inv.v:1$1_Y": {
          "hide_name": 1,
          "bits": [ 3 ],
          "attributes": {
            "src": "inv.v:1.43-1.45"
          }
        },
        "a": {
          "hide_name": 0,
          "bits": [ 2 ],
          "attributes": {
            "src": "inv.v:1.18-1.19"
          }
        },
        "o": {
          "hide_name": 0,
          "bits": [ 3 ],
          "attributes": {
            "src": "inv.v:1.28-1.29"
          }
        }
      }
    }
  }
};
if (JSON.stringify(actual) !== JSON.stringify(expected)) {
  console.log(JSON.stringify(actual));
  throw 'test failed';
}